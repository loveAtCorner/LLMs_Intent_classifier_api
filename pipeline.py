import os
import json
from text_match.classifer import initialize_regexp_lists, match_text_with_regex
from text_match.entity import initialize_entities, check_for_entity_matches, get_highest_priority_match
from mapper import intent_encoding
from LLM_intent_classifier_api import llm_intent_classifier_api
from LLM_entity_extract_api import llm_entity_extract_apis  # 动态导入生成的实体抽取 API
from my_logger import logger
from config import INTENTS_ENTITYS_MAPPER

"""
### 关键修改点：
1. **动态选择实体抽取 API**：在 `extract_entity_with_llm` 函数中，通过传递 `entity_type` 参数，选择对应的 LLM 实体抽取 API 函数。`entity_type` 的默认值为 `"企业名称"`，但可以根据需求传递其他实体类型。

2. **异常处理**：在调用 LLM 实体抽取 API 时，增加了对 `KeyError` 的处理，以防止在 `ENTITY_PROMPTS` 中未找到对应实体类型时程序崩溃。

3. **服务函数调整**：在 `intent_classify_service` 函数中，通过从 `INTENTS_ENTITYS_MAPPER` 获取的 `required_entity_type` 来动态调用相应的 LLM 实体抽取 API。

这样修改后，`pipeline.py` 将能够根据不同的实体类型，动态调用相应的 LLM 实体抽取 API，增强了代码的灵活性和扩展性。
"""

class InterfaceException(Exception):
    """Custom exception for interface errors."""
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


def parse_data(data):
    """Extracts the first entity type and value from the parsed data."""
    if not data:
        return None, None

    key, values = next(iter(data.items()))
    return key, values[0] if values else None


def classify_intent_with_rules(query):
    """Classifies the intent using regular expressions."""
    directory = "./text_match/intent_classification"
    regexp_lists = initialize_regexp_lists(directory)
    match_results = match_text_with_regex(query, regexp_lists)
    rule_intent = next(iter(match_results), "others")
    logger.info(f"Intent classification (rules): {rule_intent}")
    return rule_intent


def classify_intent_with_llm(query):
    """Classifies the intent using the LLM API."""
    try:
        llm_intent = llm_intent_classifier_api(query)
        logger.info(f"Intent classification (LLM): {llm_intent}")
        return llm_intent
    except Exception as e:
        logger.error(f"Failed to call LLM intent classification API: {str(e)}")
        raise InterfaceException(f"Failed to call LLM intent classification API: {str(e)}", 108)


def extract_entity_with_rules(query):
    """Extracts entities using regular expressions."""
    directory = "./text_match/entity_type"
    entities_lists = initialize_entities(directory)
    match_results = check_for_entity_matches(query, entities_lists)
    select_entity = get_highest_priority_match(match_results)
    first_entity_type, first_entity_value = parse_data(select_entity)
    logger.info(f"Entity extraction (rules): Type—{first_entity_type}, Value—{first_entity_value}")
    return first_entity_value


def extract_entity_with_llm(query, entity_type="企业名称"):
    """Extracts the entity using the LLM API based on the entity type."""
    try:
        llm_entity_extract_api = llm_entity_extract_apis[entity_type]
        place_entity = llm_entity_extract_api(query)
        logger.info(f"Entity extraction (LLM): Type—{entity_type}, Value—{place_entity}")
        return place_entity
    except KeyError:
        logger.error(f"No LLM API found for entity type: {entity_type}")
        raise InterfaceException(f"No LLM API found for entity type: {entity_type}", 109)
    except Exception as e:
        logger.error(f"Failed to call LLM entity extraction API: {str(e)}")
        raise InterfaceException(f"Failed to call LLM entity extraction API: {str(e)}", 108)


def intent_classify_service(query):
    """Main service function for intent classification and entity extraction."""
    final_intent = classify_intent_with_rules(query)

    if final_intent == "others":
        final_intent = classify_intent_with_llm(query)

    final_entity = extract_entity_with_rules(query)

    # Determine if LLM-based entity extraction is needed based on the intent
    required_entity_type = INTENTS_ENTITYS_MAPPER.get(final_intent)
    if required_entity_type and final_entity is None:
        final_entity = extract_entity_with_llm(query, entity_type=required_entity_type)

    intent, type = intent_encoding(final_intent)

    interface_data = {
        "errorcode": "1",
        "result": "1",
        "data": {
            "content": query,
            "intent": intent,
            "type": type,
            "text": final_entity
        },
        "msg": "success"
    }

    interface_json = json.dumps(interface_data, ensure_ascii=False)
    logger.info(f"Final interface response: {interface_json}")

    return interface_json


if __name__ == "__main__":
    print(f"Script execution path: {os.path.abspath(__file__)}")

    request_example = {
        "header": {
            "appId": "yx_dfw_ytsb",
            "requestId": "202003080000093154723",
            "requestTime": "2024-03-21 15:40:30"
        },
        "body": {
            "content": "与杭州亚信科技有限公司定位相似的公司，都订购了哪些业务？"
        }
    }

    query = request_example['body']['content']
    response = intent_classify_service(query)
    print(response)

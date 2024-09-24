import os
import json
from text_match.classifer import initialize_regexp_lists, match_text_with_regex
from text_match.entity import initialize_entities, check_for_entity_matches, get_required_match
from mapper import intent_encoding
from LLM_intent_classifier_api import llm_intent_classifier_api
from LLM_entity_extract_api import llm_entity_extract_apis  # 动态导入生成的实体抽取 API
from my_logger import logger
from config import INTENTS_ENTITYS_MAPPER, INTENTS_ch, INTENTS_en, ENTITYS_ch, ENTITYS_en

class InterfaceException(Exception):
    """自定义接口异常处理类"""
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


def parse_data(data):
    """
    从数据中提取第一个实体类型和实体值。

    :param data: 包含实体类型和值的字典
    :return: 第一个实体类型和实体值
    """
    if not data:
        return None, None

    key, values = next(iter(data.items()))
    return key, values[0] if values else None


def classify_intent_with_rules(query):
    """
    使用正则表达式对意图进行分类。

    :param query: 用户输入的文本
    :return: 分类结果（规则匹配）
    """
    directory = "./text_match/intent_classification"
    regexp_lists = initialize_regexp_lists(directory)
    match_results = match_text_with_regex(query, regexp_lists)
    rule_intent = next(iter(match_results), "others")
    
    logger.info(f"规则意图分类结果: {rule_intent}")
    return rule_intent


def classify_intent_with_llm(query):
    """
    使用大模型（LLM）对意图进行分类。

    :param query: 用户输入的文本
    :return: 大模型分类结果
    :raises: InterfaceException 如果API调用失败
    """
    try:
        llm_intent = llm_intent_classifier_api(query)
        logger.info(f"大模型意图分类结果: {llm_intent}")
        return llm_intent
    except Exception as e:
        logger.error(f"调用LLM意图分类API失败: {str(e)}")
        raise InterfaceException(f"调用LLM意图分类API失败: {str(e)}", 108)


def extract_entity_with_rules(query, entity_type=None):
    """
    使用正则表达式提取实体。

    :param query: 用户输入的文本
    :param entity_type: 实体类型列表，若为None则返回空列表
    :return: 包含提取实体的字典列表
    """
    if entity_type is None:
        return None

    if isinstance(entity_type, str):
        entity_type = [entity_type]  # 确保 entity_type 是一个列表

    directory = "./text_match/entity_type"
    entities_lists = initialize_entities(directory)
    match_results = check_for_entity_matches(query, entities_lists)

    selected_entities = get_required_match(entity_type, match_results)
    extracted_entities = []

    if selected_entities:
        for entity, matches in selected_entities.items():
            entity_value = ", ".join(matches)
            extracted_entities.append({entity: entity_value})

    logger.info(f"规则实体抽取结果: {extracted_entities}")
    return extracted_entities if extracted_entities else None


def extract_entity_with_llm(query, entity_type=None):
    """
    使用大模型（LLM）提取实体。

    :param query: 用户输入的文本
    :param entity_type: 实体类型列表，若为None则返回空列表
    :return: 包含提取实体的字典列表
    """
    if entity_type is None:
        return None

    if isinstance(entity_type, str):
        entity_type = [entity_type]  # 确保 entity_type 是列表

    extracted_entities = []
    
    for entity in entity_type:
        try:
            llm_entity_extract_api = llm_entity_extract_apis[entity]
            extracted_entity = llm_entity_extract_api(query)
            if extracted_entity:
                extracted_entities.append({entity: extracted_entity})
        except KeyError:
            logger.error(f"找不到对应实体类型的LLM API: {entity}")
        except Exception as e:
            logger.error(f"调用LLM实体抽取API失败: {entity} - {str(e)}")

    logger.info(f"大模型实体抽取结果: {extracted_entities}")
    return extracted_entities if extracted_entities else None


def map_intent_en_to_ch(intent_en):
    """
    将英文意图映射到中文意图。

    :param intent_en: 英文意图
    :return: 对应的中文意图
    """
    try:
        intent_index = INTENTS_en.index(intent_en)
        return INTENTS_ch[intent_index]
    except ValueError:
        logger.error(f"意图 '{intent_en}' 未在 INTENTS_en 列表中找到")
        return None


def translate_entity_types_to_en(entity_type_list):
    """
    将中文实体类型列表翻译成英文。

    :param entity_type_list: 中文实体类型列表
    :return: 英文实体类型列表
    """
    translated_list = []
    for entity in entity_type_list:
        if entity in ENTITYS_ch:
            index = ENTITYS_ch.index(entity)
            translated_list.append(ENTITYS_en[index])
        else:
            translated_list.append(entity)
    return translated_list
    

def translate_entity_keys_to_ch(entity_list):
    """
    将字典中英文实体类型的 key 翻译成中文。

    :param entity_list: 包含字典的列表
    :return: 字典的 key 翻译成中文后的列表
    """
    translated_entity_list = []
    
    for entity_dict in entity_list:
        translated_dict = {}
        for key, value in entity_dict.items():
            if key in ENTITYS_en:
                index = ENTITYS_en.index(key)
                translated_key = ENTITYS_ch[index]
            else:
                translated_key = key
            translated_dict[translated_key] = value
        translated_entity_list.append(translated_dict)
    
    return translated_entity_list


def intent_classify_service(query):
    """
    意图分类和实体提取服务。

    :param query: 用户输入的文本
    :return: 最终接口响应的 JSON 字符串
    """
    # 规则分类
    final_intent = classify_intent_with_rules(query)
    print("规则分类结果:", final_intent)

    # 若规则分类为 "others"，则调用大模型分类
    if final_intent == "others":
        final_intent = classify_intent_with_llm(query)
    print("大模型分类结果:", final_intent)

    # 映射英文意图到中文
    if final_intent.isalpha() and final_intent.isascii():
        final_intent_ch = map_intent_en_to_ch(final_intent)
        required_entity_type = INTENTS_ENTITYS_MAPPER.get(final_intent_ch)
    else:
        final_intent_ch = final_intent
        required_entity_type = INTENTS_ENTITYS_MAPPER.get(final_intent_ch)

    if required_entity_type:
        required_entity_type = required_entity_type.split()
        required_entity_type_en = translate_entity_types_to_en(required_entity_type)
    else:
        required_entity_type_en = None

    # 规则实体抽取
    final_entity = extract_entity_with_rules(query, required_entity_type_en)
    if final_entity:
        final_entity = translate_entity_keys_to_ch(final_entity)
    print("规则实体抽取结果:", final_entity)

    # 大模型实体抽取（若规则抽取无结果）
    if required_entity_type and final_entity is None:
        final_entity = extract_entity_with_llm(query, entity_type=required_entity_type)
        print("大模型实体抽取结果:", final_entity)

    # 意图编码
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
    logger.info(f"最终接口响应: {interface_json}")

    return interface_json


if __name__ == "__main__":
    print(f"脚本执行路径: {os.path.abspath(__file__)}")

    request_example = {
        "header": {
            "appId": "yx_dfw_ytsb",
            "requestId": "202003080000093154723",
            "requestTime": "2024-03-21 15:40:30"
        },
        "body": {
            "content": "给客户推荐路演活动的策划方案，时间是中秋节或者重阳节，公司叫做华为科技有限公司"
        }
    }

    query = request_example['body']['content']
    response = intent_classify_service(query)
    print(response)

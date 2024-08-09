import asyncio
import json
from text_match.classifer import initialize_regexp_lists, match_text_with_regex
from text_match.entity import initialize_entities, check_for_entity_matches, get_highest_priority_match
from mapper import intent_encoding
from LLMs_intent_classifier import llm_intent_classifier_api_asyn
from LLMs_entity_extract import llm_entity_extract_api_asyn
from my_logger import logger

# 解析实体数据函数
def parse_data(data):
    if not data:
        return None, None

    key, values = next(iter(data.items()))
    first_entity_type = key
    first_entity_value = values[0] if values else None

    return first_entity_type, first_entity_value

async def intent_classify_service_asyn(query):
    # 初始化局部变量，避免使用全局变量
    final_intent = None
    final_entity = None

    # 第一步：规则分类
    directory = "./text_match/intent_classification"
    regexp_lists = initialize_regexp_lists(directory)
    match_results = match_text_with_regex(query, regexp_lists)

    rule_intent = next(iter(match_results)) if match_results else "others"
    logger.info(f"意图规则分类结果: {rule_intent}")
    final_intent = rule_intent

    # 定义要并发执行的任务列表
    tasks = []

    # 第二步：如果规则分类为“others”，使用大模型进行分类
    if rule_intent == "others":
        tasks.append(llm_intent_classifier_api_asyn(query))

    # 第三步：规则实体抽取
    directory = "./text_match/entity_type"
    entities_lists = initialize_entities(directory)
    match_results = check_for_entity_matches(query, entities_lists)
    select_entity = get_highest_priority_match(match_results)
    first_entity_type, first_entity_value = parse_data(select_entity)

    logger.info(f"实体规则提取结果: 实体类型——{first_entity_type}，实体内容——{first_entity_value}")
    final_entity = first_entity_value

    # 第四步：如果规则抽取实体失败，使用大模型进行实体抽取
    if final_entity is None:
        tasks.append(llm_entity_extract_api_asyn(query))

    # 并发执行所有任务
    if tasks:
        results = await asyncio.gather(*tasks)

        # 根据任务的顺序分别获取结果
        for result in results:
            if isinstance(result, str):  # 假设llm_intent_classifier_api_asyn返回的是字符串
                final_intent = result
            else:  # 假设llm_entity_extract_api_asyn返回的是实体
                final_entity = result

    # 意图编码
    intent, type = intent_encoding(final_intent)

    # 构建接口返回数据
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

    # 转换为JSON字符串并打印
    interface_json = json.dumps(interface_data, ensure_ascii=False)

    return interface_json

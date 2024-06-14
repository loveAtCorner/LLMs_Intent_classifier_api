import os
import json
import asyncio
import aiofiles
from text_match.classifer import initialize_regexp_lists, match_text_with_regex
from text_match.entity import initialize_entities, check_for_entity_matches, get_highest_priority_match
from mapper import intent_encoding
from LLM_intent_classifier_api_asyn import llm_intent_classifier_api_asyn
from LLM_entity_extract_api_asyn import llm_entity_extract_api_asyn
from my_logger import *

# 自定义接口异常类
class InterfaceException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# 解析实体数据函数
def parse_data(data):
    if not data:
        return None, None

    key, values = next(iter(data.items()))
    first_entity_type = key
    first_entity_value = values[0] if values else None

    return first_entity_type, first_entity_value

async def intent_classify_service_asyn(query):
    global final_intent
    global final_entity

    # 第一步：规则分类
    directory = "./text_match/intent_classification"
    regexp_lists = initialize_regexp_lists(directory)
    match_results = match_text_with_regex(query, regexp_lists)

    rule_intent = next(iter(match_results)) if match_results else "others"
    logger.info(f"意图规则分类结果: {rule_intent}")
    final_intent = rule_intent
    print(1)

    # 第二步：如果规则分类为“others”，使用大模型进行分类
    if rule_intent == "others":
        try:
            llm_intent = await llm_intent_classifier_api_asyn(query)
            logger.info(f"大模型意图分类结果: {llm_intent}")
        except Exception as e:
            logger.error(f"大模型意图分类接口调用失败: {str(e)}")
            raise InterfaceException(f"大模型意图分类接口调用失败: {str(e)}", 108)
        final_intent = llm_intent
        print(2)

    # 第三步：规则实体抽取
    directory = "./text_match/entity_type"
    entities_lists = initialize_entities(directory)
    match_results = check_for_entity_matches(query, entities_lists)
    select_entity = get_highest_priority_match(match_results)
    first_entity_type, first_entity_value = parse_data(select_entity)

    logger.info(f"实体规则提取结果: 实体类型——{first_entity_type}，实体内容——{first_entity_value}")
    final_entity = first_entity_value
    print(3)

    # 第四步：如果规则抽取实体失败，使用大模型进行实体抽取
    if final_entity is None:
        try:
            place_entity = await llm_entity_extract_api_asyn(query)
            entity_type = "enterprise_name"
            logger.info(f"大模型企业名称实体提取结果: 实体类型——{entity_type}，实体内容——{place_entity}")
        except Exception as e:
            logger.error(f"大模型实体抽取接口调用失败: {str(e)}")
            raise InterfaceException(f"大模型实体抽取接口调用失败: {str(e)}", 108)
        final_entity = place_entity
        print(4)

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
    print(interface_json)

    return interface_json

async def process_question(query):
    result = await intent_classify_service_asyn(query)
    return query, result

async def main():
    current_path = os.getcwd()
    print("当前路径是:", current_path)

    async with aiofiles.open('./test/query_small.txt', 'r', encoding='utf-8') as file:
        queries = await file.readlines()

    tasks = [process_question(query.strip()) for query in queries]
    results = await asyncio.gather(*tasks)

    async with aiofiles.open('./test/api_response_small.txt', 'w', encoding='utf-8') as answer_file:
        for query, result in results:
            print(result)
            await answer_file.write(result + '\n')

if __name__ == "__main__":
    # 打印当前脚本的执行路径
    print(f"当前脚本的执行路径: {os.path.abspath(__file__)}")

    # 异步运行主函数
    asyncio.run(main())

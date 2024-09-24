import requests
import json
import os
from my_logger import logger
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, HEADERS, ENTITY_PROMPTS

def request(system_prompt, user_prompt):
    """
    发送请求到大模型的 API，并返回响应。
    
    :param system_prompt: 系统提示词
    :param user_prompt: 用户输入的提示词
    :return: 大模型返回的响应
    """
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    response = requests.post(LLM_QUESTION_URL_CONFIG, json=data, headers=HEADERS)
    return response

def create_llm_entity_extract_api(system_prompt_path, user_prompt_path, entity_key):
    """
    动态创建实体抽取的 API 调用函数。
    
    :param system_prompt_path: 系统提示词文件路径
    :param user_prompt_path: 用户提示词文件路径
    :param entity_key: 在返回的 JSON 数据中要提取的键
    :return: 实体抽取函数
    """
    def llm_entity_extract_api(input_text):
        # 读取系统提示词和用户提示词
        with open(system_prompt_path, 'r', encoding='utf-8') as file:
            system_prompt = file.read()

        with open(user_prompt_path, 'r', encoding='utf-8') as file:
            user_prompt_template = file.read()

        user_prompt = user_prompt_template.replace("此处为任意文本", input_text)
        data = request(system_prompt, user_prompt)
        print(data.text)
        logger.info(f"API响应: {data.text}")

        try:
            # 解析大模型返回的响应
            parsed_data = json.loads(data.text)
            message_content = parsed_data['choices'][0]['message']['content']

            # 解析 content 字段中的 JSON 数据
            entity_data = json.loads(message_content)
            entity_name = entity_data.get(entity_key, "")

            if not entity_name:
                logger.warning(f"键 {entity_key} 对应的值为空")
                entity_name = ""
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"解析错误: {str(e)}, 完整响应: {data.text}")
            entity_name = ""

        return entity_name

    return llm_entity_extract_api

# 动态创建多个实体抽取函数，键为实体类型，值为该类型在响应中的键
llm_entity_extract_apis = {}
for entity_type, prompts in ENTITY_PROMPTS.items():
    llm_entity_extract_apis[entity_type] = create_llm_entity_extract_api(
        prompts["system_prompt"],
        prompts["user_prompt"],
        prompts["entity_key"]  # 从配置中提取响应中需要抽取的键
    )

if __name__ == '__main__':
    current_path = os.getcwd()
    print("当前路径是:", current_path)

    with open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = file.readlines()

    with open('./test/LLMs_entities.txt', 'w', encoding='utf-8') as answer_file:
        for question in questions:
            question = question.strip()

            # 使用指定的API进行实体抽取，这里可以选择不同的实体类型
            entity = llm_entity_extract_apis['产品名称'](question)  # 替换为需要的实体类型
            print(entity)
            answer_file.write(question + '————' + str(entity) + '\n')

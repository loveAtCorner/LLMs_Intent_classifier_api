import requests
import json
import os
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, HEADERS, ENTITY_PROMPTS

"""
优化内容

1. **动态生成实体抽取函数**：根据 `config.py` 中的 `ENTITY_PROMPTS` 生成多个实体抽取 API 函数，每个函数对应不同的实体类型（如 "企业名称"、"可添加一" 等）。
2. **访问特定实体类型的 API**：在实际调用中，可以通过实体类型（如 `'企业名称'`）来访问相应的抽取函数。这使得代码更加灵活，可以支持不同的实体类型。
3. **修改动态字典的键**：原先以数字索引为键的字典 `llm_entity_extract_apis`，现在以实体类型为键，这样可以通过实体类型名称直接访问对应的 API 函数。
"""

def request(system_prompt, user_prompt):
    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0
    }

    response = requests.post(LLM_QUESTION_URL_CONFIG, json=data, headers=HEADERS)
    return response

def create_llm_entity_extract_api(system_prompt_path, user_prompt_path):
    def llm_entity_extract_api(input_text):
        with open(system_prompt_path, 'r', encoding='utf-8') as file:
            system_prompt = file.read()

        with open(user_prompt_path, 'r', encoding='utf-8') as file:
            user_prompt_template = file.read()

        user_prompt = user_prompt_template.replace("此处为任意文本", input_text)
        data = request(system_prompt, user_prompt)

        parsed_data = json.loads(data.text)
        entity_name = json.loads(parsed_data['choices'][0]['message']['content'])['CompanyName']

        return entity_name

    return llm_entity_extract_api

# 动态创建多个实体抽取函数，键为实体类型
llm_entity_extract_apis = {}

for entity_type, prompts in ENTITY_PROMPTS.items():
    llm_entity_extract_apis[entity_type] = create_llm_entity_extract_api(
        prompts["system_prompt"], prompts["user_prompt"]
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
            entity = llm_entity_extract_apis['企业名称'](question)  # 替换为需要的实体类型
            print(entity)
            answer_file.write(question + '————' + str(entity) + '\n')

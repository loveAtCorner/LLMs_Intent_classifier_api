# -*- coding: utf-8 -*-
import os
import requests
import json
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, HEADERS, INTENT_SYSTEM_PROMPT, INTENT_USER_PROMPT


def request(system_prompt, user_prompt):
    # 定义请求的数据
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

    # 直接使用配置文件中的HEADERS
    response = requests.post(LLM_QUESTION_URL_CONFIG, json=data, headers=HEADERS)
    return response



def llm_intent_classifier_api(text):
    with open(INTENT_SYSTEM_PROMPT, 'r', encoding='utf-8') as file:
        system_prompt = file.read()

    with open(INTENT_USER_PROMPT, 'r', encoding='utf-8') as file:
        user_prompt_template = file.read()

    # 替换文本
    user_prompt = user_prompt_template.replace("此处为任意文本", text)

    # 发送请求并获取响应
    data = request(system_prompt, user_prompt)

    # 将JSON字符串解析为Python字典
    parsed_data = json.loads(data.text)

    # 提取信息
    user_input = json.loads(parsed_data['choices'][0]['message']['content'])['UserInput']
    intent_type = json.loads(parsed_data['choices'][0]['message']['content'])['IntentType']

    return intent_type

if __name__ == '__main__':
    current_path = os.getcwd()
    print("当前路径是:", current_path)

    with open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = file.readlines()

    with open('./test/LLMs_intents.txt', 'w', encoding='utf-8') as answer_file:
        for question in questions:
            question = question.strip()
            intent_type = llm_intent_classifier_api(question)
            print(intent_type)
            answer_file.write(question + '————' + str(intent_type) + '\n')
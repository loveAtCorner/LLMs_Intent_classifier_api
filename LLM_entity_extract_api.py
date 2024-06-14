# -*- coding: utf-8 -*-
import requests
import time
import json
import re
import os
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, STATUS

question_url = LLM_QUESTION_URL_CONFIG

def request(system_prompt, user_prompt):

    # 定义请求头
    headers = {
        'Authorization': 'Bearer sk-t6bAw31nIfa2ONFI5dBeD59bFfB04194917fF1A15f5286F3',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    
    # 定义请求的数据
    data = {
        "model": MODEL_NAME,
        "messages": [
            {   "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0
    }

    # 根据配置决定是否包含headers
    if STATUS == 'test':
        response = requests.post(question_url, json=data, headers=headers)
    elif STATUS == 'online':
        response = requests.post(question_url, json=data)
    else:
        raise ValueError("Invalid config value. Expected 'test' or 'online'.")
    
    return response

def llm_entity_extract_api(input_text):
    
    with open('./prompt/system_prompt_entity.txt', 'r', encoding='utf-8') as file:
        system_prompt = file.read()

    with open('./prompt/user_prompt_entity.txt', 'r', encoding='utf-8') as file:
        user_prompt_template = file.read()
        
    # 替换文本
    user_prompt = user_prompt_template.replace("此处为任意文本", input_text)

    data = request(system_prompt, user_prompt)
    
    # 将JSON字符串解析为Python字典
    parsed_data = json.loads(data.text)
    print(parsed_data)
    # 提取信息
    entity_name = json.loads(parsed_data['choices'][0]['message']['content'])['CompanyName']
    # 打印提取的信息
    # print(f"实体名称: {entity_name}")
    
    return entity_name
    
    
if __name__ == '__main__':

    current_path = os.getcwd()
    print("当前路径是:", current_path)
    
    with open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = file.readlines()
    
    with open('./test/LLMs_entities.txt','w',encoding='utf-8') as answer_file:
        for question in questions:
            question = question.strip()
            entity = llm_entity_extract_api(question)
            print(entity)
            answer_file.write(question+'————'+str(entity)+'\n')


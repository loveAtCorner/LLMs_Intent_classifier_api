# -*- coding: utf-8 -*-
import asyncio
import aiofiles
import httpx
import json
import os
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, STATUS

question_url = LLM_QUESTION_URL_CONFIG

async def request(system_prompt, user_prompt):
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
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    async with httpx.AsyncClient(timeout=30) as client:  # 增加超时时间
        for attempt in range(3):  # 重试机制，最多尝试3次
            try:
                if STATUS == 'test':
                    response = await client.post(question_url, json=data, headers=headers)
                elif STATUS == 'online':
                    response = await client.post(question_url, json=data)
                else:
                    raise ValueError("Invalid config value. Expected 'test' or 'online'.")
                
                response.raise_for_status()  # 如果响应状态码不是200，则引发HTTPError
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                print(f"An error occurred: {exc}")
                if attempt < 2:  # 重试前等待一段时间
                    await asyncio.sleep(2)
                else:
                    raise  # 超过最大重试次数，抛出异常

async def llm_entity_extract_api_asyn(input_text):
    async with aiofiles.open('./prompt/system_prompt_entity.txt', 'r', encoding='utf-8') as file:
        system_prompt = await file.read()

    async with aiofiles.open('./prompt/user_prompt_entity.txt', 'r', encoding='utf-8') as file:
        user_prompt_template = await file.read()

    # 替换文本
    user_prompt = user_prompt_template.replace("此处为任意文本", input_text)

    data = await request(system_prompt, user_prompt)

    # 将JSON字符串解析为Python字典
    parsed_data = json.loads(data.text)
    print(parsed_data)
    # 提取信息
    entity_name = json.loads(parsed_data['choices'][0]['message']['content'])['CompanyName']
    
    return entity_name

async def process_question(question):
    entity = await llm_entity_extract_api_asyn(question.strip())
    return question, entity

async def main():
    current_path = os.getcwd()
    print("当前路径是:", current_path)

    async with aiofiles.open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = await file.readlines()

    tasks = [process_question(question) for question in questions]
    results = await asyncio.gather(*tasks)

    async with aiofiles.open('./test/LLMs_entities.txt', 'w', encoding='utf-8') as answer_file:
        for question, entity in results:
            print(entity)
            await answer_file.write(question.strip() + '————' + str(entity) + '\n')

if __name__ == '__main__':
    asyncio.run(main())

# -*- coding: utf-8 -*-
import asyncio
import aiofiles
import httpx
import json
import os
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, STATUS

question_url = LLM_QUESTION_URL_CONFIG

async def request(system_prompt, user_prompt):
    headers = {
        'Authorization': 'Bearer sk-t6bAw31nIfa2ONFI5dBeD59bFfB04194917fF1A15f5286F3',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    async with httpx.AsyncClient(timeout=30) as client:
        for attempt in range(3):
            try:
                if STATUS == 'test':
                    response = await client.post(question_url, json=data, headers=headers)
                elif STATUS == 'online':
                    response = await client.post(question_url, json=data)
                else:
                    raise ValueError("Invalid config value. Expected 'test' or 'online'.")
                
                response.raise_for_status()
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                print(f"An error occurred: {exc}")
                if attempt < 2:
                    await asyncio.sleep(2)
                else:
                    raise

async def llm_intent_classifier_api_asyn(text):
    async with aiofiles.open('./prompt/system_prompt_classifier.txt', 'r', encoding='utf-8') as file:
        system_prompt = await file.read()

    async with aiofiles.open('./prompt/user_prompt_classifier.txt', 'r', encoding='utf-8') as file:
        user_prompt_template = await file.read()

    user_prompt = user_prompt_template.replace("此处为任意文本", text)
    data = await request(system_prompt, user_prompt)
    
    parsed_data = json.loads(data.text)
    print(parsed_data)

    user_input = json.loads(parsed_data['choices'][0]['message']['content'])['UserInput']
    intent_type = json.loads(parsed_data['choices'][0]['message']['content'])['IntentType']

    return intent_type

async def process_question(question):
    intent_type = await llm_intent_classifier_api_asyn(question.strip())
    return question, intent_type

async def main():
    current_path = os.getcwd()
    print("当前路径是:", current_path)

    async with aiofiles.open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = await file.readlines()

    tasks = [process_question(question) for question in questions]
    results = await asyncio.gather(*tasks)

    async with aiofiles.open('./test/LLMs_intents.txt', 'w', encoding='utf-8') as answer_file:
        for question, intent_type in results:
            print(intent_type)
            await answer_file.write(question.strip() + '————' + str(intent_type) + '\n')

if __name__ == '__main__':
    asyncio.run(main())

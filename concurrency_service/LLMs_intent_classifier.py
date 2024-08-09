import json
import asyncio
import aiofiles
from LLMs_base_function_asyn import request, read_prompt_file

async def llm_intent_classifier_api_asyn(text):
    system_prompt = await read_prompt_file('./prompt/system_prompt_classifier.txt')
    user_prompt_template = await read_prompt_file('./prompt/user_prompt_classifier.txt')

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
    async with aiofiles.open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = await file.readlines()

    tasks = [process_question(question) for question in questions]
    results = await asyncio.gather(*tasks)

    async with aiofiles.open('./test/LLMs_intents.txt', 'w', encoding='utf-8') as answer_file:
        for question, intent_type in results:
            await answer_file.write(question.strip() + '————' + str(intent_type) + '\n')

if __name__ == '__main__':
    asyncio.run(main())

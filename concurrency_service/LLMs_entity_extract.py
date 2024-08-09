import json
import asyncio
import aiofiles
from LLMs_base_function_asyn import request, read_prompt_file

async def llm_entity_extract_api_asyn(input_text):
    system_prompt = await read_prompt_file('./prompt/system_prompt_entity.txt')
    user_prompt_template = await read_prompt_file('./prompt/user_prompt_entity.txt')

    user_prompt = user_prompt_template.replace("此处为任意文本", input_text)
    data = await request(system_prompt, user_prompt)

    parsed_data = json.loads(data.text)
    print(parsed_data)

    entity_name = json.loads(parsed_data['choices'][0]['message']['content'])['CompanyName']
    return entity_name

async def process_question(question):
    entity = await llm_entity_extract_api_asyn(question.strip())
    return question, entity

async def main():
    async with aiofiles.open('./test/query.txt', 'r', encoding='utf-8') as file:
        questions = await file.readlines()

    tasks = [process_question(question) for question in questions]
    results = await asyncio.gather(*tasks)

    async with aiofiles.open('./test/LLMs_entities.txt', 'w', encoding='utf-8') as answer_file:
        for question, entity in results:
            await answer_file.write(question.strip() + '————' + str(entity) + '\n')

if __name__ == '__main__':
    asyncio.run(main())

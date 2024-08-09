import asyncio
import aiofiles
import httpx
import json
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, STATUS, CONCURRENCY_LIMIT

question_url = LLM_QUESTION_URL_CONFIG

# Semaphore to limit concurrency, using value from configuration
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

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

    async with semaphore:
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

async def read_prompt_file(file_path):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        return await file.read()

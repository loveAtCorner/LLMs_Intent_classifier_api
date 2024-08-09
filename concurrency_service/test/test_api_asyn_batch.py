
import asyncio
import httpx
import logging
import time
import aiofiles

"""
并发请求部分
- **并发请求**：该脚本通过 `httpx.AsyncClient` 和 `asyncio.gather` 实现了并发请求，能够同时向API发送多个请求，大幅度提升了请求处理效率。
- **重试机制**：脚本为每个请求提供了最多3次的重试机会，确保在请求失败时能够进行一定程度的自动恢复。
- **日志记录**：脚本详细记录了请求发送和响应的日志，便于跟踪和调试。
- **异常处理**：对HTTP错误、请求错误和其他未预期错误进行了全面处理，确保脚本在面对各种异常情况时依然能够稳健运行。
- **并发限制**
1. **信号量 `Semaphore`**：
   - 使用 `asyncio.Semaphore` 来限制并发任务的数量。`Semaphore` 控制了同时执行的任务数量，每个任务在执行前必须从信号量中获取一个许可 (`async with semaphore:`)。
   - 当达到最大并发数 `MAX_CONCURRENT_REQUESTS` 时，其他任务必须等待，直到有许可释放。
2. **修改 `send_request` 函数**：
   - 在 `send_request` 函数中添加了 `semaphore` 参数，函数内部使用 `async with semaphore:` 语句来确保同时最多只有 `MAX_CONCURRENT_REQUESTS` 个任务在运行。
3. **`MAX_CONCURRENT_REQUESTS` 设置**：
   - `MAX_CONCURRENT_REQUESTS = 5` 设置了最大并发任务数量为5。你可以根据需要调整此值。


文件写入部分
1. **新增写入函数 `write_response_to_file`**：
   - 这个异步函数用于将每个成功响应的数据追加写入到 `api_response.txt` 文件中。
   - 使用了 `aiofiles` 来异步写入文件，保证在写入过程中不会阻塞其他异步操作。

2. **在 `send_request` 函数中添加写入操作**：
   - 当请求成功时，会调用 `write_response_to_file` 函数，将响应数据写入文件，然后跳出重试循环。

3. **文件初始化**：
   - 在 `main` 函数中启动时，先清空 `api_response.txt` 文件的内容，确保每次运行脚本时不会保留之前的数据。
"""

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置API的URL
API_URL = 'http://localhost:8000/process_request/'

# 设置最大并发数
MAX_CONCURRENT_REQUESTS = 8
# 设置连接超时时间和总超时时间
CONNECTION_TIMEOUT = 30.0
# 设置连接超时数
TOTAL_TIMEOUT = 5.0

# 从 query.txt 文件中读取测试数据
async def load_test_data(file_path):
    test_data = []
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        async for line in file:
            test_data.append({"content": line.strip()})
    return test_data

# 将所有响应一次性写入文件
async def write_all_responses_to_file(file_path, responses):
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
        for response in responses:
            await file.write(f"{response}\n")

async def send_request(data, semaphore):
    async with semaphore:  # 使用信号量控制并发
        async with httpx.AsyncClient(timeout=httpx.Timeout(CONNECTION_TIMEOUT, connect=TOTAL_TIMEOUT)) as client:  # 增加超时时间
            for attempt in range(3):  # 重试机制，最多尝试3次
                try:
                    logger.info(f"Sending request with data: {data}")
                    response = await client.post(API_URL, json=data)
                    response.raise_for_status()
                    response_data = response.json()
                    logger.info(f"Response: {response_data}")
                    return response_data  # 成功后返回响应数据
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                    if attempt < 2:
                        await asyncio.sleep(2)  # 重试前等待一段时间
                except httpx.RequestError as e:
                    logger.error(f"Request error: {e}")
                    if attempt < 2:
                        await asyncio.sleep(2)  # 重试前等待一段时间
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    if attempt < 2:
                        await asyncio.sleep(2)  # 重试前等待一段时间
    return None  # 如果所有尝试都失败，返回None


async def main():
    # 记录开始时间
    start_time = time.time()

    # 加载测试数据
    test_data = await load_test_data('query.txt')

    # 创建信号量
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    # 并发请求，收集所有响应
    tasks = [send_request(data, semaphore) for data in test_data]
    responses = await asyncio.gather(*tasks)

    # 过滤掉失败的请求
    successful_responses = [resp for resp in responses if resp is not None]

    # 将所有成功的响应一次性写入文件
    await write_all_responses_to_file('api_response.txt', successful_responses)

    # 记录结束时间并计算总耗时
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total run time: {total_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())


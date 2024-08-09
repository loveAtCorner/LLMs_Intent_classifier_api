import asyncio
import httpx
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置API的URL
# API_URL = 'http://20.20.137.59:8000/process_request/'
API_URL = 'http://localhost:8000/process_request/'
# API_URL = 'http://0.0.0.0:8000/process_request/'

# 定义测试数据
test_data = [
    {"content": "帮我找到杭州亚信科技有限公司"},
    {"content": "杭州亚信科技有限公司有几条宽带？"},
    {"content": "如何给企业推荐合适的专线产品"},
    {"content": "怎么向客户介绍互联网专线"},
    {"content": "互联网专线资费信息"},
    {"content": "我要下班"}
]

async def send_request(data):
    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0, connect=5.0)) as client:  # 增加超时时间
        for attempt in range(3):  # 重试机制，最多尝试3次
            try:
                logger.info(f"Sending request with data: {data}")
                response = await client.post(API_URL, json=data)
                response.raise_for_status()
                logger.info(f"Response: {response.json()}")
                break  # 成功后退出循环
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

async def main():
    tasks = [send_request(data) for data in test_data]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

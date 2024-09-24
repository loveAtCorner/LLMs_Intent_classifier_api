import requests
import json

import sys
import os
# 将上一级目录加入到 Python 搜索路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 从配置文件 config.py 中导入参数
from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, HEADERS


def chat_completions():
    # 使用配置文件中的 API 基础地址和模型名称
    url = LLM_QUESTION_URL_CONFIG

    # 请求体，使用配置中的模型名称
    params = {
        'model': MODEL_NAME,
        'messages': [{'role': 'user', 'content': '1+100='}]
    }

    # 发送 POST 请求
    r = requests.post(url, json=params, headers=HEADERS)

    return r


if __name__ == '__main__':
    r = chat_completions()
    response = r.json()
    
    # 处理响应，输出聊天结果
    if 'choices' in response and len(response['choices']) > 0:
        content = response['choices'][0]['message']['content']
        print(content)
    else:
        print(f"Error: {response}")

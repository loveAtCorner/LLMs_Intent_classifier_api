import requests

# 设置API的URL
url = 'http://localhost:8000/process_request/'
# url = 'http://0.0.0.0:8000/process_request/'

# 定义请求数据
data = {
        "content": "请查找关于小米“智能家居”的招投标政策，尤其是他们在国内市场上的投标流程和技术要求，想了解他们是否计划进入国际市场。"
}

# 发送POST请求
response = requests.post(url, json=data)

# 打印响应
print("状态码:", response.status_code)
print("响应体:", response.json())

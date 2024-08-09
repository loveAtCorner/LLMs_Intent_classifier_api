import requests

# 设置API的URL
# url = 'http://20.20.137.59:8000/process_request/'
url = 'http://localhost:8000/process_request/'
# url = 'http://0.0.0.0:8000/process_request/'

# 定义请求数据
data = {
        "content": "如何给企业推荐合适的专线产品"
}

# 发送POST请求
response = requests.post(url, json=data)

# 打印响应
print("状态码:", response.status_code)
print("响应体:", response.json())

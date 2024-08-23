import requests

# 设置API的URL
url = 'http://localhost:8000/process_request/'
# url = 'http://0.0.0.0:8000/process_request/'

# 定义请求数据
data = {
        "content": "请告知企业法人相关的路演活动详情"
}

# 发送POST请求
response = requests.post(url, json=data)

# 打印响应
print("状态码:", response.status_code)
print("响应体:", response.json())

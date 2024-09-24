import requests

# 设置API的URL
url = 'http://localhost:8000/process_request/'
# url = 'http://0.0.0.0:8000/process_request/'

# 从文件中读取问题列表
with open('query.txt', 'r', encoding='utf-8') as file:
    questions = file.readlines()

# 准备写入答案的文件
with open('api_response.txt', 'w', encoding='utf-8') as answer_file:
    for question in questions:
        question = question.strip()  # 移除可能的换行符
        # 定义请求数据
        data = {
                "content": question
            }
        
        # 发送POST请求
        response = requests.post(url, json=data)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 获取响应内容
            answer = response.json()
            # 写入文件
            answer_file.write(str(answer) + '\n')
            print("状态码:", response.status_code)
            print("响应体:", response.json())
        else:
            print("响应体:", response.json())

# 打印完成信息
print("所有问题处理完毕，答案已保存")

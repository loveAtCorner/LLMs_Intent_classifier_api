FROM robd003/python3.10:latest
LABEL MAINTAINER="python_env"

WORKDIR /service

COPY ./requirements.txt /service/requirements.txt

# 安装linux常用包
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
RUN apt-get update -y && apt-get install -y vim curl libgl1 libglib2.0-0 && apt-get clean

# 安装python环境
RUN pip install -r requirements.txt && rm -rf `pip cache dir`

# 支持中文字体
ENV LANG C.UTF-8
# 自定义意图识别服务

功能
- 本服务的实现了对自定义的的五类营销意图的识别,包括：查询企业、企业信息问答、专线解决方案（专线推荐）、产品概述、产品信息问答，用户可以根据自己业务需求，修改提示词，实现自定义的意图分类功能
- 支持并发调用

底层依赖
- 底层驱动大模型为vllm框架启动的 qwen1.5-32b-int4 大语言模型


## 服务启动命令(串行服务)

```bash
cd serial_service
```

构建镜像
```bash
docker build -t esop_intent:v1.0 .
```

启动容器
```bash
# 测试
docker run -it --rm --net=host --name=intent_recognition esop_intent:v1.0 python api.py
```

```bash
# 上线
docker run -it --net=host --name=intent_recognition esop_intent:v1.0 /bin/bash
python api.py
cd test 
python test_api.py
```


## 服务启动命令（并发服务）

```bash
cd concurrency_service
```

构建镜像
```bash
docker build -t esop_intent:v1.5 .
```

启动容器
```bash
# 测试
docker run -it --rm --net=host --name=intent_recognition esop_intent:v1.5 python api_asyn.py
```

```bash
# 上线
docker run -it --net=host --name=intent_recognition esop_intent:v1.5 /bin/bash
python api_asyn.py
cd test 
python test_api_asyn.py
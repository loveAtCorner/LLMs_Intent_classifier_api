# config.py

# 服务状态
STATUS = 'test'
# STATUS = 'online'

# API服务配置
API_SERVICE_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000
}

# 大模型调用地址
LLM_QUESTION_URL_CONFIG = 'http://10.1.251.235:3000/v1/chat/completions'
MODEL_NAME = 'qwen1.5-32b-chat-int4'
# LLM_QUESTION_URL_CONFIG= "http://chatmarket.zj.chinamobile.com/qwen/v1/chat/completions"
# MODEL_NAME= "qwen1.5-32b-chat-int4"


# 意图和实体数据目录路径
INTENT_DIRECTORY = "./text_match/intent_classification"
ENTITY_DIRECTORY = "./text_match/entity_type"
 

# 日志参数
LOG_FILENAME = "service.log" # log文件名称，默认为service.log
SIGLE_LOGFILE_SIZE = 50 # 单个日志文件大小，单位是M
BACKUPCOUNT = 5 # 日志文件留存个数，默认为5个
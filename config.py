# config.py

# API服务配置
API_SERVICE_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000
}

# 大模型调用地址
LLM_QUESTION_URL_CONFIG = 'http://20.20.136.251:8001/v1/chat/completions'
MODEL_NAME = 'qwen1.5-32b-chat-int4'

# 请求头配置
HEADERS = {
    'Authorization': 'Bearer a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}

# 意图
INTENTS_ch = [
    "招投标信息查询", 
    "招投标项目概述", 
    "路演活动查询", 
    "路演活动详情", 
    "查询企业参展信息", 
    "企业参展概述", 
    "查看招标公告", 
    "查询中标企业", 
    "路演活动预约", 
    "招投标政策解读", 
    "查询招投标记录", 
    "查询企业法人信息", 
    "招标信息订阅", 
    "路演活动总结", 
    "其他"
]
INTENTS_en = [
    "query_bidding_information", 
    "bidding_project_overview", 
    "query_roadshow_events", 
    "roadshow_event_details", 
    "query_enterprise_exhibition_information", 
    "enterprise_exhibition_overview", 
    "view_bidding_announcement", 
    "query_winning_enterprises", 
    "roadshow_event_booking", 
    "bidding_policy_interpretation", 
    "query_bidding_records", 
    "query_enterprise_legal_person_information", 
    "bidding_information_subscription", 
    "roadshow_event_summary", 
    "others"
]

# 实体
ENTITYS_ch = ["企业名称", "企业法人"]
ENTITYS_en = ["enterprise_name", "enterprise_legal_person"]


# 意图和实体的对应关系
INTENTS_ENTITYS_MAPPER = {
"招投标信息查询": "企业名称",
"招投标项目概述": "企业法人",
"路演活动查询": "企业名称",
"路演活动详情": "企业法人",
"查询企业参展信息": "企业名称",
"企业参展概述": "企业法人",
"查看招标公告": "企业名称",
"查询中标企业": "企业法人",
"路演活动预约": None,
"招投标政策解读": None,
"查询招投标记录": "企业名称",
"查询企业法人信息": "企业法人",
"招标信息订阅": None,
"路演活动总结": None,
"其他": None,
}


# 意图和实体规则目录路径
INTENT_REGEXP_DIRECTORY = "./text_match/intent_classification"
ENTITY_REGEXP_DIRECTORY = "./text_match/entity_type"


# 意图和实体提示词目录路径
NUM_OF_INTENT = 1
INTENT_SYSTEM_PROMPT = "./prompt/classifier/system_prompt_classifier.txt"
INTENT_USER_PROMPT = "./prompt/classifier/user_prompt_classifier.txt"

NUM_OF_ENTITY = 3
ENTITY_PROMPTS = {
    "企业名称": {
        "system_prompt": "./prompt/entity/system_prompt_entity_1.txt",
        "user_prompt": "./prompt/entity/user_prompt_entity_1.txt"
    },
    "企业法人": {
        "system_prompt": "./prompt/entity/system_prompt_entity_2.txt",
        "user_prompt": "./prompt/entity/user_prompt_entity_2.txt"
    },
    "可添加一": {
        "system_prompt": "./prompt/entity/system_prompt_entity_3.txt",
        "user_prompt": "./prompt/entity/user_prompt_entity_3.txt"
    }
}

# 日志参数
LOG_FILENAME = "service.log" # log文件名称，默认为service.log
SIGLE_LOGFILE_SIZE = 50 # 单个日志文件大小，单位是M
BACKUPCOUNT = 5 # 日志文件留存个数，默认为5个

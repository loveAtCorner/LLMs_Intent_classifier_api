# -- coding: utf-8 --
import logging
from logging.handlers import RotatingFileHandler
from config import *

"""
创建logger
"""
# 使用 logging.getLogger() 创建一个日志记录器（logger）
logger = logging.getLogger()
# 设置日志级别为 INFO
logger.setLevel(logging.INFO)

"""
创建handler
"""
# 定义日志文件的路径和名称
name = LOG_FILENAME
log_name = './logs/' + name
print('log_name :', log_name)
logfile = log_name

# 创建一个处理器，允许日志文件达到一定大小后自动“轮转”，并设置文件编码为 UTF-8
fh = RotatingFileHandler(logfile, maxBytes=SIGLE_LOGFILE_SIZE*1024*1024, backupCount=BACKUPCOUNT, encoding='utf-8')

# 设置处理器的日志级别为 INFO
fh.setLevel(logging.INFO)

"""
定义handler的输出格式
"""
# 定义日志的格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# 将这个格式应用于之前创建的文件处理器
fh.setFormatter(formatter)

"""
将Handler添加到Logger
"""
# 将文件处理器添加到 logger
logger.addHandler(fh)

# 测试命令
logger.info('START OK !!!')

import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
import sys
from sys import stdout, stderr, exit



WORK_DIR = Path(__package__).absolute()
PARENT_DIR = WORK_DIR.parent

# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

LOG_FILE = PARENT_DIR / 'last_run.log'
LOG_FILE = WORK_DIR / 'last_run.log'
# LOG_FORMAT = "[%(levelname)s] %(asctime)s %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
# LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
#  LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
#  FORMATTER: logging.Formatter = logging.Formatter(LOG_FORMAT)


# 创建一个自定义的日志格式
class CustomFormatter(logging.Formatter):
  def format(self, record):
    # 获取调用栈中的前一个帧
    caller_frame = sys._getframe(2)  # 获取上级调用的帧
    #  caller_function = caller_frame.f_code.co_name  # 获取前一个函数名
    #  record.funcName = caller_function  # 修改 LogRecord 的 funcName
    record.funcName = caller_frame.f_code.co_name
    record.lineno = caller_frame.f_lineno
    return super().format(record)

formatter = CustomFormatter("%(asctime)s [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s")
logging.Formatter = formatter


LOGGER = logging.getLogger()
logger=LOGGER

debug = False
debug = True

if debug:
  #  handler = logging.StreamHandler()
  #  handler.setFormatter(formatter)
  #  logger.addHandler(handler)
  logging.basicConfig()
  LOGGER.setLevel(logging.INFO)
  OUT = None
  ERR = None

elif False:
  logging.basicConfig(format=LOG_FORMAT)
  LOGGER.setLevel(logging.INFO)
  OUT = None
  ERR = None


elif False:
  # https://docs.python.org/zh-cn/3/library/logging.html#logging.basicConfig
  logging.basicConfig(format=LOG_FORMAT)
  LOGGER.setLevel(logging.INFO)
  OUT = None
  ERR = None

  #  OUT = logging.StreamHandler(stdout)
  #  OUT.setFormatter(FORMATTER)
  #  OUT.setLevel(logging.INFO)
  #  #  OUT.setLevel(logging.WARNING)
  #  OUT.addFilter(NoParsingFilter())
  #
  #  LOGGER.addHandler(OUT)
elif False:
  logging.basicConfig(filename=str(LOG_FILE), filemode='w', format=LOG_FORMAT)

  handler = TimedRotatingFileHandler(LOG_FILE, when="d", interval=1, backupCount=3)
  handler.setFormatter(FORMATTER)
  #  handler.setLevel(logging.ERROR)
  handler.setLevel(logging.WARNING)
  LOGGER.addHandler(handler)
  del handler

  OUT = logging.StreamHandler(stdout)
  OUT.setFormatter(FORMATTER)
  OUT.setLevel(logging.INFO)
  #  OUT.setLevel(logging.WARNING)
  LOGGER.addHandler(OUT)

  ERR = logging.StreamHandler(stderr)
  ERR.setFormatter(FORMATTER)
  #  ERR.setLevel(logging.WARNING)
  ERR.setLevel(logging.ERROR)
  LOGGER.addHandler(ERR)

  # LOGGER.setLevel(logging.DEBUG)
  LOGGER.setLevel(logging.WARNING)
#  LOGGER.setLevel(logging.ERROR)


#  import pyrogram
#  from pyrogram import enums
#
#  from . import config
#  CONFIG = config.CONFIG

import os
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

HOME = os.environ.get("HOME")


#  def get_my_key(key, path=f"{HOME}/.ssh/private_keys.txt"):
def get_my_key(key, path=f"{HOME}/vps/private_keys.txt"):
  # key value
  # key value
  # key value
  path2 = "private_keys.txt"
  if os.path.isfile(path2):
    path = path2
  with open(path) as f:
    while True:
      line = f.readline()
      if line:
        if ' ' in line and line.split(' ', 1)[0] == key:
          return line.split(' ', 1)[1].rstrip('\n')
      else:
        raise ValueError(f"没找到key: {key}")
  LOGGER.error("wtf", exc_info=True)
  #  return None;
  exit(1)


#  exit(0)
# __ALL__ = ["WORK_DIR", "PARENT_DIR", "CMD", "LOGGER", "debug", "OUT", "ERR", "asyncio", "config", "UB", "loop", "MY_NAME", "NB", "BOT_ID", "BOT_NAME", "UB2_ID"]


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
else:
    print('{} 运行'.format(__file__))
    print('{} package 初始化'.format(__name__))

import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from sys import stdout, stderr

import sys
import asyncio

from telethon import TelegramClient


from .utils.tools import get_my_key


WORK_DIR = Path(__package__).absolute()
PARENT_DIR = WORK_DIR.parent

# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

LOG_FILE = PARENT_DIR / 'last_run.log'
# LOG_FORMAT = "[%(levelname)s] %(asctime)s %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
# LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
FORMATTER: logging.Formatter = logging.Formatter(LOG_FORMAT)

LOGGER = logging.getLogger()

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
        debug = True
    elif sys.argv[1] == "test":
        debug = True
    else:
        debug = False

if debug:
    logging.basicConfig(format=LOG_FORMAT)
    LOGGER.setLevel(logging.INFO)
    OUT = None
    ERR = None
else:
    logging.basicConfig(filename=str(LOG_FILE),
                        filemode='w',
                        format=LOG_FORMAT)

    handler = TimedRotatingFileHandler(LOG_FILE,
                                       when="d",
                                       interval=1,
                                       backupCount=3)
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


api_id = int(get_my_key("TELEGRAM_API_ID"))
api_hash = get_my_key("TELEGRAM_API_HASH")

bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
BOT_ID = int(bot_token.split(':', 1)[0])
bot_hash = bot_token.split(':', 1)[1]

MY_ID = int(get_my_key("TELEGRAM_MY_ID"))

# UB = TelegramClient('/home/liqsliu/.ssh/telethon_for_get_msg.session', api_id, api_hash)



# UB = TelegramClient('/home/liqsliu/.ssh/telethon_session_name.session', api_id, api_hash)
UB = TelegramClient(None, api_id, api_hash)
#UB.session.set_dc(2, '149.154.167.40', 80)
UB.session.set_dc(2, '149.154.167.40', 443)
UB.start(phone='9996620512', code_callback=lambda: '22222')

UB2 = UB
# UB2 = TelegramClient('/home/liqsliu/.ssh/telethon_ub2.session', api_id, api_hash)

NB = UB
# NB = TelegramClient('/home/liqsliu/.ssh/telethon_bot.session', api_id, api_hash).start(bot_token=bot_token)

del api_id
del api_hash
del bot_token
del bot_hash



# __ALL__ = [
#    "LOOP", "LOGGER", "OUT", "ERR", "debug", "UB", "NB", "MY_ID", "BOT_ID",
#    "CONFIG", "MY_NAME", "BOT_MANE"
# ]




print("init ok")

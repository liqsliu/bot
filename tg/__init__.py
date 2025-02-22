import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from sys import stdout, stderr



WORK_DIR = Path(__package__).absolute()
PARENT_DIR = WORK_DIR.parent

# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

LOG_FILE = PARENT_DIR / 'last_run.log'
LOG_FILE = WORK_DIR / 'last_run.log'
# LOG_FORMAT = "[%(levelname)s] %(asctime)s %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
# LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
FORMATTER: logging.Formatter = logging.Formatter(LOG_FORMAT)

LOGGER = logging.getLogger()

debug = False
#debug = True


if debug:
    logging.basicConfig(format=LOG_FORMAT)
    LOGGER.setLevel(logging.INFO)
    OUT = None
    ERR = None
else:
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




import asyncio
LOOP = asyncio.get_event_loop()

import pyrogram
from pyrogram import enums

from . import config
CONFIG = config.CONFIG



async def _init():

    UB = config.UB

    global MY_NAME, MY_ID
    await UB.start()
    me = await UB.get_me()
    #  UB.set_parse_mode(None)
    UB.set_parse_mode(enums.ParseMode.DISABLED)
#    me = UB.get_me()
    MY_ID = me.id
    print(me.id)
    MY_NAME = me.username
    del me
    if hasattr(config, "NB"):
        global NB, BOT_NAME, BOT_ID
        NB = config.NB
        await NB.start()
        bot = await NB.get_me()
        NB.set_parse_mode(enums.ParseMode.DISABLED)
        print(bot.id)
        BOT_NAME = bot.username
        BOT_ID = bot.id
        del bot
        if hasattr(config, "NB2"):
            global NB2, BOT2_NAME, BOT2_ID
            NB2 = config.NB2
            await NB2.start()
            bot = await NB2.get_me()
            NB2.set_parse_mode(enums.ParseMode.DISABLED)
            print(bot.id)
            BOT2_NAME = bot.username
            BOT2_ID = bot.id
            del bot
    if hasattr(config, "UB2"):
        global UB2, UB2_ID
        UB2 = config.UB2
        await UB2.start()
        bot = await UB2.get_me()
        UB2.set_parse_mode(enums.ParseMode.DISABLED)
        print(bot.id)
        UB2_ID = bot.id
        del bot


#LOOP.run_until_complete(init())
if LOOP.is_running():
    LOGGER.error("loop running...")
else:
    LOGGER.error("loop stoped...")

if LOOP.is_closed():
    LOGGER.error("loop closed, this may be a error")

# __ALL__ = ["WORK_DIR", "PARENT_DIR", "CMD", "LOGGER", "debug", "OUT", "ERR", "asyncio", "config", "UB", "LOOP", "MY_NAME", "NB", "BOT_ID", "BOT_NAME", "UB2_ID"]

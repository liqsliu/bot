import logging
import os
from .utils import db
from .utils.tools import decode_base64, encode_base64, compress, decompress, load_str, raise_error
from .utils.tools import my_exceptions_handler as exceptions_handler


# basedir = os.path.split(os.path.realpath(__file__))[0]
#    path=os.environ.get("tmp")

HOME = os.environ.get("HOME")


def get_my_key(key, path=f"{HOME}/.ssh/private_keys.txt"):
    # key value
    # key value
    # key value
    path2 = "private_keys.txt"
    if os.path.isfile(path2):
        path = path2
    with open(path) as f:
        line = f.readline()
        while line:
            if len(line.split(' ', 1)) == 2 and line.split(' ', 1)[0] == key:
                f.close()
                return line.split(' ', 1)[1].rstrip('\n')
                break
            line = f.readline()
    return None


logger = logging.getLogger(__name__)
mp = logger.info



api_id = int(get_my_key("TELEGRAM_API_ID"))
api_hash = get_my_key("TELEGRAM_API_HASH")


MY_ID = int(get_my_key("TELEGRAM_MY_ID"))

# from telethon import TelegramClient
from pyrogram import Client

session = "pyrogram"

UB = Client(HOME + '/.ssh/' + session + '.session', api_id, api_hash)
#  UB2 = Client(HOME + '/.ssh/' + session + '_ub2.session', api_id, api_hash)

#  bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
#  BOT_ID = int(bot_token.split(':', 1)[0])
#  bot_hash = bot_token.split(':', 1)[1]
# NB = Client(HOME + '/.ssh/' + session + '_nb.session', api_id, api_hash).start(bot_token=bot_token)
#  NB = Client(HOME + '/.ssh/' + session + '_nb.session', api_id, api_hash, bot_token=bot_token)
bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIUBOT")
#  NB2 = Client(HOME + '/.ssh/' + session + '_nb2.session', api_id, api_hash, bot_token=bot_token)
NB = Client(HOME + '/.ssh/' + session + '_nb2.session', api_id, api_hash, bot_token=bot_token)

del api_id
del api_hash
del bot_token
del session


myid = int(get_my_key("TELEGRAM_MY_ID"))
cid_disk = int(get_my_key("TELEGRAM_GROUP_DISK"))

cid_ipfsrss = int(get_my_key("TELEGRAM_GROUP_IPFSRSS"))
cid_tw = int(get_my_key("TELEGRAM_GROUP_TW"))
cid_wtfipfs = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

cid_btrss = int(get_my_key("TELEGRAM_GROUP_BTRSS"))
cid_fw = int(get_my_key("TELEGRAM_GROUP_FW"))


cid_test = int(get_my_key("TELEGRAM_GROUP_TEST"))


config_saved_msgid = 2817682
config_save_buffer = None

TG_BOT_ID_FOR_MT = 420849111
TG_BOT_ID_FOR_MT = -1001502458909



news_list = []
CONFIG = []

#    "gateway5":[cid_ipfsrss],
MT_GATEWAY_LIST = {
    "gateway5": news_list,
    "gateway11": [cid_wtfipfs]
}

MT_GATEWAY_LIST_for_tg = {}


def update_mt_list():
    global MT_GATEWAY_LIST_for_tg

    tmp = {}
    #  MT_GATEWAY_LIST_for_tg.clear()
    for i in MT_GATEWAY_LIST:
        #  MT_GATEWAY_LIST_for_tg.update({MT_GATEWAY_LIST[i][0]: i})
        for j in MT_GATEWAY_LIST[i]:
            tmp.update({j: i})
    if tmp != MT_GATEWAY_LIST_for_tg:
        MT_GATEWAY_LIST_for_tg.clear()
        MT_GATEWAY_LIST_for_tg.update(tmp)


async def load_config():
    global config_save_buffer
    config_save_buffer = []

    try:
        text = []
        num_of_config = 4
        for i in range(num_of_config):
            tmp = db.get(i+1, "config")
            if tmp["text"] is None:
                print(text)
                raise_error("fail to load config")
            text.append(tmp["text"])
        if text:
            tmp = []
            for i in text:
                tmp.append(load_str(i))
    except Exception as e:
        logger.exception(f"can not load config: {e}")
        raise_error("fail to load config")
        return
    if tmp and len(tmp) == num_of_config:

        auto_forward_list = tmp[0]
        auto_msg_list = tmp[1]
        feed_list = tmp[2]
        global news_list

        if not feed_list:
            raise_error("fail to load config")
            raise ValueError

        if len(tmp) > 3:
            news_list.extend(tmp[3])
            tmp.pop(3)


#      news_list=tmp[3]
        tmp.append(news_list)

        global CONFIG
        CONFIG.extend(tmp)
        # db.save(CONFIG, "config")
        # db.save(list(repr(x) for x in CONFIG), "config")
        db.save(list(str(x) for x in CONFIG), "config")
        config_save_buffer = str(CONFIG).replace(" ", "").strip()
        update_mt_list()
        #    config_save_buffer=msg.raw_text

        await NB.send_message(MY_ID, "config loaded")
        return

    else:
        await UB.send_message(MY_ID, "load config fail: no msg")
        raise_error("fail to load config")
        raise ValueError


@exceptions_handler
async def save_config():
    global config_save_buffer
    global CONFIG
    logger.debug("save config?")
    update_mt_list()
    if config_save_buffer != str(CONFIG).replace(" ", "").strip():
        logger.info("diff")
        db.save(list(str(x) for x in CONFIG), "config")
    else:
        logger.debug("same")
        pass



#  SH_PATH = get_sh_path()

from .utils.tools import SH_PATH, DOMAIN


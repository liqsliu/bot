import logging

logger = logging.getLogger(__name__)
mp = logger.info

from .tools import get_my_key
from .tools import decode_base64, encode_base64, compress, decompress, load_str, my_exceptions_handler

config_saved_msgid = 2817682
config_save_buffer = None

TG_BOT_ID_FOR_MT = 420849111


myid = int(get_my_key("TELEGRAM_MY_ID"))

cid_ipfsrss = int(get_my_key("TELEGRAM_GROUP_IPFSRSS"))
cid_tw = int(get_my_key("TELEGRAM_GROUP_TW"))
cid_wtfipfs = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

cid_btrss = int(get_my_key("TELEGRAM_GROUP_BTRSS"))
cid_fw = int(get_my_key("TELEGRAM_GROUP_FW"))

#news_list=[-1001788173808, -1001771739613]
news_list = []

MT_GATEWAY_LIST = {
#    "gateway5":[cid_ipfsrss],
    "gateway5": news_list,
#    "gateway2": [-1001137152439],
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


CONFIG = []

#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from .. import *


#from ..bot import *
async def load_config():
    global config_save_buffer
    config_save_buffer = []

    auto_forward_list = {}
    auto_msg_list = {}
    feed_list = {}
    global news_list

    try:
        chat = await UB.get_input_entity(MY_ID)
        if chat:
            msg = await UB.get_messages(chat, ids=config_saved_msgid)
    except:
        #    info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
        logger.exception("can not load config")
        pass
        return
    if chat and msg and msg.raw_text:

        if msg.raw_text[0:2] == "[{":
            config_save_buffer = msg.raw_text
        else:
            config_save_buffer = decompress(decode_base64(
                msg.raw_text)).decode()

        tmp = load_str(config_save_buffer)
        auto_forward_list = tmp[0]
        auto_msg_list = tmp[1]
        feed_list = tmp[2]

        if len(tmp) > 3:
            news_list.extend(tmp[3])
            tmp.pop(3)


#      news_list=tmp[3]
        tmp.append(news_list)

        global CONFIG
        CONFIG.extend(tmp)
        config_save_buffer = str(CONFIG).replace(" ", "").strip()
        update_mt_list()
        #    config_save_buffer=msg.raw_text

        await msg.reply("loaded, size: " + str(len(msg.raw_text)) +
                        " < %s" % len(config_save_buffer))
        logger.info(msg)
        return
        if len(config_save_buffer) > 4096:
            await NB.send_message(MY_ID, "config too long")
        else:
            await NB.send_message(MY_ID, str(CONFIG))

    else:
        await UB.send_message(MY_ID, "load config fail: no msg")


@my_exceptions_handler
async def save_config():
    global config_save_buffer
    global CONFIG
    logger.debug("save config?")
    update_mt_list()
    #  if config_save_buffer != str([auto_forward_list,auto_msg_list,feed_list]).replace(" ", "").strip():
    if config_save_buffer != str(CONFIG).replace(" ", "").strip():
        logger.info("diff")
        try:
            chat = await UB.get_input_entity(MY_ID)
            msg = await UB.get_messages(chat, ids=config_saved_msgid)
        except:
            #info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
            #      logger.exception(info)
            logger.exception("can not get msg")
            pass
            return
        if chat and msg:
            #      config_save_buffer=[auto_forward_list,auto_msg_list,feed_list]
            #      config_save_buffer = str([auto_forward_list,auto_msg_list,feed_list]).replace(" ", "").strip()
            config_save_buffer = str(CONFIG).replace(" ", "").strip()
            tmp = encode_base64(compress(config_save_buffer.encode()))
            if msg.raw_text != tmp:
                logger.info("diff!")
                #        await msg.edit(config_save_buffer)
                #        await msg.edit( encode_base64(zlib.compress(config_save_buffer.encode())) )
                if len(tmp) < 4096:
                    try:
                        await msg.edit(tmp)
                    except:
                        #            info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
                        #            logger.exception(info)
                        logger.exception("can not edit msg")
                        return
                    return True
                else:
                    await NB.send_message(myid,
                                          "E: fail to save config, too long")
        else:
            await UB.send_message(
                myid,
                str([auto_forward_list, auto_msg_list,
                     feed_list]).replace(" ", "").strip())
            await UB.send_message(
                myid, "E: fail to save config, can't find the msg or chat")
    else:
        logger.debug("same")
        pass


#    await userbot.send_message(myid, "not change")

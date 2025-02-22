from . import *  # noqa: F403
import logging

from functools import wraps

import asyncio
import subprocess
from subprocess import Popen, PIPE
import traceback

import time
import re
import functools
import io
import os
import mimetypes

from urllib.parse import urlsplit, unquote,urlparse





import pyrogram

from pyrogram import enums
from pyrogram.raw import types

from pyrogram import StopPropagation, ContinuePropagation
# from pyrogram.errors import *
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions import bad_request_400, flood_420

from pyrogram.types import User, Chat
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
InlineKeyboardButton, BotCommand, InputMediaPhoto, InputMediaVideo,InputMediaDocument,InputMediaAudio)
from pyrogram.types import MessageEntity



from .config import cid_wtfipfs, cid_ipfsrss, cid_tw, cid_ipfsrss, cid_btrss, cid_fw, CONFIG, cid_test, TG_BOT_ID_FOR_MT
from .config import MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg, TG_BOT_ID_FOR_MT
from .config import cid_wtfipfs, cid_ipfsrss, cid_tw, TG_BOT_ID_FOR_MT
from .config import SH_PATH, DOMAIN

from .utils.tools import ennum, denum, denum_auto, tw_re, pic_re, url_only_re, my_host_re, url_re, url_md_re, url1_md_re, url2_md_re, pic_md_re, text_has_md, mdraw, bot_msg_re, bot_msg_qt_re, discord_id_end_re, my_jaccard, pastebin, ipfs_add, http, pastebin, ipfs_add, pb_0x0, transfer, file_io, catbox, num2byte, byte2num, catbox, my_traceback, format_byte

# from .utils.tools import current_thread_is_main
from .utils.tools import put
from .utils.tools import my_raise
from .utils.mt import mt_send
from .utils import db


from .utils.tools import my_exceptions_handler
# from .utils.tools import my_exceptions_handler as decorator
from .utils.tools import file_read

# from .telegram import get_sender_id


MSG_QUEUE = asyncio.Queue(512)

MAX_MSG_LEN = 4096
MAX_MSG_LINE = 64
DOWNLOAD_PATH = "/var/www/dav/tmp"
#  MY_DOMAIN = "liuu.tk"

GID = cid_test  # private group, for saving some content

LOCK = asyncio.Event()  # floodwait
LOCK.set()


logger = logging.getLogger(__name__)
mp = logger.info
auto_forward_list = CONFIG[0]
auto_msg_list = CONFIG[1]
feed_list = CONFIG[2]



MSG_TYPE_IN_QUEUE = 0
MSG_TYPE_IN_QUEUE_MT = 1
MSG_TYPE_IN_QUEUE_MT_DE = 1
MSG_TYPE_IN_QUEUE_RSS = 2
MSG_TYPE_IN_QUEUE_TW = 3

MSG_TYPE_IN_QUEUE_ME = 5

MSG_TYPE_IN_QUEUE_CMD = 6
MSG_TYPE_IN_QUEUE_CMD_RES = 6


# https://github.com/yshalsager/ebook-converter-bot/blob/master/ebook_converter_bot/utils/telegram.py


from random import uniform


def tg_exceptions_handler(func):

    if not asyncio.iscoroutinefunction(func):
        from .utils.tools import raise_error
        raise_error("the fun is not async: " + func.__name__)
        return

    from .utils.tools import get_ex

    # @my_exceptions_handler
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            ex = get_ex(func, args, kwargs)
            await LOCK.wait()
            return await func(*args, **kwargs)
        except (FloodWait, flood_420.FloodWait) as e:
            if LOCK.is_set():
                LOCK.clear()
                #  await asyncio.sleep(e.seconds+uniform(0.5, 1.0))
                await asyncio.sleep(e.value+uniform(0.5, 1.0))
                LOCK.set()
            else:
                LOCK.clear()
                await asyncio.sleep(e.value*2+uniform(0.5, 1.0)+5)
                LOCK.set()

            my_traceback(e, ex)
            await asyncio.sleep(5)
            #  return tg_exceptions_handler(await func(*args, **kwargs))
            return await tg_exceptions_handler(func)(*args, **kwargs)
        # except QueryIdInvalidError:
            # info = "inline answer is too slow"
            # logger.warning(info)
            # put(info)
        except ContinuePropagation:
            raise
        except StopPropagation as e:
            logger.debug("stop a event")
            raise
        except bad_request_400.MediaInvalid as e:
            #  my_raise(e, func, *args, **kwargs)
            my_raise(e, ex)
            await asyncio.sleep(2)
            put("retry...")
            await asyncio.sleep(5)
            #  retry one time
            await LOCK.wait()
            #  return my_exceptions_handler(await func(*args, **kwargs))
            return await my_exceptions_handler(func)(*args, **kwargs)
        except TimeoutError as e:
            logger.error(e, exc_info=True)
            #  await NB.send_message(MY_ID, str(e))
            my_raise(e, ex)
        # except (ChannelPrivateError, ChatWriteForbiddenError,
                # UserIsBlockedError, InterdcCallErrorError,
                # MessageNotModifiedError, InputUserDeactivatedError,
                # MessageIdInvalidError):
            # info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
            # print(info)
            # await NB.send_message(MY_ID, info)
            # await asyncio.sleep(3)
        # except SlowModeWaitError as error:
            # await asyncio.sleep(error.seconds)
            # await asyncio.sleep(3)
            # return tg_exceptions_handler(await func(*args, **kwargs))
        # except FloodWaitError as error:
            # await asyncio.sleep(error.seconds+uniform(0.5, 1.0))

            # return tg_exceptions_handler(await func(*args, **kwargs))
        except Exception as e:
            # logger.error(e)
            # return my_exceptions_handler(await func(*args, **kwargs))
            # return await exception_when_run(func.__name__, *args, **kwargs)
#            return await _()
            #  @my_exceptions_handler
            #  async def from_handler(*args, **kwargs):
            #      raise e
            #  if func.__name__ == "exception_from":
            #      return await from_handler(*args, **kwargs)
            #  else:
            #      return await from_handler(func, *args, **kwargs)
            #  my_raise(e, func, *args, **kwargs)
            my_raise(e, ex)

    return wrapper



def disable_async(func):

    lock = asyncio.Lock()

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with lock:
            return await func(*args, **kwargs)
    return wrapper


@tg_exceptions_handler
async def cmd_answer_for_my_group(text, msg):
    if text is None:
        return
    try:
        chat_id = cid_wtfipfs
        client = UB

        if await UB.set_send_as_chat(chat_id, TG_BOT_ID_FOR_MT):
            name_re = await get_name_for_mt(msg)
            #  if text.splitlines()[0] == '...':
            #      return
            text = f"C bot: {name_re}: {text}"
            #  res = await UB.send_message(chat_id, text, parse_mode=parse_mode)
            res = await UB.send_message(chat_id, text, parse_mode=enums.ParseMode.DISABLED)
            msg_for_mt = await parse_msg_for_mt(client, res)
            if msg_for_mt:
                await mt_send(msg_for_mt[0], msg_for_mt[1], msg_for_mt[2], msg_for_mt[3])
            return res
    except Exception as e:
        raise
    finally:
        if not await UB.set_send_as_chat(chat_id, MY_ID):
            logger.error("fail to recover")
            put("fail to recover")


@tg_exceptions_handler
#  async def cmd_answer(text, client=NB, event=None, msg=None, parse_mode=None):
async def cmd_answer(text, client=NB, event=None, msg=None, parse_mode=enums.ParseMode.DISABLED):
    logger.info(text)
    if not msg:
        if event:
            msg = event
    if text:
        #  if type(text) is not str:
        if not isinstance(text, str):
            logger.warning(f"{type(text)} is not str")
            text = str(text)
        else:
            text = str(text)
    else:
        text = "None"
    text = text.strip()
    #  if len(text) > MAX_MSG_LEN or len(text.splitlines()) > MAX_MSG_LINE:
    if len(text) > MAX_MSG_LEN:
        if len(text) > 3 * MAX_MSG_LEN:
            logger.warning("too long, use link")
            tmp = await cmd_answer("...", client, msg=msg, parse_mode=parse_mode)
            text = await text2link(text)
            if tmp.id != msg.id:
                await tmp.delete()
        else:
            logger.warning("need split: {}".format(len(text)))
            logger.warning("split long msg: {}".format(text[0:MAX_MSG_LINE]))
            text_splited = []
            #  k = len(text) // MAX_MSG_LEN + 1
            #  k = len(text) // k
            i = 0
            #  while i * k < len(text):
                #  text_splited.append(text[i * k:i * k + k])
                #  i += 1
            while i < len(text):
                text_splited.append(text[i:i+MAX_MSG_LEN])
                i += MAX_MSG_LEN
            logger.warning("splited to: {}".format(len(text_splited)))
            for i in text_splited:
                msg = await cmd_answer(i, client, msg, parse_mode=parse_mode)
                await asyncio.sleep(0.3)
            return msg
    if client and msg:
        chat_id = get_chat_id(msg)
        sender = get_sender(msg)
        res = None
        if is_my_group(msg):
            return await cmd_answer_for_my_group(text, msg)
        try:
            if text == msg.text:
                return msg
            #  if msg.outgoing and (chat_id != sender.id or client.bot_token is not None):
            if msg.outgoing and (client != UB or chat_id != sender.id ):
                try:
                    if msg.edit_date:
                        d = msg.edit_date
                        # w = d.today().timestamp() - d.timestamp()
                        w = time.time() - d
                        if w < 1.5:
                            res = await client.send_message(chat_id, text, parse_mode=parse_mode)
                            return res
                        else:
                            res = await msg.edit(text, parse_mode=parse_mode)
                            return res
                    elif hasattr(sender, "is_bot") and not sender.is_bot and msg.text and msg.text.startswith("."):
                        res = await msg.edit(text, parse_mode=parse_mode)
                        return res
                    else:
                        d = msg.date.timestamp()
                        w = time.time() - d
                        if w > 1.9:
                            res = await msg.edit(text, parse_mode=parse_mode)
                            return res
                    res = await client.send_message(chat_id, text, parse_mode=parse_mode)
                    return res
                    #  if sender.is_bot:
                    #      return await client.send_message(chat_id, text, parse_mode=parse_mode)
                except Exception as e:
                    logger.error(e)
                    raise
            else:
                if is_private(msg):
                    res = await client.send_message(chat_id, text, parse_mode=parse_mode)
                    return res
                else:
                    res = await msg.reply(text, parse_mode=parse_mode)
                    return res
        except Exception as e:
            logger.warning(e)
            put(e)
        finally:
            pass
            #  if need_recover:
            #      if not await UB.set_send_as_chat(chat_id, MY_ID):
            #          logger.error("fail to recover")
            #      if res is not None and is_my_group(msg):
            #          msg_for_mt = await parse_msg_for_mt(client, res)
            #          if msg_for_mt:
            #              await mt_send(msg_for_mt[0], msg_for_mt[1], msg_for_mt[2], msg_for_mt[3])
    else:
        logger.warning("no source msg, send to admin")
        #  raise ValueError
        return await NB.send_message(MY_ID, text, parse_mode=parse_mode)



def get_id_of_db(tmp):

    id = tmp
    if str(tmp).startswith("-100"):
        if db.existed("chat", tmp) or db.existed("channel", tmp):
            id = tmp
            tmp = 0
        else:
            tmp = int(str(tmp)[4:])
    elif tmp < 0:
        if db.existed("chat", tmp):
            id = tmp
            tmp = 0
        else:
            tmp = -1*tmp

    if tmp > 0:
        if db.existed("user", tmp):
            id = tmp
            tmp = 0
        else:
            tmp = -1*tmp
    if tmp < 0:
        if db.existed("chat", tmp):
            id = tmp
            tmp = 0
        else:
            tmp = int("-100"+str(-1*tmp))
    if tmp < 0:
        if db.existed("chat", tmp) or db.existed("channel", tmp):
            id = tmp
            tmp = 0

    if tmp == 0:
        return id


def get_real_id(peer):
    if type(peer) == int:
        id = peer
        if id < 0:
            # need fix
            if str(id).startswith("-100") and db.existed("channel", id):
                id = str(id)[4:]
                id = int(id)
            elif len(str(id)) == 14 and str(id).startswith("-100"):
                # need fix
                id = str(id)[4:]
                id = int(id)
            else:
                id = id*(-1)
        return id
    #  if hasattr(peer, "type"):
    if isinstance(peer, Chat):
        #  if peer.type == "private":
        if peer.type == enums.ChatType.PRIVATE:
            return peer.id
        #  if peer.type == "bot":
        elif peer.type == enums.ChatType.BOT:
            return peer.id
        #  if peer.type == "group":
        elif peer.type == enums.ChatType.GROUP:
            return peer.id*(-1)
        #  if peer.type == "supergroup":
        elif peer.type == enums.ChatType.SUPERGROUP:
            return int(str(peer.id)[4:])
        #  if peer.type == "channel":
        elif peer.type == enums.ChatType.CHANNEL:
            return int(str(peer.id)[4:])
    elif isinstance(peer, User):
        return peer.id
    if peer is None:
        return
    else:
        return peer.id

def get_chat(message):
    if message.chat:
        return message.chat
    return None

def get_chat_id(message):
    if message.chat:
        return message.chat.id
    return None

def get_sender(message):
    if message.from_user:
        return message.from_user
    if message.sender_chat:
        return message.sender_chat
    return None
    if message.chat:
        return message.chat

def get_sender_id(message):
    sender = get_sender(message)
    if sender is not None:
        return sender.id
    return None


async def get_qt_from_mtmsg(qt_text):
    qt = None
    tg_nick = None
    for line in qt_text.splitlines():
        if line.startswith("> > ") or url_md_re.match(
                line[2:]) or line == "> ----" or url_md_re.match(line[2:]):
            if qt:
                logger.warning("stop to get more qt")
                break
        if line.startswith("> "):
            if tg_nick:
                qt += "\n" + line[2:]
            elif qt is not None:
                qt += "\n" + line[2:]
            else:
                # if ": " in line:
                if qt_text.startswith("> C twitter: "):
                    tg_nick = cid_tw
                    qt = line.split(": ", 1)[1]
                elif qt_text.startswith("> T "):
                    tg_nick = line[4:].split(": ", 1)[0]
                    if line.split(
                            ": ",
                            1)[1].startswith("转自") and ": " in line.split(
                                ": ", 1)[1]:
                        qt = line.split(": ", 2)[2]
                    elif line.split(": ", 1)[1].startswith(
                            "Forwarded from") and ": " in line.split(": ",
                                                                     1)[1]:
                        qt = line.split(": ", 2)[2]
                    else:
                        qt = line.split(": ", 1)[1]
                elif bot_msg_qt_re.match(line):
                    #                    tg_nick = "liqsliu_bot"
                    tg_nick = TG_BOT_ID_FOR_MT
                    qt = line[2:]
                else:
                    qt = line[2:]

        else:
            break

    logger.info("finally qt: {}".format(qt))
    return qt, tg_nick


@tg_exceptions_handler
async def mtmsg2msg(msgd):
    msg = msgd
    mp("get: " + msgd["text"])

    text = msgd["text"]
    name = msgd["username"]
    chat_id = msgd["chat_id"]

    if len(name.splitlines()) > 1:
        qt_text = name
        name = name.splitlines()[-1]
    else:
        qt_text = name

    if qt_text.startswith("> **"):
        qt_text = qt_text.replace("> **", "> ", 1)
        qt_text = qt_text.replace(":**", ":", 1)
        logger.warning("change qt to: {}".format(qt_text))

    if name.startswith("T "):
        logger.debug("ignore msg from telegtam: " + msgd["text"])
        return

    reply_to = None
    #      if text.startswith("> "):
    if qt_text.startswith("> "):
        #        name=msgd["username"]
        #        if text.startswith("> T "):

#        if qt_text.startswith("> T ") and ":" in qt_text:
        if ":" in qt_text:
            #                reply_to=denum_auto(qt_text.split(":", 1)[0])
            if ":" in qt_text:
                tmp = qt_text.split(": ", 1)[0]
            else:
                logger.warning("no ': '")
                tmp = qt_text.split(":", 1)[0]
            reply_to = denum_auto(tmp)
        if reply_to is not None:
            if reply_to == 0:
                logger.info("qt is from rss, need't search")
                reply_to = None
            else:
                logger.info("denum success: {}".format(reply_to))

        else:
            logger.warning("denum fail: {}".format(qt_text))
            reply_to = None
            qt, tg_nick = await get_qt_from_mtmsg(qt_text)
            if qt:
                protocol = name[0]
                reply_to = await get_msg_id_from_text(qt,
                                                      chat_id,
                                                      name=tg_nick,
                                                      protocol=protocol)
                logger.info("finally reply_to msg id: {}".format(reply_to))
                if reply_to:
                    logger.info("get msg id: %s" % reply_to)
        if reply_to:
            if await get_msg(chat_id, reply_to):
                pass
            else:
                logger.warning("replied msg is deleted: {}: {}".format(
                    reply_to, qt_text))
                reply_to = None
        if not reply_to:
            logger.warning("cannot get msg id for reply, use orig qt")
            name = qt_text
            reply_to = None
    else:
        logger.info("not reply, orig qt: %s" % qt_text)

    name = name.splitlines()
    if len(name) > 1:
        name = "\n".join(name[:-1]) + "\n**" + name[-1].rstrip(" ") + "** "
    else:
        name = "**" + name[0].rstrip(" ") + "** "

    text = name + text
    # msg = [0, chat_id, text, {"reply_to":reply_to}]
    # msg = [1, chat_id, text, {"reply_to": reply_to, "parse_mode": "md"}]
    msg = [MSG_TYPE_IN_QUEUE_MT_DE, chat_id, text, {"reply_to_message_id": reply_to, "parse_mode": enums.ParseMode.MARKDOWN}]
    return msg


def get_file_type(url):
    t = mimetypes.guess_type(url, strict=False)[0]
    if t is None:
        return None
    return t.split("/")[0]



async def get_file_id(file, chat_id=cid_test, client=UB):
    msg = await send_file(chat_id, file, client=client)
    if msg:
        file = getattr(msg, msg.media.value)
        if file:
            return file.file_id


async def send_file(chat_id, file, client=UB, caption=None, parse_mode=enums.ParseMode.DISABLED, *args, **kwagrs):
    if type(file) == list:
        if len(file) == 1:
            file = file[0]
        elif len(file) == 0:
            return

    if type(file) == list:
        f = file[0]
        if isinstance(f, str):
            fs = []
            for f in file:
                #  if url_only_re.match(f):
                #      link = await catbox(f)
                #      if link:
                #          put(f"using catbox: {f} => {link}")
                #          f = link

                #  print(f"send a {get_file_type(f)}: {f}")
                #  put(f"send a {get_file_type(f)}: {f}")
                if get_file_type(f) == "image":
                    fid = await get_file_id(f, client=client)
                    if fid:
                        f = fid
                    fs.append(InputMediaPhoto(f))
                elif get_file_type(f) == "video":
                    fid = await get_file_id(f, client=client)
                    if fid:
                        f = fid
                    fs.append(InputMediaVideo(f))
                elif get_file_type(f) == "audio":
                    fid = await get_file_id(f, client=client)
                    if fid:
                        f = fid
                    fs.append(InputMediaAudio(f))
                else:
                    fid = await get_file_id(f, client=client)
                    if fid:
                        f = fid
                    fs.append(InputMediaDocument(f))
            if caption is not None:
                fs[-1].caption = caption
                fs[-1].parse_mode = parse_mode

            try:
                return await client.send_media_group(chat_id, fs)
            except bad_request_400.MediaInvalid as e:
                print(str(e) +"\n\nfiles: "+ repr(fs))
                put(str(e) +"\n\nfiles: "+ repr(fs))
        else:
            put(f"umknown file type, need fix: {type(f)}")
    else:
        f = file
        if isinstance(f, str):
            #  print(f"send a {get_file_type(f)}: {f}")
            #  put(f"send a {get_file_type(f)}: {f}")
            # if f.endswith(".jpg")
            if get_file_type(f) == "image":
                return await client.send_photo(chat_id, f, caption=caption, parse_mode=parse_mode, *args, **kwagrs)
            elif get_file_type(f) == "video":
                return await client.send_video(chat_id, f, caption=caption, parse_mode=parse_mode, *args, **kwagrs)
            elif get_file_type(f) == "audio":
                return await client.send_audio(chat_id, f, caption=caption, parse_mode=parse_mode, *args, **kwagrs)
            else:
                return await client.send_document(chat_id, f, caption=caption, parse_mode=parse_mode, *args, **kwagrs)
        else:
            put(f"umknown file type, need fix: {type(f)}")


@tg_exceptions_handler
async def send_msg_of_queue():
    """msg: [type, chat_id, text, ...]
{
"parse_mode": "md",
"link_preview": False,
"file":None
}

"""
    wait_time = 3
    max_msg_flood = 8

    # for every 3 seconds send a msg for a chat
    locks = {}
    wait = []
    recent = []
    skip = []

    @tg_exceptions_handler
    async def smf(msg, client=None):
        "send, retry when error"
        need_recover = False
        msg = msg.copy()
        entities = []
        #  if msg[2] and msg[0] != 5:
        #      for url in url_re.finditer(msg[2]):
        #          entities.append(MessageEntity(type="url", offset=url.start(), length=url.end()-url.start()))
        tmp=""
        last=0
        #  if msg[2] and msg[0] != 5 and "parse_mode" in msg[3] and msg[3]["parse_mode"] == "md":
        if msg[2] and msg[0] != 5 and "parse_mode" in msg[3] and msg[3]["parse_mode"] == enums.ParseMode.MARKDOWN:
#            if not url_md_re.match(msg[2]) and not url1_md_re.match(msg[2]):
            if not url_md_re.search(msg[2]) and not url1_md_re.search(msg[2]):
                #  print(repr(msg[2]))
                for url in url_re.finditer(msg[2]):
                    if not tmp:
                        tmp = msg[2][0:url.start()]
                    else:
                        tmp += msg[2][last:url.start()]

                    tmp += f"[{url.group()}]({url.group()})"
                    last= url.end()
                    
                if tmp and last != len(msg[2]):
                    tmp += msg[2][last:]

                if tmp:
                    msg[2] = tmp

        if client is None:
            #  if msg[0] == 1 or msg[0] == 6:
            if msg[0] == 1:
                #mt
                client = NB
                if TG_BOT_ID_FOR_MT < 0:
                    if await UB.set_send_as_chat(cid_wtfipfs, TG_BOT_ID_FOR_MT):
                        client = UB
                        need_recover = True

            elif msg[0] == 2:
                # rss
                client = UB
            elif msg[0] == 3:
                # twitter
                client = UB
            elif msg[0] == 5:
                # log for me
                client = NB
            else:
                client = UB

        if "file" in msg[3] and msg[3]["file"] is not None:
            file = msg[3]["file"]
            msg[3].pop("file")
            if "disable_web_page_preview" in msg[3]:
                msg[3].pop("disable_web_page_preview")
            res = await send_file(msg[1], file, client, msg[2], **msg[3])
        elif "link_preview" in msg[3]:
            print("need fix: link_preview")
        else:
            #            await NB.send_message(msg[1], msg[2], **msg[3])
            if "file" in msg[3]:
                msg[3].pop("file")
            res = await client.send_message(msg[1], msg[2], **msg[3], entities=entities)


        if msg[0] == 1:
            #  if not await CMD.run(client, res):
            if not await CMD.check_cmd(client, res, run=True):
                #  text = msg[2]
                text = res.text
                if ': ' in text:
                    cmd = text.split(': ', 1)[1]
                else:
                    cmd = text
                faq = await faq_get(cmd)
                if faq:
                    await cmd_answer_for_my_group(faq, res)
                elif cmd.startswith('.'):
                    #  from .mytask import send2mt
                    #  await send2mt(client, res)
                #  await CMD.run(client, res)
                    msg_for_mt = await parse_msg_for_mt(client, res)
                    if msg_for_mt:
                        #  await mt_send(msg_for_mt[0], msg_for_mt[1], msg_for_mt[2], msg_for_mt[3])
                        if msg_for_mt[2] == "gateway11":
                            msg_for_mt[2] = "gateway1"
                        #for cmd answer
                        if msg_for_mt[1].endswith(": "):
                            msg_for_mt[1] = msg_for_mt[1][:-2]
                        if msg_for_mt[1] != "C bot":
                            asyncio.create_task(send_cmd_to_bash(msg_for_mt))
        elif msg[0] == 2:
            if client == UB:
                await forward_msg(client, res)
        #  elif msg[0] == 6:
        #      try:
        #          from .mytask import send2mt
        #          await send2mt(client, res)
        #      except StopPropagation:
        #          pass
        if need_recover:
            if not await UB.set_send_as_chat(msg[1], MY_ID):
                logger.error("fail to recover")
        return res

    async def sm(msg):
        "check lock then send"
        nonlocal locks
        lock = locks[msg[1]]

        # https://docs.python.org/zh-cn/3/library/asyncio-sync.html
        #    await lock.acquire()
        async with lock:
            await smf(msg)
            logger.debug("wait for read or rest")
            await asyncio.sleep(wait_time)

#  while i < MAX_AUTO_MSG_TASK_TIME:

    while True:
        if MSG_QUEUE.full():
            info = "E: msg queue is full, cleared!"
            logger.warning(info)
            await NB.send_message(MY_ID, info)
            while not MSG_QUEUE.empty():
                await MSG_QUEUE.get()
#        try:
#          MSG_QUEUE.get_nowait()
#        except:
#          break
            await asyncio.sleep(5)

        logger.debug("queue size: {}".format(MSG_QUEUE.qsize()))
        logger.debug("waiting...")
        data = await MSG_QUEUE.get()

        # 0: normal msg [0, chat_id, text, {}]
        # 1: from matterbridge
        # 2: rss
        # 3: twitter
        # 4: from tg group (only for cmd answer, not forward msg)

        # 5: from put(), admin log, no flood check

        # 6: send as channel, for my group

        msg = data
        if data[0] == 0:
            msg = data
        elif data[0] == 5:
            # admin log
            logger.warning("put to master: {}".format(msg))
            await smf(msg)
            continue
            try:
                await NB.send_message(MY_ID, msg[2], **msg[3])
#            except:
            except FloodWait as e:
                logger.error(f"FloodWait: {msg=}", exc_info=True)
                await asyncio.sleep(error.seconds)
                await NB.send_message(MY_ID, msg[2], **msg[3])
            continue
        elif data[0] == 1:
            msgd = data[1]
            msg = await mtmsg2msg(msgd)
            if not msg:
                continue
        if len(msg[2]) > 4096:
            logger.warning("msg is too long, use link")
            msg[2] = await text2link(msg[2])

        if len(msg) == 3:
            msg.append({})

#    if msg[1] in MT_GATEWAY_LIST_for_tg:
#    if msg[0] == 0 or msg[0] == 1:
#    if True:
        if msg[0] == 1:
            ntime = time.time()
            if msg[1] in skip:
                if not recent or ntime - recent[-1] > wait_time * 20:
                    skip.remove(mag[1])


#                    await NB.send_message(msg[1], "start to forward msg")
                else:
                    continue
            recent.append(ntime)
            for i in recent:
                if ntime - i > wait_time:
                    recent.remove(i)
                else:
                    break
            if len(recent) > max_msg_flood:
                info = "W: flood!: tg://openmessage?chat_id={} : {}".format(
                    msg[1], msg[2])
                logger.warning(info)
                await NB.send_message(MY_ID, info)
                await NB.send_message(msg[1],
                                      "too many msg, start to ignore msg")
                skip.append(msg[1])
                continue

        if msg[0] == 0:
            await smf(msg)
        elif msg[0] == 1:
            await smf(msg)

        else:
            # slow mode, for rss, twitter...
            if msg[1] in locks:
                pass
            else:
                locks.update({msg[1]: asyncio.Lock()})

            if locks[msg[1]]:
                pass
            else:
                logger.error("wtf <2: {}".format(locks[msg[1]]))

            asyncio.create_task(sm(msg), name=msg[1])
        logger.debug("sent msg: {}".format(msg))


async def get_name_from_peer(peer):
    if not peer:
        return "unknown"
    if peer:
        #  if type(peer) == User:
        if isinstance(peer, User):
            if peer.username:
                name = peer.username
            else:
                name = peer.first_name
        else:
            # ignore username
            if hasattr(peer, 'title'):
                name = peer.title
            elif hasattr(peer, 'username'):
                name = peer.username
            elif hasattr(peer, 'first_name'):
                name = peer.first_name
            else:
                #                fwd_info+=str(utils.get_peer_id(peer))
                #  name = str(utils.get_peer_id(peer))
                name = str(peer.id)
        return name
    else:
        return "null"


async def get_name_for_mt(message, use_chat=False):
    sender_id = get_sender_id(message)
    if get_sender_id(message) == cid_tw:
        return "C twitter"
    #  elif get_sender_id(message) == TG_BOT_ID_FOR_MT:
    #  elif get_sender_id(message) == TG_BOT_ID_FOR_MT or get_sender_id(message) == 420415423:
    elif sender_id == 420415423 or sender_id == TG_BOT_ID_FOR_MT or sender_id == BOT_ID:
        name = "bot"
        text = message.text
        if text and ": " in text:
            name = text.split(": ", 1)[0]
            return name
    if use_chat is True:
        peer = message.chat
    else:
        peer = get_sender(message)
    if peer is not None:
        name = await get_name_from_peer(peer)
    else:
        name = get_sender_id(message)
        name = str(name)

    return f"T {name}"


async def parse_bridge_name(name):
    # _discord_885668436070531122_=58=20测试liqsliu
    if name.startswith("_discord_"):
        pass
    elif name.endswith("#0000"):
        return name.rstrip("#0000")
    elif "#0000 " in name and name.split("#0000 ", 1)[0][1] == " ":
        return name.split("#0000 ", 1)[0]
    else:
        return
    i = 0
    tmp = name.split("_", 3)[3]
    res = ""
    while i < len(tmp):
        if tmp[i] == "=":
            res += chr(int(tmp[i + 1:i + 3], 16))
            i += 2
        else:
            res += tmp[i]
        i += 1
    return res


# tg msg to mt
#async def send_msg_to_mt(message, edited=False):
async def parse_msg_for_mt(client, message, edited=False, reply=False):
#    if type(client, message) == messages.newmessage.NewMessage.Event:
#        if message.grouped_id is not None:
#            return
    #  msg=message.message
    msg = message
    # chat_id = message.chat_id
    chat_id = await get_id(message.chat)
    if chat_id in MT_GATEWAY_LIST_for_tg:
        gateway = MT_GATEWAY_LIST_for_tg[chat_id]
    else:
        gateway = "gateway1"
        logger.warning(
            "not found gateway, use default gateway for: {}".format(chat_id))
    logger.debug("msg: {}".format(message.text))

    qt = None
    # if not reply and msg.is_reply:
    if not reply and is_reply(message):
        logger.warning("get qt")
        # replied = await message.get_reply_message()
        replied = message.reply_to_message
        if replied:
            qt = await parse_msg_for_mt(client, replied, reply=True)
            if qt:
                qt = "{}{}".format(qt[1], qt[0])

    sender_id = get_sender_id(message)
    text = ""
    # if type(client, message) == messages.album.Album.Event:
    if 0:
        for msg in message.messages:
            if text:
                text += "\n"
            tmp = await msg2md(client, msg)
            if tmp is None:
                return
            text += f"{tmp}"
            break  # msg2md will parse grouped_id
    elif message.media_group_id:
        if not reply:
            await asyncio.sleep(5)
            last = await get_msg(get_chat_id(message), message.id-1, client=client)
            
            if last and message.media_group_id == last.media_group_id:
                logger.warning(f"ignore a group media message: {get_chat_id(message)} {message.id}")
                return
        logger.info("use msg2md")
        tmp = await msg2md(client, message)
        if tmp is None:
            return
            pass
        text += f"{tmp}"
        # group_id = message.media_group_id:
    else:
        text = await msg2md(client, message)

    logger.info("after msg2md: {text}")
    username = await get_name_for_mt(message)
    #  username = "T {}".format(username)
    if gateway == "gateway11":
        if ": " in text:
            if sender_id == TG_BOT_ID_FOR_MT:
                username = text.split(": ", 1)[0]
                text = text.split(": ", 1)[1]
            elif sender_id == 420415423:
                # t2bot
                username = text.split(": ", 1)[0]
                text = text.split(": ", 1)[1]
                #        if username.endswith("#0000"):
                username_real = await parse_bridge_name(username)
                if username_real:
                    if no_qt:
                        username = username_real
                elif discord_id_end_re.search(username):
                    username = "D {}".format(username)
                else:
                    username = "M {}".format(username)
    elif gateway == "gateway5":
        username = await get_name_for_mt(message, use_chat=True)
        #  username = "T {}".format(username)

    if gateway == "gateway5":
        # rss from channel
        if username == "T v2ex.com":
            if not "#reply0" in text:
                return
        if not reply and len(text.splitlines()) > 2:
            tmp = "**" + text.split("\n", 1)[0] + "**\n"
            tmp += text.split("\n", 1)[1]
            text = tmp

#                sender = message.sender
#                if not sender:
#                    sender = await message.get_sender()
#                if sender.bot and ": " in message.text:

    if gateway == "gateway11":
        rid = ennum(msg.id)
    else:
        #  rid = None
        rid = ennum(0)  #  disable search msg id
#    username = "{}{}: ".format(username, rid if rid is not None else "")
    if rid is not None:
        username = "{}{}: ".format(username, rid)
    else:
        username = "{}: ".format(username)

    #  return [await msg2md(client, message),username, gateway, qt]
    return [text, username, gateway, qt]

#  return await msg2md(client, message),username, gateway, qt


def get_another_client(client=UB):
    if client == UB:
        return NB
    else:
        return UB


async def file_to_ipfs(path):
    #  shell_cmd="{} {} {} {}"
    shell_cmd = ["bash", SH_PATH + "/file_to_ipfs.sh"]
    shell_cmd.append(path)
    shell_cmd.append("only")

    logger.info("save cmd: {}".format(shell_cmd))
    #  await run_my_bash(shell_cmd, shell=False)
    res = await my_popen(shell_cmd, shell=False, combine=False)
    if not res:
        return
    if res[0] != 0:
        logger.error("E: {}".format(res))
        return
    return res[1]



async def progress(current, total, m, i, link, lock):
    #  print(f"{current} {current * 100 / total:.1f}%")
    if current <= m[1]:
        return
    if current <= m[2]:
        return
    else:
        m[2] = current
    async with lock:
        if current <= m[1]:
            return
        if current < m[2]:
            return

        msg = m[0]
        if msg.edit_date:
            d = msg.edit_date.timestamp()
        else:
            d = msg.date.timestamp()
        w = time.time() - d
        if w < i:
            if current != total:
                return
            else:
                await asyncio.sleep(1)

        #  info = f"{link}\n{(format_byte((current - m[1])/i)}/s {format_byte(current)} =>{format_byte(total)} {current * 100 / total:.1f}%"
        info = f"{link} \n{format_byte(current)} / {format_byte(total)}\n{format_byte((current - m[1])/w)}/s {current * 100 / total:.3g}%"
        m[1] = current
        print(info)
        #  put(f"{msg.link} {current} {current * 100 / total:.1f}%")
        if info == msg.text:
            return
        try:
            #  m[0] = await asyncio.create_task(msg.edit(info))
            m[0] = await msg.edit(info)
        except bad_request_400.MessageNotModified:
            put(f"wtf: not modified: {info=} {msg.text=}")
        except flood_420.FloodWait as e:
            await asyncio.sleep(e.value+5)



# max in the same time
control_download_media = asyncio.Semaphore(1)


@tg_exceptions_handler
async def download_media(client, msg, chat_id=cid_test, in_memory=False):
    # path = await msg.download_media(DOWNLOAD_PATH)
    async with control_download_media:
        #  link = str(msg.link)
        link = await get_msg_link(msg)
        file = getattr(msg, msg.media.value)
        size = file.file_size
        await asyncio.sleep(1)
        try:
            m = await NB.send_message(chat_id, link + f"\n{format_byte(size)}...")
        except flood_420.FloodWait as e:
            await asyncio.sleep(e.value+5)
            put(link+f"\n{e=}")
            m = await NB.send_message(chat_id, link + f"\n{format_byte(size)}...")
        m = [m]
        m.append(0)
        m.append(0)

        lock = asyncio.Lock()
        i = 2
        if size > 64000000:
            i = 5
        if control_download_media.locked():
            i = i+3
        progress_args=(m, i, link, lock)
        if in_memory:
            path = await client.download_media(msg, in_memory=in_memory, progress=progress, progress_args=progress_args)
            dir2 = DOWNLOAD_PATH+"/"
        else:
            path = await client.download_media(msg, DOWNLOAD_PATH+"/", progress=progress, progress_args=progress_args)
            dir2 = SH_PATH+"/tmp/"
        #  path = await client.download_media(msg, DOWNLOAD_PATH+"/", progress=progress, progress_args=progress_args, block=False)
        if not path:
            put(f"fail to default dir, new dir: {dir2=}")
            logger.warning(f"fail to default dir, new dir: {dir2=}")
            if file:
                if size > 64000000:
                    logger.warning("too big")
                    put("too big")
                    return
            async with lock:
                text = m[0].text +"\nerror: chang dir, retry..."
                try:
                    await asyncio.sleep(3)
                    m[0] = await m[0].edit(text)
                    await asyncio.sleep(3)
                    m[0] = await NB.send_message(chat_id, link + "\n...")
                except bad_request_400.MessageNotModified:
                    put(f"wtf: not modified: {text=} {m[0].text=}")
                except flood_420.FloodWait as e:
                    await asyncio.sleep(e.value+5)
                    put(link+f"\n{e=}")
                    m[0] = await NB.send_message(chat_id, link + "\n...")

            path = await client.download_media(msg, dir2, progress=progress, progress_args=progress_args)
            #  path = await client.download_media(msg, SH_PATH+"/tmp/", progress=progress, progress_args=progress_args, block=False)
            if path:
                LOOP.call_later(3600, os.remove, path)
        async with lock:
            text = m[0].text +" OK"
            try:
                await asyncio.sleep(3)
                await m[0].edit(text)
            except bad_request_400.MessageNotModified:
                put(f"wtf: not modified: {text=} {m[0].text=}")
            except flood_420.FloodWait as e:
                await asyncio.sleep(e.value+5)
                put(link+f"\n{e=}")
        return path


#  lock_when_upload = asyncio.Lock()

import aiofiles

async def __save_file_to_local(data, name):
    #  with open(name, "wb") as file:
        #  file.write(data)
    async with aiofiles.open(name, "wb") as file:
        #  await file.write(data)
        try:
            logger.info(f"saveing: {name}")
            await asyncio.wait_for(file.write(data), timeout=120)
            logger.info(f"saved: {name}")
        except asyncio.TimeoutError:
            logger.error(f"save fail: {name}")
            put(f"save fail: {name}")

def _save_file_to_local(data, name):
    asyncio.run(__save_file_to_local(data, name))

async def save_file_to_local(data, name="tmp.bin"):
    # save file to net disk
    name = "{}/{}".format(DOWNLOAD_PATH, name)
    return await asyncio.to_thread(_save_file_to_local, data, name)

@disable_async
async def media2link(client, msg, pb=False, ex=False, all=False, max_file_size = 200000000):
    """download media of msg"""
    #  if client == NB:
    #      max_file_size = 200000000
    #  else:
    #      max_file_size = 64000000

    if msg.media and msg.media in MEDIAS:
        file = getattr(msg, msg.media.value)
        size = file.file_size
        if file:
            if size > max_file_size:
                logger.warning("too big")
                put("E: stop download, too big")
                return
        # path = await msg.download_media(DOWNLOAD_PATH)
        #  path = await client.download_media(msg, DOWNLOAD_PATH+"/")
        path = await download_media(client, msg, in_memory=True)
        ipfs = None
        if path:
            #  name = path.split('/')[-1]
            name = path.name
            name = name.split('/')[-1]
            #  data = path
            # path: <class '_io.BytesIO'>
            #  data = bytes(path.getbuffer())
            data = path.getbuffer()
            asyncio.create_task(save_file_to_local(data, name), name="saving "+name)
            if pb:
                link = await pastebin(data, filename=name)
                return link
            elif ex == "just":
                pass
            elif ex == "dd":
                tmp = []
                link = await pastebin(data, filename=name)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "ddd":
                tmp = []
                link = await pb_0x0(data, filename=name)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "dddd":
                tmp = []
                link = await transfer(data, filename=name)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "ddddd":
                link = await catbox(data, filename=name)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "dddddd":
                link = await catbox(data, filename=name, tmp=True)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "ddddddd":
                link = await file_io(data, filename=name)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif all:
                tmp = []
                link = await ipfs_add(data, filename=name)
                if link:
                    tmp.append(link)
                link = await catbox(data, filename=name, tmp=True)
                if link:
                    tmp.append(link)
                link = await pastebin(data, filename=name)
                if link:
                    tmp.append(link)
                link = await pb_0x0(data, filename=name)
                if link:
                    tmp.append(link)
                link = await transfer(data, filename=name)
                if link:
                    tmp.append(link)
                link = await file_io(data, filename=name)
                if link:
                    tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            else:
                #  ipfs = await file_to_ipfs(path)
                ipfs = await ipfs_add(data, filename=name)
        else:
            logger.error("down fail")
            return
        if path != None:
            #  name = path.split('/')[-1]
            url = 'https://{}/'.format(DOMAIN) + name.replace(' ', '%20')
            if url:
                if ipfs:
                    if ex or " " in ipfs:
                        return [ipfs + " " + url, name]
                    else:
                        return [ipfs, name]
                else:
                    return [url, name]
            else:
                return
    else:
        logger.warning(f"no media: {msg}")
        put(f"no media: {msg}")



@disable_async
async def media2link_bu(client, msg, pb=False, ex=False, all=False, max_file_size = 200000000):
    """download media of msg"""
    #  if client == NB:
    #      max_file_size = 200000000
    #  else:
    #      max_file_size = 64000000

    if msg.media and msg.media in MEDIAS:
        file = getattr(msg, msg.media.value)
        size = file.file_size
        if file:
            if size > max_file_size:
                logger.warning("too big")
                put("E: stop download, too big")
                return
        # path = await msg.download_media(DOWNLOAD_PATH)
        #  path = await client.download_media(msg, DOWNLOAD_PATH+"/")
        path = await download_media(client, msg)
        ipfs = None
        if path:
            name = path.split('/')[-1]
            if pb:
                with open(path, "rb") as file:
                    #  data = await asyncio.to_thread(file.read)
                    data = file
                    #  link = await pastebin(data)
                    link = await pastebin(data, filename=name)
                    return link
            elif ex == "just":
                pass
            elif ex == "dd":
                tmp = []
                with open(path, "rb") as file:
                    data = file
                    link = await pastebin(data, filename=name)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "ddd":
                tmp = []
                with open(path, "rb") as file:
                    data = file
                    link = await pb_0x0(data, filename=name)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "dddd":
                tmp = []
                with open(path, "rb") as file:
                    data = file
                    link = await transfer(data, filename=name)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "ddddd":
                tmp = []
                with open(path, "rb") as file:
                    data = file
                    link = await catbox(data, filename=name)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "dddddd":
                tmp = []
                with open(path, "rb") as file:
                    data = file
                    link = await catbox(data, filename=name, tmp=True)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif ex == "ddddddd":
                tmp = []
                with open(path, "rb") as file:
                    data = file
                    link = await file_io(data, filename=name)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            elif all:
                tmp = []
                #  ipfs = await file_to_ipfs(path)
                #  if ipfs:
                #      tmp.append(ipfs)
                with open(path, "rb") as file:
                    data = file
                    link = await ipfs_add(data, filename=name)
                    if link:
                        tmp.append(link)
                with open(path, "rb") as file:
                    data = file
                    link = await catbox(data, filename=name, tmp=True)
                    if link:
                        tmp.append(link)
                with open(path, "rb") as file:
                    #  data = await asyncio.to_thread(file.read)
                    data = file
                    link = await pastebin(data, filename=name)
                    if link:
                        tmp.append(link)
                with open(path, "rb") as file:
                    data = file
                    link = await pb_0x0(data, filename=name)
                    if link:
                        tmp.append(link)
                with open(path, "rb") as file:
                    data = file
                    link = await transfer(data, filename=name)
                    if link:
                        tmp.append(link)
                with open(path, "rb") as file:
                    data = file
                    link = await file_io(data, filename=name)
                    if link:
                        tmp.append(link)
                if tmp:
                    ipfs = " ".join(tmp)
            else:
                #  ipfs = await file_to_ipfs(path)
                with open(path, "rb") as file:
                    data = file
                    ipfs = await ipfs_add(data, filename=name)
        else:
            logger.error("down fail")
            return
        if path != None:
            name = path.split('/')[-1]
            #      from .ipfs import file_to_ipfs
            #print('https://liuu.tk/'+path.replace(' ','%20'))
            url = 'https://{}/'.format(DOMAIN) + name.replace(' ', '%20')
            if url:
                if ipfs:
                    if ex or " " in ipfs:
                        return [ipfs + " " + url, name]
                    else:
                        return [ipfs, name]
                else:
                    return [url, name]
            else:
                return
    else:
        logger.warning(f"no media: {msg}")
        put(f"no media: {msg}")


async def text2md(msg):
    #  if text and msg.entities and not pic_md_re.search(text):
    #  if msg.text:
    if msg.caption:
        text = msg.caption
        entities = msg.caption_entities
    else:
        text = msg.text
        entities = msg.entities
    if not text:
        return ""
    if text and entities and not pic_md_re.search(text):
        text_fix = {}
        url_index = 0
        urls = []
        for t in entities:
            # if type(t) == MessageEntityTextUrl:
            #  if t.type == "text_link":
            if t.type == enums.MessageEntityType.TEXT_LINK:
                #      if type(t) == MessageEntityUrl:

                url = text[t.offset:t.offset + t.length]

                if url == "\u200c":
                    continue

                s = url_re.match(text, t.offset)
                #  if url == t.url:
                #  if url == unquote(t.url):
                if unquote(url).rstrip("/") == unquote(t.url).rstrip("/"):
                    #  need not to check
                    continue
                    if s:
                        #  if s.group("url") == t.url:
                        #  url_p = urlsplit(s.group("url")).geturl()
                        url_p = urlsplit(s.group("url")).geturl()
                        if unquote(url_p).rstrip("/") == unquote(t.url).rstrip("/"):
                            #                            continue
                            pass
                        else:
                            info = "E: fixme, url_re may be bad: {} => {} != {}".format(text[t.offset:], unquote(t.url), url_p)
                            info += "\nmsg link: "
                            info += await get_msg_link(msg)
                            mp(info)
                    else:
                        #                        info = "E: fixme, can't find a url, text: " + text[t.offset:] + "\n msg: " + msg.stringify()
                        info = "E: fixme, can't find a url, text: " + text[
                            t.offset:]
                        info += "\nmsg link: "
                        info += await get_msg_link(msg)
                        mp(info)
                else:
                    if s:
                        url_p = urlsplit(s.group("url")).geturl()
                        if s.span()[0] < t.offset + t.length:
                            if unquote(url_p).rstrip("/") == unquote(t.url).rstrip("/"):
                                # fix is better: just a mistake
                                continue
                            else:
                                # may be malicious
                                t.url = t.url + " may be malicious"
                                info = "W: find a bad url: {} => {} != {}".format( text[t.offset:], unquote(t.url), url_p)
                                info += "\nmsg link: "
                                info += await get_msg_link(msg)
                                mp(info)
                                put(info)
                                # continue
                        else:
                            pass
                    else:
                        pass

                if text_has_md(text, t.url):
                    continue


#        if text[t.offset-1] == "(" and len(text) >= t.offset+t.length and text[t.offset+t.length] == "(":
#          continue
                url_index += 1
                tmp = "["
                if t.offset in text_fix:
                    tmp = text_fix[t.offset] + tmp
                text_fix.update({t.offset: tmp})

                tmp = "][%s]" % url_index
                if t.offset + t.length in text_fix:
                    tmp = text_fix[t.offset + t.length] + tmp
                text_fix.update({t.offset + t.length: tmp})

                urls.append(t.url)
        if url_index:
            new_text = ""
            o = 0
            #      for i in sorted(text_fix):
            for i in text_fix:
                new_text += text[o:i]
                new_text += text_fix[i]
                o = i
            if len(text) != i:
                new_text += text[i:]

            # print hidden link in message from telegram
            new_text = new_text.replace("[\u200b]", "[hidden_link]")
            #  new_text = new_text.replace("[\u200c]", "[hidden_link]")

            new_text += "\n"
            url_index = 0
            for url in urls:
                url_index += 1

                # fix markdown error
                p = urlparse(url)
                path = p.path.replace("-", "%2D")
                path = path.replace("*", "%2A")
                path = path.replace("_", "%5F")
                path = path.replace(":", "%3A")
                path = path.replace(" ", "%20")
                path = path.replace("\"", "%22")
                path = path.replace("'", "%27")
                p = p._replace(path=path)
                url = p.geturl()

                new_text += "\n[%s]: %s" % (url_index, url)
                text = new_text
    return text




MEDIAS = {enums.MessageMediaType.PHOTO, enums.MessageMediaType.DOCUMENT}
MEDIAS.add(enums.MessageMediaType.VIDEO)
MEDIAS.add(enums.MessageMediaType.AUDIO)
MEDIAS.add(enums.MessageMediaType.VOICE)
MEDIAS.add(enums.MessageMediaType.ANIMATION)
MEDIAS.add(enums.MessageMediaType.VIDEO_NOTE)

MEDIAS.add(enums.MessageMediaType.STICKER)


async def msg2md(client, message):
    #  client=bot
    msg = message

    #  text = msg.text
    #  if not text:
    #      if msg.caption:
    #          text = msg.caption

    text = await text2md(msg)
    logger.info(text)

    if client == NB:
        max_file_size = 10000000
    else:
        max_file_size = 64000000
    media = ""
    # audio, document, photo, sticker, video, animation, voice, video_note,
    # contact, location, venue, poll, web_page, dice, game.
    #  if msg.media in ["audio","document","photo","sticker","video","animation","voice","video_note"]:
    if msg.media in MEDIAS:
        file = getattr(msg, msg.media.value)
        size = file.file_size
    else:
        file = None
    if file and size > max_file_size:
        if text:
            media += "\n\n"
        media = "[file is too big. tg link: {} ]".format(await get_msg_link(msg))
    if file and size < max_file_size:
        group_id = msg.media_group_id
        if not group_id:
            res = await media2link(client, msg)
            if res:
                urls = res[0]
                if len(res) == 2:
                    name = res[1]
                else:
                    #  name = "media"
                    name = msg.media
                if text:
                    media += "\n\n"
                media += '[{}]({})'.format(name, urls)
        else:
            msg_id = msg.id
            if group_id:
                try:
                    msgs = await client.get_media_group(get_chat_id(msg), msg_id)
                except ValueError as e:
                    info = f"can't get media group\nmsg: {await get_msg_link(msg)}\nE: {e=}"
                    put(info)
                    return
                for msgn in msgs:
                # async for msgn in client.iter_messages(
                        # message.chat_id,
                        # limit=8,
                        # ids=list(range(msg_id + 1, msg_id + 4))):

                    # if msgn and msgn.grouped_id == group_id:
                    #  if msgn and msgn.media_group_id == group_id:
                    res = await media2link(client, msgn)
                    if res:
                        urls = res[0]
                        if len(res) == 2:
                            name = res[1]
                        else:
                            #  name = "media"
                            name = msg.media
                    else:
                        break
                    #  if msgn.text:
                    if msgn.caption:
                        if not text:
                            text = await text2md(msgn)
                        elif msgn.id != msg_id:
                            media += '\n\n[{}]({})'.format((await text2md(msgn)).replace("\n", " "), urls)
                            continue
                    media += '\n\n[{}]({})'.format(name, urls)

    if media:
        if not text:
            text = media
        else:
            text += media

    if text:
        #  if msg.forward_date:
        if get_sender_id(msg) != cid_tw and msg.forward_date:
            #      fwd_info="Forwarded from "
            fwd_info = "转自 "
            # username? firstname?
            # if f.from_name:
            if msg.forward_from:
                fwd_info += await get_name_from_peer(msg.forward_from)
            elif msg.forward_from_chat:
                fwd_info += await get_name_from_peer(msg.forward_from_chat)
            else:
                fwd_info += f"{msg.forward_sender_name}"

            fwd_info += ": "
            text = fwd_info + text

        logger.info(text)
        return text
    else:
        return "null"







async def save2db(e, table, in_chat=None):
    if e is None:
        return
    data = {}
    cs = db.columns(table)
    d = e.__dict__.copy()
    if table == "user":
        if d.get("first_name", None) is None:
            return
    elif table == "message":
        if d.get("chat", None) is None:
            return
        # d = e.message.to_dict()
        # d["chat_id"] = await get_id(e.chat_id)
        # d["sender_id"] = await get_id(e.sender_id)
        if e.text:
            d["text"] = e.text
        else:
            return
        d["id"] = e.id
        #  d["id"] = d.get("id", None)
        #  d["chat"] = await get_id(e.chat)
        d["chat"] = get_chat_id(e)
        #  d["sender"] = await get_id(e.from_user)
        d["sender"] = get_sender_id(e)
    elif table == "chat":
        if d.get("title", None) is None:
            return
    elif table == "channel":
        if d.get("title", None) is None:
            return

    if d["id"] is None:
        logger.error(f"need fix: id not found: {d}")
        return

    if table == "message":
        if d["chat"] is None:
            logger.error(f"need fix: chat not found: {d}")
            rerurn

    # if "date" in cs:
        # # d["date"] = int(e.date.timestamp())
        # d["date"] = e.date.timestamp()

    for i in cs:
        if i in d:
            # if d.get(i, None) is not None:
            data.update({i: d.get(i)})
    if table == "user" and in_chat is not None:
        g = db.get(in_chat, "chat")
        if g is not None:
            id2 = db.get(in_chat, "chat")["id2"]
            u = db.get(d["id"], "user")
            if u is not None:
                g = u["groups"]
                if g is None:
                    g = 0
                else:
                    g = byte2num(g)
                data["groups"] = num2byte(1<<(id2-1) | g)
                if data == u:
                    logger.warning(f"skip {data['id']}")
                    return
    elif table == "chat":
        g = db.get(data["id"], "chat")
        if g is not None:
            g.pop("id2")
            if data == g:
                logger.warning(f"skip {data['id']}")
                return
    #  print(data)
    #  return
    db.save(data, table)
    return data


async def get_peer(name,
                   chat=None,
                   client=None,
                   no_client2=False,
                   input=False):
    """name: name or id or peer
  chat: name or id or peer"""

    if not name:
        return None
    if client is None:
        client = UB

    #  if type(name) == str:
    if isinstance(name, str):
        if chat:
            users = []
            try:
                #        if type(chat) == int:
                #          chat= await get_peer(chat, client=client)
                #          chat=utils.get_peer_id(chat)
#                async for user in client.iter_participants(chat, search=name):
                #  async for user in client.iter_chat_members(chat, query=name, limit=5):
                async for user in client.get_chat_members(chat, query=name, limit=5):
                    if user.username:
                        if name != user.username:
                            continue
                    elif user.first_name != name:
                        continue
                    users.append(user)
            except Exception as e:
                logger.error(e)
            if not users:
                logger.warning("not find user: {} in chat".format(name))
            return users
        if name[0] == "@":
            id = name[1:]
        else:
            id = await get_id(name)
    elif type(name) == int:
        # id = utils.resolve_id(name)[0]
        id = name
        tmp = id
        # ########
        if str(tmp).startswith("-100"):
            if db.existed("chat", tmp) or db.existed("channel", tmp):
                id = tmp
                tmp = 0
            else:
                tmp = int(str(tmp)[4:])
        elif tmp < 0:
            if db.existed("chat", tmp):
                id = tmp
                tmp = 0
            else:
                tmp = -1*tmp

        if tmp > 0:
            if db.existed("user", tmp):
                id = tmp
                tmp = 0
            else:
                tmp = -1*tmp
        if tmp < 0:
            if db.existed("chat", tmp):
                id = tmp
                tmp = 0
            else:
                tmp = int("-100"+str(-1*tmp))
        if tmp < 0:
            if db.existed("chat", tmp) or db.existed("channel", tmp):
                id = tmp
                tmp = 0
        # ########
        if tmp == 0:
            return await _get_peer(id, client=client)


        tmp = id
        if str(tmp).startswith("-100"):
            peer = await _get_peer(tmp, client=client)
            if peer:
                d = await save2db(peer, "chat")
                return peer
            tmp = int(str(tmp)[4:])
        elif tmp < 0:
            peer = await _get_peer(tmp, client=client)
            if peer:
                d = await save2db(peer, "chat")
                return peer
            tmp = -1*tmp
            id = tmp

        if tmp > 0:
            peer = await _get_peer(tmp, client=client)
            if peer:
                d = await save2db(peer, "user")
                return peer
            tmp = tmp*(-1)

        if id == tmp:
            pass
        else:
            peer = await _get_peer(tmp, client=client)
            if peer:
                d = await save2db(peer, "chat")
                return peer
        tmp = int("-100"+str(-1*tmp))
        if id == tmp:
            return
        peer = await _get_peer(tmp, client=client)
        if peer:
            d = await save2db(peer, "chat")
            return peer
        return
    else:
        #    id=utils.resolve_id(name)[0]
        id = name

    return await _get_peer(id)


ERRORS =(ValueError, bad_request_400.UsernameInvalid, bad_request_400.ChatIdInvalid, bad_request_400.PeerIdInvalid, bad_request_400.ChannelInvalid)

async def _get_peer(id, client=UB):
    peer = None
    try:
        if type(id) == int and id > 0:
            peer = await client.get_users(id)
        else:
            peer = await client.get_chat(id)
    except pyrogram.errors.exceptions.not_acceptable_406.ChannelPrivate as e:
        print(f"can not get info of private channel {id}")
        return
    except ERRORS as e:
        try:
            client = get_client2(client)
            if type(id) == int and id > 0:
                peer = await client.get_users(id)
            else:
                peer = await client.get_chat(id)
        except pyrogram.errors.exceptions.not_acceptable_406.ChannelPrivate as e:
            print(f"can not get info of private channel {id}")
            return
        except ERRORS as e:
            logger.warning("can not find peer for: {}\nbecause: {}".format(id, e))
    return peer

async def get_msg_from_url(url, client=UB):
    msg = None
    if isinstance(url, str):
        if len(url.split('/')) >= 5 and url.split('/')[2] == "t.me":
            if url.split('/')[3] == "c":
                id = int(url.split('/')[4])
                cid = (await get_peer(id, client)).id
            elif url.split('/')[3] == "s":
                cid = url.split('/')[4]
            else:
                cid = url.split('/')[3]
            if "?comment=" in url:
                cid = (await get_peer(cid, client=client)).linked_chat.id
            id = await get_msg_id(url)
            msg = await get_msg(cid, ids=id, client=client)
            if not msg:
                await client.send_message(
                    MY_ID, "E: all clients: can't find the msg: {}".format(url))
                return None
    elif isinstance(url, int):
        return await get_msg_from_url(f"https://t.me/c/{cid_test}/{url}", client=client)
    else:
        await client.send_message(MY_ID, "E: error url: {}".format(url))
        return None
    return msg


def get_client2(client):
    if client == UB:
        return NB
    else:
        return UB


async def get_fwd_info(client, message):
    if is_forward(message):
        msg = message
        info = "fwd: "
        if msg.forward_from_chat:
            peer = msg.forward_from_chat
            cid = peer.id
#            peer = await get_peer(cid, client=client)
            rcid = get_real_id(peer)
            if peer.username:
                info += "\nfrom group: https://t.me/" + peer.username + "/" + str(msg.forward_from_message_id)
            else:
                info += "\nfrom group: https://t.me/c/" + str(rcid) + "/" + str(msg.forward_from_message_id)
            if peer.username:
                info += "\ninfo: @" + peer.username
            info += "\ncid: `" + str(cid) + "`"
            info += " tg://openmessage?chat_id=" + str(rcid)
            if msg.forward_signature:
                info += "\nsignature: {}".format(msg.forward_signature)
        elif msg.forward_from:
            peer = msg.forward_from
            cid = peer.id
#            peer = await get_peer(cid, client=client)
            rcid = get_real_id(peer)
            if msg.forward_from_message_id:
                if peer.username:
                    info += "\nfrom: https://t.me/" + peer.username + "/" + str(msg.forward_from_message_id)
                else:
                    info += "\nfrom: https://t.me/c/" + str(rcid) + "/" + str(msg.forward_from_message_id)
            info += "\ninfo: "
            if peer.username:
                info += " @" + peer.username
            else:
                if cid > 0:
                    info += " tg://openmessage?user_id=" + str(rcid)
                else:
                    info += " tg://openmessage?chat_id=" + str(rcid)
            info += "\nid: `" + str(cid) + "`"
        elif msg.forward_sender_name:
            info += "\nsent by:"
            info += "only name: " + msg.forward_sender_name
        else:
            info += "None"
    else:
        info = None
    return info

async def fuck_empty_msg(msg, chat_id, ids, ex=""):
    info = ex
    if isinstance(chat_id, str):
        #  chat_id = await get_id(chat_id, client)
        #  put(f"fail to get msg for: {chat_id} {ids}\nmsg link: https://t.me/{chat_id}/{ids}\n\nempty:\n{msg}")
        info += f"fail to get msg for: {chat_id} {ids}\nmsg link: https://t.me/{chat_id}/{ids}\n\nempty:\n{msg}"
    else:
        #  put(f"fail to get msg for: {chat_id} {ids}\nmsg link: https://t.me/c/{get_real_id(chat_id)}/{ids}\n\nempty:\n{msg}")
        info += f"fail to get msg for: {chat_id} {ids}\nmsg link: https://t.me/c/{get_real_id(chat_id)}/{ids}\n\nempty:\n{msg}"
    #  if e:
    if isinstance(msg, Exception):
        info += f"\n\n{msg=}"
    else:
        info += f"\n\nempty msg:\n{msg}"

    put(info)

async def get_msg(chat_id=GID, ids=1, client=None):
    if client is None:
        client = UB
    msg = None
        #        peer = await get_peer(cid, client=client, no_client2=True)
        # msg = await client.get_messages(chat_id, ids=ids)
    try:
        msg = await client.get_messages(chat_id, ids)
        if msg:
            if msg.empty:
                await fuck_empty_msg(msg, chat_id, ids)
            else:
                return msg
    except bad_request_400.ChannelInvalid as e:
        # maybe a private group
        logger.error(e)
        logger.warning("can not get msg")
        put(f"{e=}")

    try:
        client = get_client2(client)
        msg = await client.get_messages(chat_id, ids)
        #  if msg.empty:
        #      await client.send_message(MY_ID, f"client2: empty msg:\n{msg}")
        if msg:
            if msg.empty:
                await fuck_empty_msg(msg, chat_id, ids, ex="client2: ")
            return msg
    except bad_request_400.ChannelInvalid as e:
        # maybe a private group
        logger.warning("client2 can not get msg")
        logger.info(e)
        #  put(f"client2: {e=}")
        #  put(f"client2: fail to get msg for: {chat_id} {ids}\nmsg link: https://t.me/c/{get_real_id(chat_id)}/{ids}\n\n{e=}")
        await fuck_empty_msg(e, chat_id, ids, ex="client2: ")


async def get_msg_id(url):
    """link to id"""
    id = 0
    if type(url) == int:
        return url
    elif "?comment=" in url:
        id = int(url.split('=')[1])
    else:
        #        id = int(url.split('/')[-1])
        id = int(url.split('/')[-1].split('?')[0])
    if id:
        return id
    else:
        return None




#  except Exception as e:
#except:
#    await client.send_message(me.id, "E: "+str(e)+"\n==\n"+traceback.format_exc())
#    await myprint("==\n"+traceback.format_exc())
#    await bot.send_message(me.id, "E: "+str(e)+"\n==\n"+traceback.format_exc())
#    await client.send_message(me.id, "E: "+sys.exc_info()[0]+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info()))
#  info="E: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
#  await bot.send_message(MY_ID, info)
#  if client == userbot:
#    await client.send_message(MY_ID, "E: > tg://openmessage?user_id="+str(bot_id))

#@messages.register(messages.NewMessage)
#  async def run_cmd_for_bots(client, message):
#    client = message.client
#  sender=await client.get_input_entity(sender_id)
#  try:
#  if msg.via_bot:
#    return
#  if type(message.peer_id) == PeerUser and chat.bot:
#    return
#  if sender and sender.bot:
#    return


async def myprint(msg,
                  #  parse_mode="text",
                  parse_mode=enums.ParseMode.DEFAULT,
                  message=None,
                  client=None,
                  *args,
                  **kwagrs):
    if client is None:
        if message:
            client = message.client
        else:
            client = NB
    if args:
        msg += " ".join(str(v) for v in args)
    if len(msg.strip()) == 0:
        return
        msg = "null"
    logger.info("I: myprint:" + str(msg))
    if len(msg) > MAX_MSG_LEN:
        #    msg=subprocess.run(["bash", SH_PATH+"/change_long_text.sh", msg ], stdout=subprocess.PIPE, text=True ).stdout
        msg = await text2link(msg)
    if message and message.chat_id:
        id = message.chat_id
    else:
        id = MY_ID
    if parse_mode == enums.ParseMode.MARKDOWN:
        #    return await client.send_message(log_cid, msg, parse_mode=parse_mode)
        #        return await client.send_message(log_cid, msg, parse_mode=parse_mode)

        return await client.send_message(id, msg, parse_mode=parse_mode)
    else:
        return await client.send_message(id, msg)


async def myprintmd(msg, *args, **kwagrs):
    return await myprint(msg, parse_mode=enums.ParseMode.MARKDOWN, *args, **kwagrs)


async def myprintraw(msg, *args, **kwagrs):
    #  return await myprintmd("`"+msg.replace("`","\\`")+"`")
    if len(msg) > MAX_MSG_LEN:
        return await myprint(msg, *args, **kwagrs)
    else:
        return await myprintmd("```\n" + msg + "\n```", *args, **kwagrs)


#    msg=mdraw(msg,"code")


async def get_id(url, client=None):
    """get id"""
    if not url:
        return None
    if client is None:
        client = UB
    id = 0
    if type(url) == int:
        id = url
        if id < 0:
            # id = utils.resolve_id(id)[0]
            pass
        return id
    elif isinstance(url, str):
        if url[0] == "@":
            # peer = await get_peer(url[1:], message=message)
            peer = await get_peer(url, client=client)
            # id = utils.resolve_id(utils.get_peer_id(peer))[0]
            id = peer.id
        elif len(url.split('/')) >= 4 and url.split('/')[2] == "t.me":
            if url.split('/')[3] == "c":
                id = int(url.split('/')[4])
            elif url.split('/')[3] == "s":
                id = await get_id("@"+url.split('/')[4], client=client)
            else:
                id = await get_id("@"+url.split('/')[3], client=client)
        elif url.isnumeric():
            # id = utils.resolve_id(int(name))[0]
            id = int(url)
        elif url[0] == "-" and url[1:].isnumeric():
            # id = utils.resolve_id(int(url))[0]
            id = int(url)
        else:
#            id = int(url)
            # id = utils.resolve_id(utils.get_peer_id(id))[0]
            id = await get_id("@"+url, client=client)

        if "?comment=" in url:
            id = await get_linked_cid(id, client)
        if id:
            return id
        else:
            return None
    elif isinstance(url, types.PeerChannel):
        return int("-100"+str(url.channel_id))
    elif isinstance(url, types.PeerChat):
        return -1*url.chat_id
    elif isinstance(url, types.PeerUser):
        return url.user_id
    else:
        # may be a peer
        id = url.id
        return id


async def get_msg_link(msg):
    """meg to link"""
    #  if msg.link:
    #      return msg.link
    peer = msg.chat
    if peer is not None:
        #  if peer.id == MY_ID:
        #      #  id = BOT_ID
        #      #  name = f"c/{id}"
        #      if client == UB:
        #          name = MY_NAME
        #      else:
        #          name = BOT_NAME
        if peer.username:
            name = peer.username
        else:
            id = get_real_id(peer)
            name = f"c/{id}"
    else:
        return "None"
    return "https://t.me/" + name + "/" + str(msg.id)
    return "msg link: https://t.me/c/" + str(utils.resolve_id(
        msg.chat_id)[0]) + "/" + str(msg.id)


#group
async def get_admins(url, client=UB):

    #  if type(chat) == str or type(chat) == int:
    if isinstance(url, str) or isinstance(url, int):
        chat = await get_peer(url, client=client)
        chat_id = chat.id
        #  chat_id = await get_id(chat, client=client)
    elif isinstance(url, Chat):
        chat = url
        chat_id = chat.id
    else:
        logger.error("wtf chat")
        return
    info = "admin of: "
    users = []
    if chat.username:
        info = info + "@" + chat.username
    else:
        info += f"{chat.id}"
    try:
        #  users = await client.get_chat_members(chat_id, filter="administrators")
        #  users = await client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)
        async for user in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            users.append(user)
    except bad_request_400.ChatAdminRequired as e:
        info = "E: need admin"
        if chat.type == enums.ChatType.CHANNEL:
            info = info + ", but for channel:\n"
            info = info + str(await get_admin_of_channel(chat, client=client))
    except Exception as e:
        logger.error(e)
        raise
        #  client2 = get_client2(client)
        #  users = await client2.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)
        async for user in client2.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            users.append(user)
    except Exception as e:
        logger.error(e)
        raise

    for user in users:
        info = info + "\n"
        #  if user.is_anonymous:
        #      info = info + " - "
        #  if user.status == "creator":
        if user.status == enums.ChatMemberStatus.OWNER:
            info = info + "owner: "
        user = user.user
        if user.is_bot:
            info = info + "bot"
        else:
            info = info + str(user.id)
        if user.username:
            info = info + " @" + user.username
        if user.first_name:
            info = info + " " + user.first_name

    return info


#small group: Chat
async def get_admin_of_group(msg, message=None):
    if message is None:
        client = UB
    else:
        client = message.client
    peer = await get_peer(msg, message)
    if type(peer) == Chat:
        info = "id: `" + str(utils.get_peer_id(peer))
        if peer.username:
            info = info + "` @" + peer.username
        else:
            info = info + "` no name, tg://openmessage?chat_id=" + str(peer.id)
#    full = await client(functions.messages.GetFullChatRequest(peer.id))
        full = await client(functions.channels.GetFullChannelRequest(peer))
        full_chat = full.full_chat
        if full_chat.exported_invite:
            id = str(full_chat.exported_invite.admin_id)
            info = info + "\nadmin id: `" + id + "` tg://openmessage?user_id=" + id
        else:
            info = info + "can't find admin id in group"
        return info


#channel or big group: Channel
async def get_admin_of_channel(chat, client=UB):
    if isinstance(chat, str) or isinstance(chat, int):
        #        chat=await client.get_entity(await get_id(chat))
        chat = await get_peer(chat, client=client)
        chat_id = chat.id
        #  chat_id = await get_id(chat, client=client)
    elif isinstance(chat, Chat):
        chat_id = chat.id
    else:
        logger.error("wtf chat")
        return
    peer = chat
    info = ""
    if peer.type == "channel":
        info = "id: `" + str(peer.id) +"`"
        if peer.linked_chat:
            peer = peer.linked_chat
            if peer.username:
                info += " @" + peer.username
            else:
                info += " no username, tg://openmessage?chat_id=" + str(get_real_id(peer))
            info = info + "\nlinked id: `" + str(peer.id)
            info = info + "`\n" + (await get_admins(peer, client))
        else:
            info = info + "\nno linked group"

    elif type(peer) == Chat:
        info = await get_admins(peer, message=message)
    else:
        info = "wtf: " + str(type(peer)) + " " + str(peer)
    return info


async def get_linked_cid(id, client=None):
    peer = await get_peer(id, client=client)
    if hasattr(peer, "linked_chat") and peer.linked_chat is not None:
        return peer.linked_chat.id
    return None

    if client is None:
        client = UB
    peer = await client.get_input_entity(id)
    if not peer:
        peer = await client.get_input_entity(await get_peer(id, message=message))
#  if type(peer) == User:
    if type(peer) == InputPeerUser or type(peer) == User:
        return None
        full = await client(functions.users.GetFullUserRequest(id=peer))
#  elif type(peer) == Chat:
    elif type(peer) == InputPeerChat or type(peer) == Chat:
        full = await client(functions.messages.GetFullChatRequest(peer.chat_id)
                            )
    #https://docs.telethon.dev/en/latest/concepts/chats-vs-channels.html
    #megagroups are channels
#  elif peer.broadcast or peer.megagroup or peer.gigagroup:
    elif type(peer) == InputPeerChannel or type(peer) == Channel:
        full = await client(functions.channels.GetFullChannelRequest(peer))
    else:
        await myprint("unknown type,not full:" + str(type(peer)))
    full_chat = full.full_chat
    if full_chat.linked_chat_id:
        #      info=info+"\nlinked id: `"+str(utils.get_peer_id(types.PeerChannel(full_chat.linked_chat_id)))
        return full_chat.linked_chat_id
    else:
        return None


#    async def download_media_task(msg,path):


#  #https://docs.python.org/3/library/asyncio-task.html#asyncio.run
#  async def download_media(msg, message=None):
#      if message:
#          client = message.client
#      else:
#          if msg:
#              client = msg.client
#          else:
#              client = UB
#      msg_before_return = [None]
#
#      async def download_media_callback(current, total):
#          """  # Printing download progress  #https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.downloads.DownloadMethods.download_media """
#
#          nonlocal msg_before_return
#          #      print('Downloaded', current, 'out of', total,'bytes: {:.2%}'.format(current / total))
#          #      await myprint('Downloaded', current, 'out of', total,'bytes: {:.2%}'.format(current / total))
#          msg_before_return[0] = (
#              'Downloaded ' + str(current) + ' out of ' + str(total) +
#              ' bytes: {:.2%}'.format(current / total)).strip()
#
#  #    nonlocal msg_before_return
#
#      task = asyncio.create_task(
#          msg.download_media(file=DOWNLOAD_PATH + "/",
#                             progress_callback=download_media_callback))
#      last_msg = ""
#      msg = ""
#      while True:
#          await asyncio.sleep(1)
#          if task.done():
#              break
#          elif not msg_before_return[0]:
#              if last_msg != msg_before_return[0]:
#                  last_msg = msg_before_return[0]
#                  #            await myprint(msg_before_return)
#                  if msg:
#                      await msg.edit(msg_before_return)
#                  else:
#                      msg = await client.send_message(msg.chat_id,
#                                                      msg_before_return)
#
#
#  #      msg.delete()
#      return task.result()


async def my_method(custom_method):
    result = await client(
        functions.bots.SendCustomRequestRequest(
            custom_method=custom_method,
            params=types.DataJSON(data='some string here')))
    await myprint(result.stringify())


async def update_profile(msg):
    client = UB
    result = await client(
        functions.account.UpdateProfileRequest(first_name='some string here',
                                               last_name='some string here',
                                               about='some string here'))
    await myprint(result.stringify())


async def update_name(msg):
    client = UB
    #      result = await client(functions.account.UpdateProfileRequest(
    result = await client(
        functions.account.UpdateProfileRequest(first_name=msg))
    await myprint(result.stringify())


async def ban_chat(client, message):
    chat_id = get_chat_id(message)
    sender_id = get_sender_id(message)
    put(f"will ban {sender_id}")
    if sender_id == cid_wtfipfs:
        put("not ban me")
    else:
        res = await client.ban_chat_member(chat_id, sender_id)
    put(str(res))
    #  await client.send_message(chat_id, "不要用频道身份的发言，否则该频道会被自动屏蔽。")
    await message.reply("不要用频道身份的发言，否则该频道会被自动屏蔽。")


from pyrogram.raw.types import BotCommandScopePeer, InputPeerChat, BotCommandScopeDefault, BotCommandScopeChats, BotCommandScopeUsers, BotCommandScopePeerUser
# from pyrogram.raw.functions.bots import SetBotCommands
from pyrogram.raw import functions

async def set_bot_cmd(client, message):

    if client.bot_token is None:
        return

    tg_cmd = "help,ping,myid,dc,uptime,sh c,free"
    cmds = tg_cmd.split(",")

    commands = []
    buttons = []
    for i in cmds:
        k = i.split(" ")[0]
        if await CMD.check_cmd(client, message, cmd=k):
            pass
        else:
            continue

        if len(CMD.cmds[k]) > 3:
            commands.append(BotCommand(k, CMD.cmds[k][3]))
        else:
            commands.append(BotCommand(k, i))
        if is_group(message):
            i = "/"+i
        buttons.append(i)

    chat_id = get_chat_id(message)
    sender_id = get_sender_id(message)
    if buttons:
        tmp = [[]]
        for i in buttons:
            if len(tmp[-1]) == 4:
                tmp.append([])
            tmp[-1].append(i)

        buttons = tmp
        if sender_id == MY_ID:
            selective = True
        else:
            selective = False
            selective = True
        #  await client.send_message(
        #    get_chat_id(message),
        await message.reply(
            "button is ok",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                selective=selective,
                resize_keyboard=True
            )
        )
    await asyncio.sleep(1)
    if commands:
        # await client.set_bot_commands(None)
        # await client.set_bot_commands(commands)
        peer = await client.resolve_peer(chat_id)
        user_id = await client.resolve_peer(sender_id)
        if is_private(message):
            if chat_id == MY_ID:
                # peer = InputPeerChat(chat_id=chat_id)
                # print(peer)
                scope = BotCommandScopePeer(peer=peer)
            else:
                scope = BotCommandScopeUsers()
            #  await client.send(functions.bots.SetBotCommands(scope=scope, lang_code="", commands=[c.write() for c in commands or []]))
            await client.invoke(functions.bots.SetBotCommands(scope=scope, lang_code="", commands=[c.write() for c in commands or []]))
        elif is_group(message):
            if sender_id == MY_ID:
                scope = BotCommandScopePeerUser(peer=peer, user_id=user_id)
            else:
                scope = BotCommandScopeChats()
            await client.invoke(functions.bots.SetBotCommands(scope=scope, lang_code="", commands=[c.write() for c in commands or []]))
        else:
            if sender_id == MY_ID:
                scope = BotCommandScopePeerUser(peer=peer, user_id=user_id)
            else:
                scope = BotCommandScopeDefault()
            await client.invoke(functions.bots.ResetBotCommands(scope=scope, lang_code=""))



async def run_cmd(cmd=[], message=None, client=None):
    if client is None:
        if message:
            client = message.client
        else:
            client = UB

    global auto_forward_list, debug, auto_msg_list, feed_list
    auto_forward_list = CONFIG[0]
    auto_msg_list = CONFIG[1]
    feed_list = CONFIG[2]

    chat_id = message.chat_id
    sender_id = message.sender_id
    chat = message.chat
    sender = message.sender
    msg = message.message

    if cmd[0] == "ping":
        if len(cmd) == 1:
            #          await client.send_message(message.chat_id, "pong")
            await message.reply("pong")
    elif cmd[0] == "dc":
        pass
    elif cmd[0] == "help":
        if client == NB:
            await set_bot_cmd(client, message)
        await client.send_message(message.chat_id, "use cmd")
    elif cmd[0] == "start":
        if client == bot:
            await set_bot_cmd(client, message)
        await client.send_message(message.chat_id, "ok")
    elif cmd[0] == "dg":
        if len(cmd) == 1:
            debug = not debug
        await myprint(str(debug))
    elif cmd[0] == "myid" and len(cmd) == 1:
        if message.is_private:
            await message.reply(str(sender_id))
        else:
            if message.is_reply:
                replied = await message.get_reply_message()
                if replied:
                    await message.reply(str(replied.sender_id))
            else:
                await message.reply(str(sender_id))

    elif cmd[0] == "save":
        await save_config()
        await client.send_message(
            message.chat_id,
            str([auto_forward_list, auto_msg_list,
                 feed_list]).replace(" ", "").strip())
    elif cmd[0] == "unpin":
        peer = await client.get_input_entity(await get_id(cmd[1]))
        if not peer:
            peer = await client.get_entity(await get_id(cmd[1]))
        result = await client(functions.messages.UnpinAllMessagesRequest(peer))
        await client.send_message(message.chat_id, result.stringify())
    elif cmd[0] == "me":
        if len(cmd) == 1:
            await client.send_message(message.chat_id, "me name|all text")
        elif cmd[1] == "name":
            await update_name(message.text.split(" ", 2)[2])

    elif cmd[0] == "fid":
        msg = await my_get_form_link(cmd[1])
        if msg:
            if msg.file:
                await myprint(str(msg.file.id))
            elif msg.media:
                if hasattr(msg.media, 'document'):
                    await myprint(str(msg.media.id))
                elif hasattr(msg.media, 'photo'):
                    await myprint(str(msg.photo.id))
#            await myprint(str(type(utils.pack_bot_file_id(msg.photo))))
#            await myprint(str(utils.pack_bot_file_id(msg.photo)))
                else:
                    await myprint(msg.stringify())
            else:
                await myprint(msg.stringify())
        else:
            await myprint("E: can't find msg")
    elif cmd[0] == "file":
        #https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.uploads.UploadMethods.send_file
        #          telethon.utils.pack_bot_file_id(file)
        if len(cmd[1].split('/')) >= 5 and cmd[1].split('/')[2] == "t.me":
            msg = await my_get_from_link(cmd[1])
            file = msg.file
            if msg and msg.media:
                if hasattr(msg.media, 'document'):
                    file = msg.media
                elif hasattr(msg.media, 'photo'):
                    file = msg.photo
            if file:
                msg = await client.send_file(message.chat_id, file=file)
            else:
                await myprint("no file")
        else:
            #          await myprint(msg.stringify())
            #          await myprint("file_id can't work")
            #          file=cmd[1]

            file = utils.resolve_bot_file_id(cmd[1])
            #https://github.com/LonamiWebs/Telethon/issues/1613 #file_id in userbot if different from file_id in bot
            await bot.send_file(log_cid, file=file)
    elif cmd[0] == "mkchat":
        result = await client.functions.messages.CreateChatRequest(
            users=['liqsliu_bot'], title=me.username)
        await myprint(result.stringify())
    elif cmd[0] == "idf":
        peer = await client.get_input_entity(await get_id(cmd[1]))
        #        peer=await client.get_entity(await get_id(cmd[1]))
        #        if not peer:
        #          peer=await client.get_entity(utils.get_peer_id(peer))
        #          peer=await client.get_entity(await get_id(cmd[1]))
        #        if type(peer) == User:
        if type(peer) == InputPeerUser:
            #          peer = await client.functions.users.GetFullUserRequest(id=peer)
            peer = await client(functions.users.GetFullUserRequest(id=peer))
            #            await client.send_message(me.id, peer.stringify())
            #          await myprint(peer.stringify())
            info = str(type(peer)) + ": `" + str(utils.get_peer_id(
                peer.user)) + "`"
#        elif type(peer) == Chat:
        elif type(peer) == InputPeerChat:
            #          peer = await client.functions.messages.GetFullChatRequest(peer.id)
            peer = await client(
                functions.messages.GetFullChatRequest(peer.chat_id))
            info = str(type(peer)) + ": `" + str(
                utils.get_peer_id(peer.full_chat)) + "`"


#        elif type(peer) == Channel:
        elif type(peer) == InputPeerChannel:
            #https://docs.telethon.dev/en/latest/concepts/chats-vs-channels.html
            #megagroups are channels
            #        elif peer.broadcast or peer.megagroup or peer.gigagroup:
            #          peer = await client.functions.channels.GetFullChannelRequest(peer)
            peer = await client(functions.channels.GetFullChannelRequest(peer))
            info = str(type(peer)) + ": `" + str(
                utils.get_peer_id(peer.full_chat)) + "`"
        else:
            peer = await client.get_entity(await get_id(cmd[1]))
            info = "unknown type,not full:" + str(type(peer))
        if len("```\n" + mdraw(peer.stringify(), "code") + "\n```\n\n" +
               info) > MAX_MSG_LEN:
            if len(peer.stringify()) > MAX_MSG_LEN:
                await myprintmd(info)
                await myprint(peer.stringify())
            else:
                await myprint(peer.stringify())
                await myprintmd(info)
        else:
            info = "```\n" + mdraw(peer.stringify(),
                                   "code") + "\n```\n\n" + info
            await myprintmd(info)
    elif cmd[0] == "am":
        if message.text == "am":
            await myprint(str(auto_msg_list))
        elif len(cmd) != 4:
            #          await myprint("id [ctime interval target text]")
            await myprint("am interval target text")

        else:
            ctime = time.time()
            interval = int(cmd[1])
            target = int(cmd[2])
            text = message.text.split(' ', 3)[3]
            item = [ctime, interval, target, text]
            if len(auto_msg_list) == 0:
                max_id = 0
            else:
                max_id = auto_msg_list.keys()[-1]
            auto_msg_list.update({max_id + 1: item})
            await myprint(str(auto_msg_list[max_id + 1]))
    elif cmd[0] == "amadd":
        #        await myprint("id [ctime interval target text]")
        #        await myprint("am interval target text")
        await myprint("am interval target text")
    elif cmd[0] == "amload":
        import ast
        auto_msg_list = ast.literal_eval(message.text.split(' ', 1)[1])
        await myprint(str(auto_msg_list))
    elif cmd[0] == "amdel":
        auto_msg_list.pop(int(cmd[1]))
        await myprint(str(auto_msg_list))
    elif cmd[0] == "amclear":
        auto_msg_list = {}
        await myprint(str(auto_msg_list))
    elif cmd[0] == "af":
        if message.text == "af":
            await myprint(str(auto_forward_list))
        else:
            if len(cmd) == 3:
                auto_forward_list.update({int(cmd[1]): int(cmd[2])})
                await myprint(str(auto_forward_list))
            else:
                await client.send_message(MY_ID, "格式有误: am cid cid")
    elif cmd[0] == "afad":
        await client.send_message(MY_ID, "格式: am cid cid")
    elif cmd[0] == "afload":
        #        import json
        #        auto_forward_list=json.loads(message.text.split(' ',1)[1])
        #        auto_forward_list=eval(message.text.split(' ',1)[1])
        import ast
        auto_forward_list = ast.literal_eval(message.text.split(' ', 1)[1])
        await client.send_message(me.id, str(auto_forward_list))
    elif cmd[0] == "aflist":
        await client.send_message(me.id, str(auto_forward_list))
    elif cmd[0] == "afdel":
        auto_forward_list.pop(int(cmd[1]))
        await client.send_message(me.id, str(auto_forward_list))
    elif cmd[0] == "afclear":
        auto_forward_list = {}
        await client.send_message(me.id, str(auto_forward_list))

    elif cmd[0] == "msgclear":
        if client == bot:
            await client.send_message(me.id, "W: please use userbot")
            return
        if len(cmd) == 1:
            await client.send_message(me.id,
                                      "msgclear http://t.me/... [max_msg_id]")
            return

        url = cmd[1]
        if cmd[1][0] == "@":
            peer = await client.get_entity(cmd[1][1:])
        elif url.split('/')[2] == "t.me":
            if url.split('/')[3] == "c":
                cid = int(url.split('/')[4])
                max_msg_id = int(url.split('/')[5])
            else:
                cid = url.split('/')[3]
                max_msg_id = int(url.split('/')[4])
            peer = await client.get_entity(cid)
        else:
            peer = await client.get_entity(int(cmd[1]))
        if len(cmd) == 3:
            max_msg_id = int(cmd[2])
        if max_msg_id:
            await client.delete_messages(peer,
                                         ids=list(
                                             range(1, max_msg_id + 1)))
            await client.send_message(me.id, "clear ok")
        else:
            await client.send_message(me.id, "格式有误")


async def forward_msg(client, message):
    global auto_forward_list
    chat_id = get_chat_id(message)
    if chat_id in auto_forward_list:
        cid = auto_forward_list[chat_id]
        if cid:
            if message.media_group_id:
                await client.copy_media_group(cid, chat_id, message.id)
            else:
                await message.forward(cid)
    if chat_id in MT_GATEWAY_LIST_for_tg:
        if MT_GATEWAY_LIST_for_tg[chat_id] == "gateway5":  # need not to send in order
            msg = await parse_msg_for_mt(client, message)
            if msg:
                await mt_send(msg[0], msg[1], msg[2], msg[3])



async def update_stdouterr(data):
    while data[2].poll() == None:
        try:
            data[0], data[1] = data[2].communicate(timeout=0.3)
        except subprocess.TimeoutExpired as e:
            if e.stdout:
                data[0] = e.stdout.decode("utf-8")
            if e.stderr:
                data[1] = e.stderr.decode("utf-8")
        await asyncio.sleep(0.1)


async def update_stdout(data):
    while True:
        print(1)
        await asyncio.sleep(0.4)
        tmp = await data[2].stdout.readline()
        if tmp:
            data[0] = data[0] + tmp.decode("utf-8")
        else:
            break
    logger.info(11)


async def update_stderr(data):
    while True:
        print(2)
        await asyncio.sleep(0.2)
        tmp = await data[2].stderr.readline()
        if tmp:
            data[1] = data[1] + tmp.decode("utf-8")
        else:
            break
    logger.info(22)


async def my_popen(cmd,
                   shell=True,
                   max_time=512,
                   client=NB,
                   msg=None,
                   combine=True,
                   return_msg=False,
                   executable='/bin/bash',
                   **args):
    logger.info(cmd)
    #        args=shlex.split(message.text.split(' ',1)[1])

    #        p=subprocess.Popen(message.text.split(' '))
    #        p=subprocess.Popen(message.text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #        p=subprocess.Popen(shlex.split(message.text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)

    #        p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #        p=Popen(args,text=True,universal_newlines=True,bufsize=1,stdout=PIPE, stderr=PIPE)
    #        p=Popen(args,text=True,stdout=PIPE, stderr=PIPE)
    #        p=await asyncio.create_subprocess_shell(message.text.split(' ',1)[1],stdout=PIPE, stderr=PIPE)#limit=None
    #        p=Popen(args,stdout=PIPE, stderr=PIPE,bufsize=8000000)
    #        p=Popen(args,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    #  p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    p = Popen(cmd,
              shell=shell,
              stdout=PIPE,
              stderr=PIPE,
              text=True,
              encoding="utf-8",
              errors="ignore",
              executable=executable)

    #      if client == userbot and message.chat_id < 0:
    #      if client == userbot and message.is_group:
    #      msg=await cmd_answer("...",cmd_msg)

    start_time = time.time()
    info = ""
    errs = ""
    data = ["", "", p]
    asyncio.create_task(update_stdouterr(data))
    await asyncio.sleep(0.5)
    logger.info(str(p.args))
    while True:
        #  if p.poll() == None and p.returncode == None:
        if p.poll() == None:
            pass
        else:
            break
        #  await asyncio.sleep(0.5)
        info = data[0]
        errs = data[1]

        tmp = "...\n" + info + "\n==\nE: \n" + errs
        tmp = tmp.strip()
        if msg:
            if tmp != msg.text:
                try:
                    msg = await cmd_answer(tmp, client, msg, **args)
                except Exception as e:
                    logger.error(f"can not send tmp: {e=}")
                    msg = await client.send_message(MY_ID, tmp)
        await asyncio.sleep(2)
        if time.time() - start_time > max_time:
            p.kill()
            info = "my_popen: timeout, killed, cmd: {}".format(cmd)
            logger.warning(info)
            await cmd_answer(info, client, msg)
            break

    try:
        info, errs = p.communicate(timeout=5)
    except subprocess.TimeoutExpired as e:
        logger.error("timeout")
        info = e.stdout
        errs = e.stderr

    if info:
        if isinstance(info, bytes):
            info = info.decode()
    if errs:
        if isinstance(errs, bytes):
            errs = errs.decode()
    if not info:
        info = "null"


#  info=str(info)
    res = info
    if p.returncode:
        res = info + "\n==\nE: " + str(p.returncode)
        if errs:
            res = res + "\n" + errs
        #await msg.delete()
    logger.debug("popen exit")
    if msg:
        msg = await cmd_answer(res, client, msg, **args)
        if return_msg:
            return msg
    if combine:
        return res
    else:
        return p.returncode, info, errs


async def run_my_bash(cmd, shell=True, max_time=64, cmd_msg=None):
    p = Popen(cmd,
              shell=shell,
              stdout=PIPE,
              stderr=PIPE,
              text=True,
              encoding="utf-8",
              errors="ignore")

    start_time = time.time()
    info = ""
    errs = ""
    msg = None

    await asyncio.sleep(0.5)
    if p.poll() == None and p.returncode == None:
        while p.poll() == None and p.returncode == None:
            if time.time() - start_time > max_time:
                p.kill()
                break
            await asyncio.sleep(1)

    try:
        info, errs = p.communicate(timeout=3)
    except subprocess.TimeoutExpired as e:
        info = e.stdout
        errs = e.stderr

    if not info:
        info = "null"
    info = str(info)
    if p.returncode:
        info = info + "\n==\nE: " + str(p.returncode)
        if errs:
            info = info + "\n" + errs
        #await msg.delete()
    return info


async def my_exec(cmd, client=None, msg=None, **args):
    #  exec(cmd) #return always is None
    #  p=Popen("my_exec.py "+message.text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    #    await my_popen(["python3", "my_exec.py", cmd], shell=False, msg=msg)
    #    await my_popen([ SH_PATH + "/my_exec.py", cmd], shell=False, msg=msg, executable="/usr/bin/python3")
    res = await my_popen(cmd,
                         shell=True,
                         client=client, 
                         msg=msg,
                         executable="/usr/bin/python3",
                         **args)
    return res


async def my_eval(cmd, client=None, msg=None, **args):
    res = eval(cmd)
    logger.info(str(res) + "\n" + str(type(res)))
    res = await cmd_answer(str(res), client=client, msg=msg, **args)
    return res


#    res = await msg.client.send_message(msg.chat_id, str(res))


class MyBash():

    def __init__(self, cmd, msg=None, message=None):
        """msg is needed"""
        self.cmd = cmd
        if message:
            self.msg = message.message
        else:
            self.msg = msg


class T():

    def __init__(self, client=UB, client2=NB):
        self.client = client
        if self.client2 == self.client:
            self.client2 = None
        else:
            self.client2 = client2


async def send_cmd_to_bash(msg):
    """run cmd of text msg from mt by bash(old)"""
    if isinstance(msg, str):
        shell_cmd = ["bash -l", SH_PATH + "/bcmd.sh"]
        shell_cmd.append("just_get_reply")
        shell_cmd.append(msg)
    else:
        if type(msg) == list:
            if not " " in msg[1]:
                msg[1] = "T " + msg[1]
            msg_mt = {
                "text": msg[0],
                "username": "{}: ".format(msg[1]),
                "gateway": msg[2]
            }
            msg = msg_mt
        text = msg["text"]
        name = msg["username"]
        if not text:
            return
        if name.startswith("C "):
            return
        logger.info("run cmd: {}".format(msg))
        #  shell_cmd="{} {} {} {}"
        shell_cmd = ["bash -l", SH_PATH + "/bcmd.sh"]
        shell_cmd.append(msg["gateway"])
        shell_cmd.append(msg["username"])
        shell_cmd.append(msg["text"])
        shell_cmd.append(repr(msg))

        if shell_cmd[1] == "gateway1":
            if my_host_re.match(shell_cmd[3]):
                print("my url")
                shell_cmd[3] = ".ipfs {} only".format(shell_cmd[3])
                shell_cmd[1] = "gateway4"
            elif tw_re.match(shell_cmd[3]):
                print("a twitter")
                shell_cmd[3] = ".tw {}".format(shell_cmd[3])
                shell_cmd[1] = "gateway4"
            elif pic_re.match(shell_cmd[3]):
                print("a pic")
                shell_cmd[3] = ".ipfs {} only".format(shell_cmd[3])
                shell_cmd[1] = "gateway4"
            elif url_only_re.match(shell_cmd[3]):
                print("a url")
                shell_cmd[3] = ".ipfs {} autocheck".format(shell_cmd[3])
                shell_cmd[1] = "gateway4"
    logger.warning("bash cmd: {}".format(shell_cmd))
    #  await run_my_bash(shell_cmd, shell=False)
    #  await my_popen(shell_cmd, shell=False)
    #  await my_popen(" ".join(shell_cmd))
    res = await my_popen(shell_cmd, shell=False)
    logger.info(res)
    return res


async def download_in_bash(msg, *args):
    if isinstance(msg, str):
        shell_cmd = ["bash -l", SH_PATH + "/link_to_file.sh"]
        shell_cmd.append(msg)
        shell_cmd += list(args)
    else:
        return
    return await my_popen(shell_cmd, shell=False, combine=False)
    r,res,e = await my_popen(shell_cmd, shell=False, combine=False)
    if r != 0:
        logger.error(res,e)
    logger.info(res)
    return res


async def __get_msg_id_from_text(text,
                               chat_id=None,
                               name=None,
                               client=UB,
                               protocol=None):
    if not client:
        client = UB

    orig_text = text
    text = text.strip()
    if not text:
        logger.warning("null text, return")
        return None


#  if len(text.splitlines()[0]) > 2:
#    text = text.splitlines()[0]
    logger.info("orig text: {}".format(text))
    if "\n" in text:
        tmp = ""
        for line in text.splitlines():
            if not line:
                break
            else:
                if line.startswith("> "):
                    if tmp:
                        break
                    else:
                        continue
                if not tmp and len(line) > 5:
                    tmp = line
                    break
                elif not tmp and url_only_re.match(line):
                    tmp = line
                    break
                elif url_md_re.match(line):
                    break
                elif url2_md_re.match(line):
                    break
                elif pic_md_re.match(line):
                    break
                else:
                    tmp += line
                    break
        if tmp:
            logger.warning("change text to: {}".format(tmp))
            text = tmp

    my_msg_sender = name
    limit = 10 * int(64 / len(text) + 5)
    if my_msg_sender == "bot":
        limit = limit * 10

    logger.info("user name: {}".format(name))
    user = None
    if name:
        user = await get_peer(name, chat=chat_id, client=client)
        logger.info("find user: {}".format(user))
        if not user:
            logger.warning("not find user: {}".format(name))
    else:
        pass

    if user:
        try:
            if type(user) == list:
                for u in user:
                    async for msg in client.iter_messages(chat_id,
                                                          limit=limit,
                                                          search=text,
                                                          from_user=u):
                        return msg.id
                async for msg in client.iter_messages(chat_id,
                                                      limit=limit,
                                                      from_user=user):
                    if text in msg.text.splitlines():
                        return msg.id
            else:
                async for msg in client.iter_messages(chat_id,
                                                      limit=limit,
                                                      search=text,
                                                      from_user=user):
                    return msg.id
                async for msg in client.iter_messages(chat_id,
                                                      limit=limit,
                                                      from_user=user):
                    if text in msg.text.splitlines():
                        return msg.id
                    if my_jaccard(msg.text, text):
                        return msg.id
        except TypeError:
            logger.warning("can't find replied msg for {}: {}".format(
                name, text))
            pass

    if len(text) > 1:
        async for msg in client.iter_messages(chat_id,
                                              limit=int(limit / 10),
                                              search=text):
            if name:
                if await get_name_for_mt(msg) == name:
                    return msg.id
            else:
                if my_jaccard(msg.text, text):
                    return msg.id
                if msg.text.endswith(text):
                    if msg.text[0] == protocol:
                        return msg.id

    t = 0
#    if "\n\n" in text:
    if "\n" in text and len(text.replace("\n", "")) > 0:
        for line in text.splitlines():
            if line.startswith("> "):
                continue
            if line:
                t += 1
                async for msg in client.iter_messages(chat_id,
                                                      limit=10,
                                                      search=line):
                    if name:
                        if await get_name_for_mt(msg) == name:
                            return msg.id
                    if my_jaccard(msg.text, text):
                        return msg.id
                async for msg in client.iter_messages(chat_id,
                                                      limit=int(limit /
                                                                10)):
                    if my_jaccard(msg.text, text):
                        return msg.id
                    for line2 in msg.text:
                        if line2.startswith("> "):
                            continue
                        if line2 == "":
                            continue
                        if name:
                            if await get_name_for_mt(msg) == name:
                                if line == line2:
                                    return msg.id
                        else:
                            if my_jaccard(line2, line):
                                return msg.id
                            if line2[0] == protocol:
                                if line2.endswith(line):
                                    return msg.id
                if t >= 2:
                    break

    logger.error("can't find msg id for: {}:{}".format(name, orig_text))
    return None


@tg_exceptions_handler
async def get_msg_id_from_text(text,
                               chat_id=None,
                               name=None,
                               client=UB,
                               protocol=None):
    if not client:
        client = UB

    orig_text = text
    text = text.strip()
    if not text:
        logger.warning("null text, return")
        return None


#  if len(text.splitlines()[0]) > 2:
#    text = text.splitlines()[0]
    logger.info("orig text: {}".format(text))
    if "\n" in text:
        tmp = ""
        for line in text.splitlines():
            if not line:
                break
            else:
                if line.startswith("> "):
                    if tmp:
                        break
                    else:
                        continue
                if not tmp and len(line) > 5:
                    tmp = line
                    break
                elif not tmp and url_only_re.match(line):
                    tmp = line
                    break
                elif url_md_re.match(line):
                    break
                elif url2_md_re.match(line):
                    break
                elif pic_md_re.match(line):
                    break
                else:
                    tmp += line
                    break
        if tmp:
            logger.warning("change text to: {}".format(tmp))
            text = tmp

    my_msg_sender = name
    limit = 10 * int(64 / len(text) + 5)
    if my_msg_sender == "bot":
        limit = limit * 10

    logger.info("user name: {}".format(name))
    if name:
        users = await get_peer(name, chat=chat_id, client=client)
        if users:
            if not isinstance(users, list):
                users = [users]
            for user in users:
                async for msg in client.search_messages(chat_id, query=text, limit=limit, from_user=user.id):
                    return msg.id
        else:
            logger.warning("not find user: {}".format(name))
            name = None

    if len(text) > 1:
        async for msg in client.search_messages(chat_id, query=text, limit=int(limit/2)):
            if name:
                for user in users:
                    if user.id == get_sender_id(msg):
                        return msg.id
            else:
                return msg.id
    #  async for msg in client.iter_history(chat_id, limit=64):
    async for msg in client.get_chat_history(chat_id, limit=64):
        if msg.text is None:
            continue
        if name:
            for user in users:
                if user.id == get_sender_id(msg):
                    break
            if user.id != get_sender_id(msg):
                continue
        if msg.text == text:
            return msg.id
        else:
            if my_jaccard(msg.text, text):
                return msg.id
            if msg.text.endswith(text):
                if msg.text[0] == protocol:
                    return msg.id
            if "\n" in text:
                for line in text.splitlines():
                    if line.startswith("> "):
                        continue
                    if line == "":
                        continue
                    for line2 in msg.text.splitlines():
                        if line2.startswith("> "):
                            continue
                        if line2 == "":
                            continue
                        if my_jaccard(line2, line):
                            return msg.id

    logger.error("can't find msg id for: {}:{}".format(name, orig_text))
    return None


wait_for_list = {}


async def set_event(client, msg):
    global wait_for_list
    chat_id = get_chat_id(msg)
    if chat_id in wait_for_list:
        chat = wait_for_list[chat_id]
        if msg.id < chat[5]:
            return
        if chat[4] == 0:
            return
        if chat[3] and chat[3] in msg.text:
            return
        if chat[2]:
            if chat[2] not in msg.text:
                return

        chat[4] -= 1
        if chat[4] == 0:
            message = chat[1]
            message.set()
            chat.append(msg)


# async def get_info_from_bot(text, uid, key=None, skip=None, wait=1, client=UB, return_msg=False):
async def get_info_from_bot(text, uid, key=None, skip=None, wait=1, client=UB, return_msg=False, return_msg_id=False, fun=None):
    global wait_for_list
    chat_id = uid
    info = "info from tg Bot: "

    global wait_for_list

    if chat_id in wait_for_list:
        lock = wait_for_list[chat_id][0]
#        await lock.acquire()
        try:
            await asyncio.wait_for(lock.acquire(), 30)
            #        logger.warning("too many cmd, wait for last reply")
            message = wait_for_list[chat_id][1]
            if message.is_set():
                message.clear()

        except asyncio.TimeoutError:
            wait_for_list.pop(chat_id)


    if chat_id not in wait_for_list:
        lock = asyncio.Lock()
        await lock.acquire()
        message = asyncio.Event()
        if message.is_set():
            message.clear()

    wait_for_list.update({chat_id: [lock, message, key, skip, wait]})


    msg = await client.send_message(chat_id, text)
    wait_for_list[chat_id].append(msg.id)
    try:
        await asyncio.wait_for(message.wait(), timeout=30)
    except asyncio.TimeoutError:
        lock.release()
        return info + "timeout"
#    await asyncio.sleep(5)
    msg_id = msg.id
    if return_msg_id:
        return msg_id
    msg = None
    tmp = None

    if len(wait_for_list[chat_id]) > 6:
        msg = wait_for_list[chat_id][6]
        if msg:
#            if msg.out:
#                continue
            if skip:
                if skip in msg.text:
                    msg = None

            if key:
                if key in msg.text:
                    if fun:
                        tmp = await fun(msg)
                        if tmp:
                            pass
                        else:
                            msg = None
                    pass
                else:
                    msg = None
            else:
                if fun:
                    tmp = await fun(msg)
                    if tmp:
                        pass
                    else:
                        msg = None
                pass
        else:
            pass


    if not msg:
        #  async for msg in client.iter_messages(chat_id, limit=32):
        #  async for msg in client.iter_history(chat_id, limit=64):
        async for msg in client.get_chat_history(chat_id, limit=64):
            if msg:
#            if msg.out:
#                continue
                if skip:
                    if skip in msg.text:
                        continue

                if key:
                    if key in msg.text:
                        if fun:
                            tmp = await fun(msg)
                            if tmp:
                                break
                            else:
                                continue
                        break
                    else:
                        continue
                else:
                    if fun:
                        tmp = await fun(msg)
                        if tmp:
                            break
                        else:
                            continue
                    break
            else:
                break


    if chat_id in wait_for_list:
        lock = wait_for_list[chat_id][0]
        if lock.locked():
            lock.release()
    if msg:
        if return_msg:
            return msg
        else:
            if fun and tmp:
                return info+tmp
            info += "{}".format(msg.text)
            return info
    else:
        logger.error("not get msg")





async def text2link(text, max_len=MAX_MSG_LEN):
    "pastebin or ipfs"
    return await pastebin(text)

    msg = subprocess.run(
        ["bash", SH_PATH + "/change_long_text.sh", text,
         str(max_len)],
        stdout=subprocess.PIPE,
        text=True).stdout
    return msg



async def text2tg(text, chat_id=GID):
    if len(text.encode()) > 4096:
        #  return await ipfs_add(text)
        text = f"splited: {text[:4084]}..."
    if chat_id == MY_ID:
        chat_id = GID
    elif chat_id > 0:
        #  target = await get_peer(chat_id)
        #  if target:
        #      if target.status:
        #          pass
        #      else:
        #          chat_id = GID
        chat_id = GID
    else:
        chat_id = GID
    msg = await NB.send_message(chat_id, text)
    link = await get_msg_link(msg)
    return link


async def get_text_from_msg(url, client=None, chat_id=None):
#    if type(url) == int:
#        url = f"https://t.me/c/{GID}/{url}"
#    url = url.split(" ")[-1]
    info = None
    if type(url) == int:
        if chat_id is None:
            chat_id = GID
        msg = await get_msg(chat_id, ids=url, client=client)
#        print(GID)
#        print(url)
#        print(msg)
        if msg is not None:
            info = msg.text
            if info is None:
                info = "None"
    elif url.startswith("https://t.me/"):
        msg = await get_msg_from_url(url, client)
        if msg is not None:
            info = msg.text
            if info is None:
                info = "None"
    elif url.startswith("https://"):
        info = await http(url)
    else:
        return
    return info



def get_pattern(name):
    pattern = re.compile(r'^(/|\.)?' + name.split('.')[-1] + r'( |$|\n)')
    pattern_bot = re.compile(r'^(/|\.)?' + name.split('.')[-1] + r'(@' +
                             BOT_NAME + r')?( |$|\n)')
    #  p=[check_status_before_cmd, pattern, pattern_bot]
    p = [None, pattern, pattern_bot]
    return p


#    # mentioned:8

# anyone is ok:4
# private is ok:2
# group is ok:1
cmd_dict = {
    "help": [0b111, "cmds"],
    "ping": [0b111, "pong"],
    "dc": [0b111, "dc1?"],
    "start": [0b110, "start"],
    "dg": [0b010, "debug"],
    "an": [0b111, "archivenow"],
    "gfwtest": [0b111, "test"],
    "wm": [0b111, "water mark"],
    "ip": [0b111, "ip info"],
    "down": [0b011, "download"],
    "id": [0b011, "info of"],
    "idf": [0b011, "full info of"],
    "fid": [0b010, "file id"],
    "save": [0b011, "save file or text of msg"],
    "md": [0b011, "print markdown str"],
    "hm": [0b011, "print html str"],
    "p": [0b011, "eval str"],
    "cal": [0b011, "eval str"],
    "pu": [0b011, "unicode"],
    "hex": [0b011, "unicode and hex"],
    "bs": [0b011, "base64 decode"],
    "num": [0b011, "sapce to num"],
    "py": [0b011, "run py code"],
    "sh": [0b011, "run shell code"],
    "uptime": [0b010, "admin only"],
    "exec": [0b011, "admin only"],
    "eval": [0b011, "admin only"],
    "run": [0b011, "admin only"],
    "ns": [0b010, "net speed"],
    "free": [0b010, "free -h"],
    "echo": [0b011, "echo helloworld"],
    "rss": [0b010, "rss add|del|se"],
    "mkchat": [0b010, "creat group"],
    "ad": [0b010, "get admin"],
    "link": [0b010, "get msg info"],
    "msg": [0b011, "get msg, resend"],
    "msgclear": [0b010, "clear msg(userbot)"],  # userbot only
    "up": [0b011, "unpin all"],
    "me": [0b010, "me name"],
    "af": [0b010],
    "afad": [0b010],
    "afload": [0b010],
    "afdel": [0b010],
    "afclear": [0b010],
    "aflist": [0b010],
    "unpin": [0b010],
    "amoad": [0b010],
    "amdel": [0b010],
    "amclear": [0b010],
    "am": [0b010],
    "myid": [0b111, "get my id"]
}



async def faq_get(text='ping',return_res=False):
    pass
    #  res = db.get({"text":text}, "note")
    res = db.search('like ' + text+'|%', key='text', table="note")
    #  if res and res['text'].startswith(text+'|'):
    if res is None:
        return
    for i in res.copy():
        if i["type"] is None:
            res.remove(i)
        if not i['text'].startswith(text+'|'):
            res.remove(i)

    if res:
        if return_res:
            return res
        res = res[0]
        if res:
            return res['text'].split('|', 1)[1]
    else:
        return


##############################


logger = logging.getLogger(__name__)
mp = logger.warning


class _CMD(object):
    def __init__(self):
        self.cmds = {None: []}
        self.check = {}
        self.check_score = {}

    def add_check(self, fun):
        if fun in self.check.values():
            logger.error(f"check existed: {fun.__name__}")
            raise ValueError(f"check existed: {fun.__name__}")
            return
#        bit = 2**len(self.check)
        bit = 1 << len(self.check)
        if bit in self.check:
            logger.error(f"fail to add check: {fun.__name__}")
            raise ValueError(f"fail to add, bit existed, need fix: {bit=} in {self.check=}")
        if hasattr(self, fun.__name__):
            raise ValueError(f"fail to add, name existed, need fix: {bit=} in {self.check=}")
        # exec(f"self.{fun.__name__} = bit")
        setattr(self, fun.__name__, bit)
#        self.check[bit] = fun
        # self.check[bit] = decorator(fun)
        self.check[bit] = fun
        self.check_score[bit] = [0]*4

    def get_bit(self, need):
        bit = 0
        if need:
            for n in need:
                if not n:
                    raise ValueError(f"empty str in need: {cmd=}")
                    return
                tmp = bit
                for b in self.check:
                    if self.check[b].__name__ == n:
                        bit += b
                        break
                if tmp == bit:
                    raise ValueError(f"need is not found, need fix: {cmd=}")
                    return
        return bit


    def add(self, fun, cmd=None, need=None, forbid=None, *args, **kwargs):
        if cmd and cmd in self.cmds:
            raise ValueError(f"fail to add cmd: {cmd=} in {self.cmds=}")
            return
        k = []
        if cmd is None:
            self.cmds[cmd].append(k)
        else:
            self.cmds[cmd] = k
        # k.append(decorator(fun))
        k.append(fun)
#        k.append(self.get_bit(need))
        k.append(need)
        k.append(forbid)
        if k[1] & k[2] > 0:
            print(self.check)
            print(k[1])
            print(k[2])
            raise ValueError(f"need & forbid >0, need fix: {cmd=}")
            return
        if fun.__doc__ is not None:
            k.append(fun.__doc__.strip())

    # async def get_cmd(self, event):
    async def get_cmd(self, client, message):
        " event to cmd, ignore some group msg"
        if message is None:
            return

        cmd = []
        if not is_text(message):
            return
        text = message.text
#            if message.chat_id == cid_wtfipfs and ": " in text:
        if ": " in text:
            sender_id = get_sender_id(message)
            if sender_id:
                pass
            else:
                logger.error("no sender_id, may ignore cmd")

                # sender = await message.get_sender()
                # sender_id = utils.get_peer_id(sender)
            if sender_id == 420415423 or sender_id == TG_BOT_ID_FOR_MT or sender_id == BOT_ID:
                text = text.split(": ", 1)[1]
        text = text.strip()
        cmd = text.split(' ')
        if "\n" in cmd[0]:
            cmd = cmd[0].split('\n', 1) + cmd[1:]
            #      del cmd[2]
            # cmd.pop(2)
        if cmd[0].strip() == "":
            return
        key = cmd[0][0]
        # if client == NB:
        if client.bot_token is not None:
            if is_my_group(message):
                return
            if is_group(message):
#                    if cmd[0].endswith("@{}".format(BOT_NAME)):
                if "@" in cmd[0]:
                    cmd[0] = cmd[0].split("@", 1)[0]
            if key == "/":
                cmd[0] = cmd[0][1:]

        elif is_out(message):
            if key == "/" and "@" not in cmd[0] and not is_bot(message):
                cmd[0] = cmd[0][1:]
            elif key == "$":
                cmd[0] = cmd[0][1:]
            elif key == "'":
                cmd[0] = cmd[0][1:]
            elif key == "_":
                cmd[0] = cmd[0][1:]
            elif key == ".":
                cmd[0] = cmd[0][1:]
            else:
                return
        elif is_my_group(message):
            if key == ".":
                cmd[0] = cmd[0][1:]
            else:
                return
                #  text = await faq_get(text)
                #  await cmd_answer_for_my_group(text, message)

#        return cmd
        if cmd and cmd[0] and cmd[0] in self.cmds:
            if is_my_group(message):
                print(f"get a cmd in my group: {cmd=}")
            return cmd
        else:
            return None

    async def _run(self, client, message, fun):
        if asyncio.iscoroutinefunction(fun):
            return await fun(client, message)
        else:
            return fun(client, message)

    def score(self, k, i):
        b = 1
        while True:
            if b & k != 0:
                self.check_score[b][i] += 1
            elif b > k:
                break

            b = b << 1

    def _check(self, b, client, message):
        self.score(b, 1)
        s = self.check[b](client, message)
        if s is True:
#            self.score(b, 2)
            return True
        else:
#            self.score(b, 3)
            return False

    def _checks(self, k, client, message):
        v = 0
        b = 1
        while True:
            if b & k != 0:
                s = self._check(b, client, message)
                if s is True:
                    v = v | b

            else:
                if b > k:
                    break
                self.score(b, 0)
            b = b << 1
        return v

    #  def _is_ok(self, i, v):
    #      "check v is ok"
    #      if (i[1] | i[2]) & v == i[1]:
    #          self.score((i[1] | i[2]) & (~(v ^ i[1])), 2)
    #          return True
    #      else:
    #          self.score((i[1] | i[2]) & (v ^ i[1]), 3)
    #      return False

    def _is_ok(self, n, f, v):
        "check n f is ok"
        if (n | f) & v == n:
            self.score((n | f) & ~(v ^ n), 2)
            return True
        else:
            self.score((n | f) & (v ^ n), 3)
        return False

    def print_fail_check(self, n, f, v):
        k = (n | f) & (v ^ n)
        s = (n | f) & ~(v ^ n)
        b = 1
        while True:
            if b & k != 0:
                name = self.check[b].__name__
                logger.info("fail: ", b,name)
            elif b & s != 0:
                name = self.check[b].__name__
                logger.info("ok: ", b,name)
            elif b > max(k, s):
                break
            b = b << 1


    async def _check_and_run(self, client, message):
        "check all, one time"
        funs = self.cmds[None].copy()
        cmd = await self.get_cmd(client, message)
        if cmd:
            cmd = cmd[0]
            if get_chat_id(message) == MY_ID:
                func = self.cmds[cmd][0]
                await self._run(client, message, func)
                return True
            else:
                funs.append(self.cmds[cmd])
                cmd = True
        else:
            cmd = False
        k = 0
        for i in funs:
            k = k | i[1] | i[2]
#        v = self._checks(k, message)
        b = 1
        while True:
            if b & k != 0:
                if self._check(b, client, message) is True:
                    v = b
                else:
                    v = 0
                k = 0
                for i in funs.copy():
                    n = b & i[1]
                    f = b & i[2]
                    if n | f != 0 and self._is_ok(n, f, v) is not True:
                        if cmd and funs[-1] == i:
                            cmd = False
                        funs.remove(i)
                    else:
                        k = k | i[1] | i[2]
            elif b > k:
                break
            else:
                self.score(b, 0)
            b = b << 1

        if len(funs) == 0:
            return False
#            logger.warning(f"check: {i[0].__name__}\ncheck result k n f v:\n{bin(k)}\n{bin(i[1])}\n{bin(i[2])}\n{bin(v)}\nok: {(i[1] | i[2]) & v == i[1]}\nlog False: {(i[1] | i[2]) & (v ^ i[1])}\nlog True: {(i[1] | i[2]) & (~(v ^ i[1]))}")
#        logger.info(f"result: {bin(v)}")

        b = 1
        for i in funs:
            await self._run(client, message, i[0])
        return cmd

    async def check_cmd(self, client, message, run=False, cmd=None):
        "check whether the message will start a cmd, warning: not check init"
        if cmd is None:
            cmd = await self.get_cmd(client, message)
            if cmd:
                cmd = cmd[0]
                logger.warning(f"check {cmd=}")
            else:
                return False
        elif cmd not in self.cmds:
            return False
        i = self.cmds[cmd]
        v = self._checks(i[1] | i[2], client, message)
        if self._is_ok(i[1], i[2], v):
            logger.warning(f"will run {cmd=}")
            if run:
                await self._run(client, message, i[0])
            return True
        else:
            logger.warning(f"fail: {cmd}")
            self.print_fail_check(i[1], i[2], v)
        return False

    async def run(self, client, message):
        if message is None:
            return True
        try:
            return await self._check_and_run(client, message)
        except StopPropagation as e:
            return True
            return False
            from .utils.tools import get_traceback
            info = get_traceback(e)
            if message.text == "ping":
                print(info)
                logger.warning("stop message")
            return False

    async def print_cmd(self):
        "just for me"
        info = f"None: {len(self.cmds[None])}"
        for c in self.cmds:
            if c is None:
                o = self.cmds[c]
                for k in o:
                    info += f"\n{k[1]}-{k[2]}={k[0].__name__}"
                    if len(k) > 3:
                        info += f": {k[3]}"
                info += "\n"
                continue
            k = self.cmds[c]
            info += f"\n{c}: {k[1]}-{k[2]}={k[0].__name__}"
            if len(k) > 3:
                info += f": {k[3]}"
        info += "\n"
        info += "\n"
        for c in self.check:
            info += f"\n{c}: {self.check[c].__name__}"

        info += "\n\n: skip check ok bad"
        info += "\n"
#        import json
#        info += json.dumps(self.check_score,indent=2)
        info += "\n".join(f"{self.check[x].__name__}: {self.check_score[x]}" for x in self.check if x in self.check_score)
        if len(info.encode()) > 4096:
            info = info[:2048]
        return info

    async def list_cmd(self, client, message):
        "for others"
        if is_me(client, message):
            name = "my master"
        else:
            #  sender = get_sender(message)
            name = await get_name_for_mt(message)
        info = None
        cmd = await self.get_cmd(client, message)
        info = ""
        if is_my_group(client, message):
            if len(cmd) == 1:
                if cmd[0] == "cmd":
                    pass
                else:
                    info = await file_read(PARENT_DIR / "group_help.txt", "r")
            elif cmd[1] == "xmpp":
                info = await file_read(PARENT_DIR / "group_help_xmpp.txt", "r")
            elif cmd[1] == "tox":
                info = await file_read(PARENT_DIR / "group_help_tox.txt", "r")
            elif cmd[1] == "cmd":
                pass
            elif cmd[1] == "matrix":
                info = await file_read(PARENT_DIR / "group_help_matrix.txt", "r")
            else:
                info = "\nE: need fix\n"
        if not is_my_group(client, message) or cmd == ["cmd"] or cmd == ["help", "cmd"]:
            info += f"cmds for: {name}\n--"
            for i in self.cmds:
                if i is None:
                    continue
                if is_me(client, message):
                    info += f"\n{i}:"
                elif await self.check_cmd(client, message, cmd=i):
                    info += f"\n{i}:"
                else:
                    continue
                if len(self.cmds[i]) > 3:
                    info += f" {self.cmds[i][3]}"
            if is_my_group(client, message):
                info += "\n"
                info += "\n"
                info += "\ncmd menu 2(old):"
                info += "\n--\n"
                info += "\n"
                info += await file_read(PARENT_DIR / "group_cmd.txt", "r")
        return info

CMD = _CMD()


def is_my_group(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    if get_chat_id(message) == cid_wtfipfs:
        return True
    return False
CMD.add_check(is_my_group)

def is_NB(client=UB, message=None):
    if client == NB:
        return True
    return False
CMD.add_check(is_NB)

#  def is_UB2(client=UB, message=None):
#      if client == UB2:
#          return True
#      return False
#  CMD.add_check(is_UB2)

def is_channel(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    #  return bool(message.chat and message.chat.type == "channel")
    return bool(message.chat and message.chat.type == enums.ChatType.CHANNEL)
    if message.is_channel is True and message.chat.broadcast is True:
        return True
    return False
CMD.add_check(is_channel)

def is_new(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    return not bool(message.service)
CMD.add_check(is_new)


def is_bot(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    if bool(message.from_user and message.from_user.is_bot):
        return True
    if bool(message.via_bot):
        return True
    if is_out(message) and message.chat.type == enums.ChatType.BOT:
        return True
    return False

    if hasattr(message, "via_bot_id"):
        if message.via_bot_id is not None:
            return True
    if message.is_private is True and message.chat is not None:
        if message.chat.bot is True:
            return True
    elif message.sender is not None and type(message.sender) == User:
        if message.sender.bot is True:
            return True
    return False

CMD.add_check(is_bot)

def is_out(client=UB, message=None):
    "is out"
    if message is None:
        message = client
        client = UB
    if message.outgoing and isinstance(get_sender(message), User) and get_sender(message).is_self:
        return True
    return False
CMD.add_check(is_out)

def is_UB(client=UB, message=None):
    if client == UB:
        return True
    return False
CMD.add_check(is_UB)


def is_text(client=UB, message=None):
    "has text for cmd"
    if message is None:
        message = client
        client = UB
    return bool(message.text)
#    if message.text is not None:
    if message.text.strip() != "":
        # default ""
        return True
    return False
CMD.add_check(is_text)


def is_me(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    if message.from_user and message.from_user.id == MY_ID:
        return True
    return False


CMD.add_check(is_me)


def is_all(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    return True
# CMD.add_check(is_all)


def is_edit(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    return bool(message.edit_date)


CMD.add_check(is_edit)



def is_not_mentioned_in_group(client=UB, message=None):
    "for cmd"
    if message is None:
        message = client
        client = UB
    if is_group(client=client, message=message):
        if is_out(client=client, message=message):
            return False
        #  elif is_my_group(client=client, message=message) and is_client(message):
        elif is_my_group(client=client, message=message):
            return False
        elif not is_mentioned(client=client, message=message):
            return True
    return False


CMD.add_check(is_not_mentioned_in_group)




def is_album(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    return bool(message.media_group_id)
CMD.add_check(is_album)




def is_grouped(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    return bool(message.media_group_id)
    if message.grouped_id is not None:
        return True
    return False


CMD.add_check(is_grouped)


def is_anon_msg(client=UB, message=None):
    if message is None:
        message = client
        client = UB
    return bool(message.chat and message.sender_chat and message.sender_chat.id != message.chat.id)


CMD.add_check(is_anon_msg)


def is_private(client=UB, message=None):
    "need private"
    if message is None:
        message = client
        client = UB
    #  return bool(message.chat and message.chat.type in {"private", "bot"})
    return bool(message.chat and message.chat.type in {enums.ChatType.PRIVATE, enums.ChatType.BOT})
    if message.is_private is True:
        return True
    return False


CMD.add_check(is_private)


def is_group(client=UB, message=None):
    "need group"
    # print(type(client), type(message))
    if message is None:
        message = client
        client = UB
    #  return bool(message.chat and message.chat.type in {"group", "supergroup"})
    return bool(message.chat and message.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP})
    if message.is_group and not is_channel(client, message):
        return True
    return False


CMD.add_check(is_group)


def is_mentioned(client=UB, message=None):
    if message.mentioned:
        return True
    if client.bot_token is not None:
        name = BOT_NAME
        if is_text(message):
            text = message.text
            if text.split(" ")[0].endswith(f"@{name}"):
                return True
    return False
    if message is None:
        message = client
        client = UB
    return message.mentioned
    if hasattr(message, "mentioned"):
        if message.mentioned is True:
            return True
    return False


CMD.add_check(is_mentioned)


def is_reply(client=UB, message=None):
    "is reply"
    if message is None:
        message = client
        client = UB
    return bool(message.reply_to_message)
    if message.is_reply is True:
        return True
    return False


CMD.add_check(is_reply)


def is_forward(client=UB, message=None):
    "is forward"
    if message is None:
        message = client
        client = UB
    return bool(message.forward_date)
    if message.forward is not None:
        return True
    return False

CMD.add_check(is_forward)



# @NB.on(events.NewMessage)
# @UB.on_message(filters.all)
if "NB" in globals():
    @NB.on_message()
    @NB.on_edited_message()
    @tg_exceptions_handler
    async def _(client, message):
        if await CMD.run(client, message) is True:
            # raise StopPropagation
            await message.stop_propagation()
        else:
            await message.continue_propagation()


if "NB2" in globals():
    @NB2.on_message()
    @NB2.on_edited_message()
    @tg_exceptions_handler
    async def _(client, message):
        if await CMD.run(client, message) is True:
            # raise StopPropagation
            await message.stop_propagation()
        else:
            await message.continue_propagation()


@UB.on_message()
@UB.on_edited_message()
@tg_exceptions_handler
async def _(client, message):
    #  if is_my_group(client, message):
    # if is_me(client, message):
        #  print(message)
    if await CMD.run(client, message) is True:
        await message.stop_propagation()
    else:
        await message.continue_propagation()


if "UB2" in globals():
    @UB2.on_message()
    @UB2.on_edited_message()
    @tg_exceptions_handler
    async def _(client, message):
        # if is_me(client, message):
            # print(message)
        if await CMD.run(client, message) is True:
            await message.stop_propagation()
        else:
            await message.continue_propagation()


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))

    def fun():
        pass

    CMD.add_check(is_me)

    CMD.add("test", fun, need=["is_admin"])
    CMD.add("test error need", fun, need=["is_adminhhh"])

    print(cmds)
    print(check)
    #print(dir(flag))

    #print(flag.need_admin)


else:
    print('{} 运行'.format(__file__))
    need = CMD.is_UB+CMD.is_new
    forbid = CMD.is_out
    CMD.add(set_event, need=need, forbid=forbid)
    asyncio.create_task(send_msg_of_queue(), name="msg_queue")



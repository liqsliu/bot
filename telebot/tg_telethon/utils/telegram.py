from functools import wraps
from telethon import events
from telethon import Button
from telethon.events import StopPropagation

from telethon import TelegramClient, events, sync, utils, functions, types

from telethon.errors import (ChannelPrivateError, ChatWriteForbiddenError,
                             UserIsBlockedError, InterdcCallErrorError,
                             MessageNotModifiedError,
                             InputUserDeactivatedError, MessageIdInvalidError,
                             SlowModeWaitError, FloodWaitError)

from telethon.tl.types import ChannelParticipantsAdmins

from telethon.errors.rpcerrorlist import MessageNotModifiedError, ChatAdminRequiredError, ChannelInvalidError, PeerIdInvalidError, FloodWaitError, MessageEmptyError, QueryIdInvalidError

import subprocess
from subprocess import Popen, PIPE
import traceback

import time

import re

import functools
import io

from telethon.tl.types import PeerChat, PeerUser, PeerChannel, Chat, User, Channel, ChatFull, UserFull, ChannelFull, InputPeerUser, InputPeerChat, InputPeerChannel, MessageEntityTextUrl, MessageMediaUnsupported, MessageMediaWebPage

import asyncio

MSG_QUEUE = asyncio.Queue(512)

MAX_MSG_LEN = 4096
MAX_MSG_LINE = 64
DOWNLOAD_PATH = "/var/www/dav/tmp"
MY_DOMAIN = "liuu.tk"

GID = 1791784114  # private group

#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

from .config import cid_wtfipfs, cid_ipfsrss, cid_tw, cid_ipfsrss, cid_btrss, cid_fw
from .config import MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg, TG_BOT_ID_FOR_MT

from .tools import SH_PATH, ennum, denum, denum_auto, tw_re, pic_re, url_only_re, my_host_re, url_re, url_md_re, url1_md_re, url2_md_re, pic_md_re, text_has_md, mdraw, bot_msg_re, bot_msg_qt_re, discord_id_end_re, my_jaccard, pastebin, ipfs_add, http

from ..bot import *

logger = logging.getLogger(__name__)
mp = logger.info
auto_forward_list = CONFIG[0]
auto_msg_list = CONFIG[1]
feed_list = CONFIG[2]

from telethon import TelegramClient, events, sync, utils, functions, types

# https://github.com/yshalsager/ebook-converter-bot/blob/master/ebook_converter_bot/utils/telegram.py

#from .config import save_config

from random import uniform


def tg_exceptions_handler(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except KeyboardInterrupt:
            logger.error("E: stop by master")
            #            await save_config()
            raise
        except QueryIdInvalidError:
            info = "inline answer is too slow"
            logger.warning(info)
            put(info)
        except StopPropagation:
            logger.debug("stop a event")
            raise
        except (ChannelPrivateError, ChatWriteForbiddenError,
                UserIsBlockedError, InterdcCallErrorError,
                MessageNotModifiedError, InputUserDeactivatedError,
                MessageIdInvalidError):
            info = "E: " + str(sys.exc_info(
            )[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
                sys.exc_info())
            print(info)
            #      mp(info)
            #            logger.exception(info)
            await NB.send_message(MY_ID, info)
            await asyncio.sleep(3)
        except SlowModeWaitError as error:
            await asyncio.sleep(error.seconds)
            await asyncio.sleep(3)
            return tg_exceptions_handler(await func(*args, **kwargs))
        except FloodWaitError as error:
            await asyncio.sleep(error.seconds+uniform(0.5, 1.0))

            return tg_exceptions_handler(await func(*args, **kwargs))

        except:
            info = "E: " + str(sys.exc_info(
            )[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
                sys.exc_info())
            print(info)
            logger.error("error: ", exc_info=True, stack_info=True)
            await NB.send_message(MY_ID, info)
            await asyncio.sleep(3)

    return wrapper


def put(text):
    if len(text) > MAX_MSG_LEN:
        logger.warning("split long msg: {}".format(text[0:MAX_MSG_LINE]))
        text = text[-MAX_MSG_LEN:].splitlines()[-1]

#  await UB.send_message(MY_ID, msg)
    msg = [5, MY_ID, text, {"link_preview": False}]
    try:
#        loop = asyncio.get_event_loop()
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    except Exception as e:
        loop = None
        logger.error(e, exc_info=True, stack_info=True)

    if loop == LOOP:
        logger.info("current thread is main")
        asyncio.create_task(MSG_QUEUE.put(msg))
    else:
        logger.info("current thread is not main")
        future = asyncio.run_coroutine_threadsafe(MSG_QUEUE.put(msg), LOOP)
#        result = future.result()
#        logger.info("put result: {}".format(result))





    #  await MSG_QUEUE.put(msg)
    #  loop = asyncio.get_running_loop()
    #  loop = asyncio.get_event_loop()
    #  loop.create_task(MSG_QUEUE.put(msg), name="put")
    #  loop.call_soon_threadsafe(MSG_QUEUE.put(msg))


@tg_exceptions_handler
async def cmd_answer(text, event=None, msg=None, parse_mode=None):
    logger.info(text)
    if not msg:
        if event:
            msg = event
    if text:
        if type(text) is not str:
            text = str(text)
    else:
        text = "None"
    text = text.strip()
    #  if len(text) > MAX_MSG_LEN or len(text.splitlines()) > MAX_MSG_LINE:
    if len(text) > MAX_MSG_LEN:
        logger.warning("split long msg: {}".format(text[0:MAX_MSG_LINE]))
        #    text="\n".join(text[-MAX_MSG_LEN:].splitlines()[-5:])
        #        text = text[-MAX_MSG_LEN:].splitlines()[-1]
        #        await msg.client.send_message(msg.chat_id, "W: msg is too long, splited")
        if len(text) > 5 * MAX_MSG_LEN:
            mp("use ipfs")
            tmp = await cmd_answer("...", msg)
            text = await text2link(text)
            if tmp.id != msg.id:
                await tmp.delete()
        else:
            mp("need split: {}".format(len(text)))
            text_splited = []
            k = len(text) // MAX_MSG_LEN + 1
            k = len(text) // k
            i = 0
            while i * k < len(text):
                text_splited.append(text[i * k:i * k + k])
                i += 1
            mp("splited: {}".format(len(text_splited)))
            for i in text_splited:
                res = await cmd_answer(i, msg, parse_mode=parse_mode)
            return res
    if msg:
        client = msg.client
        if text == msg.raw_text:
            return msg
        if msg.out and (msg.chat_id != MY_ID or client != UB):
            try:
                if msg.edit_date:
                    d = msg.edit_date
                    w = d.today().timestamp() - d.timestamp()
                    if w < 1.5:
                        return await client.send_message(msg.chat_id, text, parse_mode=parse_mode)

                return await msg.edit(text, parse_mode=parse_mode)
            except MessageNotModifiedError:
                #        msg=await NB.send_message(MY_ID, text)
                msg = await NB.send_message(msg.chat_id,
                                            text,
                                            parse_mode=parse_mode)
                return msg
        else:
            if msg.is_private:
                return await client.send_message(msg.chat_id,
                                                 text,
                                                 parse_mode=parse_mode)
            else:
                return await msg.reply(text, parse_mode=parse_mode)
    else:
        logger.warning("no source msg, send to admin")
        msg = await NB.send_message(MY_ID, text, parse_mode=parse_mode)
        return msg


#        logger.error("answer fail: {}|{}".format(text, msg))

#async def send_msg_of_queue(cid=cid_btrss, wait=False):


@tg_exceptions_handler
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
    msg = [1, chat_id, text, {"reply_to": reply_to, "parse_mode": "md"}]
    return msg


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

    #  def sm(msg):
    #  async def sm(msg, lock):
    @tg_exceptions_handler
    async def smf(msg, client=NB):
        while True:
            try:
                #            await NB.send_message(msg[1], msg[2], **msg[3])
                return await client.send_message(msg[1], msg[2], **msg[3])
            except FloodWaitError as error:
                logger.warning(f"FloodWaitError: {msg=}", exc_info=True)
                if client != UB:
                    await UB.send_message(msg[1], "flood error")
                await asyncio.sleep(error.seconds)
                await client.send_message(MY_ID, "flood error: {}".format(msg))
    #            return await UB.send_message(msg[1], msg[2], **msg[3])


    async def sm(msg):
        nonlocal locks
        lock = locks[msg[1]]

        # https://docs.python.org/zh-cn/3/library/asyncio-sync.html
        #    await lock.acquire()
        async with lock:
            #      await NB.send_message(msg[1], msg[2], **msg[3])
            await smf(msg)
            #      ntime=time.time()
            #      locks.update({msg[1]:[ntime]})
            logger.info("wait for read")
            await asyncio.sleep(wait_time)

#  while i < MAX_AUTO_MSG_TASK_TIME:

    while True:
        if MSG_QUEUE.full():
            info = "E: msg queue is full, cleared!"
            mp(info)
            await NB.send_message(MY_ID, info)
            while not MSG_QUEUE.empty():
                MSG_QUEUE.get()
#        try:
#          MSG_QUEUE.get_nowait()
#        except:
#          break
            asyncio.sleep(5)

        mp("queue size: {}".format(MSG_QUEUE.qsize()))
        mp("waiting...")
        data = await MSG_QUEUE.get()

        # 0: normal msg [0, chat_id, text, {}]
        # 1: from matterbridge
        # 2: rss
        # 3: twitter
        # 4: from tg group (only for cmd answer, not forward msg)

        # 5: from put(), admin log, no flood check

        msg = data
        if data[0] == 0:
            msg = data
        elif data[0] == 5:
            # admin log
            logger.warning("put to master: {}".format(msg))
            try:
                await NB.send_message(MY_ID, msg[2], **msg[3])
#            except:
            except FloodWaitError as e:
                logger.warning(f"FloodWaitError: {msg=}", exc_info=True)
                await UB2.send_message(MY_ID, msg[2], **msg[3])
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
            #      await NB.send_message(msg[1], msg[2], **msg[3])
            await smf(msg, client=NB)
        elif msg[0] == 1:
            #      await NB.send_message(msg[1], msg[2], **msg[3])
            await smf(msg, client=UB2)

        else:
            # slow mode, for rss, twitter...
            if msg[1] in locks:
                pass
            else:
                #      locks.update({msg[1]:[0]})
                #      locks[msg[1]][1]=asyncio.Lock()
                #      locks[msg[1]].append(asyncio.Lock())
                locks.update({msg[1]: asyncio.Lock()})

            if locks[msg[1]]:
                pass
            else:
                mp("wtf <2: {}".format(locks[msg[1]]))

            asyncio.create_task(sm(msg), name=msg[1])
        logger.debug("sent msg: {}".format(msg))


async def get_name_from_peer(peer, event=None):
    if not peer:
        return "unknown"
    peer = await get_peer(peer, event=event)
    if peer:
        if type(peer) == User:
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
                name = str(utils.get_peer_id(peer))
        return name
    else:
        return "null"

        if type(msg.fwd_from.from_id) == PeerChannel:
            fwd_info += "channel(%s)" % str(msg.fwd_from.from_id.channel_id)
        elif type(msg.fwd_from.from_id) == PeerUser:
            fwd_info += "user(%s)" % str(msg.fwd_from.from_id.user_id)
        elif type(msg.fwd_from.from_id) == PeerChat:
            fwd_info += "chat(%s)" % str(msg.fwd_from.from_id.chat_id)
        else:
            fwd_info += str(utils.get_peer_id(peer))
            mp("wtf")


async def get_name_for_mt(event, use_chat=False):
    if event.sender_id == cid_tw:
        return "twitter"
    if use_chat is True:
        peer = event.chat
        if peer is None:
            peer = await event.get_chat()
    else:
        peer = event.sender
        if peer is None:
            peer = await event.get_sender()
    if peer is not None:
        name = await get_name_from_peer(peer)
    else:
        if use_chat is True:
            name = "%s" % event.chat_id
        else:
            if event.sender_id is None:
                name = "%s" % event.chat_id
            else:
                name = "%s" % event.sender_id

    return name


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
#async def send_msg_to_mt(event, edited=False):
async def parse_msg_for_mt(event, edited=False, reply=False):
#    if type(event) == events.newmessage.NewMessage.Event:
#        if event.grouped_id is not None:
#            return
    #  msg=event.message
    msg = event
    chat_id = event.chat_id
    if chat_id in MT_GATEWAY_LIST_for_tg:
        gateway = MT_GATEWAY_LIST_for_tg[chat_id]
    else:
        gateway = "gateway11"
        logger.warning(
            "not found gateway, use default gateway for: {}".format(chat_id))
    logger.debug("msg: {}".format(event.raw_text))

    qt = None
    if not reply and msg.is_reply:
        logger.warning("get qt")
        replied = await event.get_reply_message()
        if replied:
            qt = await parse_msg_for_mt(replied, reply=True)
            if qt:
                qt = "{}{}".format(qt[1], qt[0])
            if 0:
                if replied.sender_id:
                    sender_id = replied.sender_id
                    pass
                else:
                    logger.warning("event not sender_id")
                    sender = await replied.get_sender()
                    sender_id = utils.get_peer_id(sender)
                if sender_id == BOT_ID:
                    qt = """{}""".format(await msg2md(replied))
                else:
                    qt = """T {}: {}""".format(await get_name_for_mt(replied),
                                               await msg2md(replied))
#          mt_send(event.message,gateway="gateway1")
#        mt_send(event, gateway)
#  mt_send(await msg2md(event),username, gateway, qt)

    sender_id = event.sender_id
    #    text = event.raw_text
    #    if sender_id == 420415423 and ": " in event.raw_text:
    text = ""
    if type(event) == events.album.Album.Event:
        for msg in event.messages:
            if text:
                text += "\n"
            text += await msg2md(msg)
            break  # msg2md will parse grouped_id
    elif event.grouped_id:
        text += await msg2md(event)
        grouped_id = msg.grouped_id
        msg_id = event.id
        client = event.client
        if 0:  # msg2md will parse grouped_id
            async for msg in client.iter_messages(chat_id, limit=16, min_id=msg_id+1):
                if not msg:
                    break
                if msg.grouped_id != grouped_id:
                    break
                if text:
                    text += "\n"
                text += await msg2md(msg)
    else:
        text = await msg2md(event)

    username = await get_name_for_mt(event)
    username = "T {}".format(username)
    if gateway == "gateway11":
        if ": " in text:
            if sender_id == BOT_ID:
                username = text.split(": ", 1)[0]
                text = text.split(": ", 1)[1]
            elif sender_id == 420849111:
                # ub2
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
        username = await get_name_for_mt(event, use_chat=True)
        username = "T {}".format(username)

    if gateway == "gateway5":
        # rss from channel
        if username == "T v2ex.com":
            if not "#reply0" in text:
                return
        if not reply and len(text.splitlines()) > 2:
            tmp = "**" + text.split("\n", 1)[0] + "**\n"
            tmp += text.split("\n", 1)[1]
            text = tmp

#                sender = event.sender
#                if not sender:
#                    sender = await event.get_sender()
#                if sender.bot and ": " in event.raw_text:

    if gateway == "gateway11":
        rid = ennum(msg.id)
    else:
        rid = None
#    username = "{}{}: ".format(username, rid if rid is not None else "")
    if rid is not None:
        username = "{}{}: ".format(username, rid)
    else:
        username = "{}: ".format(username)

    #  return [await msg2md(event),username, gateway, qt]
    return [text, username, gateway, qt]

#  return await msg2md(event),username, gateway, qt


def get_another_client(client=UB):
    if client == UB:
        return NB
    else:
        return UB


@tg_exceptions_handler
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

async def download_media(msg):
    path = await msg.download_media(DOWNLOAD_PATH)
    if not path:
        logger.error("fail to default dir")
        path = await msg.download_media(SH_PATH+"/tmp")
    return path

@tg_exceptions_handler
async def media2link(msg, pb=False):
    """download media of msg"""
    client = msg.client
    if client == NB:
        max_file_size = 10000000
    else:
        max_file_size = 64000000

    if msg.media != None:
        if msg.file:
            if msg.file.size > max_file_size:
                return
        path = await msg.download_media(DOWNLOAD_PATH)
        if path:
            if pb:
                with open(path, "rb") as file:
                    data = await asyncio.to_thread(file.read)
                    link = await pastebin(data)
                    return link
            else:
                ipfs = await file_to_ipfs(path)
        else:
            logger.error("down fail")
            return
        if path != None:
            name = path.split('/')[-1]
            #      from .ipfs import file_to_ipfs
            #print('https://liuu.tk/'+path.replace(' ','%20'))
            url = 'https://{}/'.format(MY_DOMAIN) + name.replace(' ', '%20')
            if url:
                if ipfs:
                    return [ipfs + " " + url, name]
                else:
                    return [url, name]
            else:
                return


@tg_exceptions_handler
async def msg2md(event):
    #  client=bot
    msg = event
    client = event.client
    if debug:
        event = msg
        print("#### msg ####")
        print(msg.message.stringify())
        print("#### event ####")
        print(msg.stringify())
        print("#### orig ####")
        print(event.original_update)  #UpdateNewMessage
        print(msg.raw_text)

    text = msg.raw_text
    # just for spoiler
    if msg.media and type(msg.media) == MessageMediaUnsupported:
        #    client=userbot #will get ""
        #    chat = await client.get_entity(msg.chat_id)
        #    msgn = await client.get_messages(chat, ids=msg.id)
        #    msgn = await client.get_messages(msg.chat_id, ids=msg.id)
        #      msgn = await NB.get_messages(msg.chat_id, ids=msg.id)
        #      msgn = await get_another_client().get_messages(msg.chat_id, ids=msg.id)
        client2 = get_another_client(client)
        msgn = await client2.get_messages(msg.chat_id, ids=msg.id)

        if msgn:
            if msgn.raw_text:
                text = msgn.raw_text
            else:
                text = msgn.message

    if text and msg.entities and not pic_md_re.search(text):
        text_fix = {}
        url_index = 0
        urls = []
        for t in msg.entities:
            if type(t) == MessageEntityTextUrl:
                #      if type(t) == MessageEntityUrl:

                url = text[t.offset:t.offset + t.length]
                if url == t.url:
                    s = url_re.match(text, t.offset)
                    if s:
                        if s.group("url") == t.url:
                            #                            continue
                            pass
                        else:
                            info = "E: fixme, url_re may be bad: {} => {} => {}".format(
                                text[t.offset:], s.group("url"), t.url)
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
                    s = url_re.match(text, t.offset)
                    if s:
                        if s.span()[0] < t.offset + t.length:
                            if s.group("url") == t.url:
                                # no need to fix
                                # no fix is better
                                continue
                            else:
                                # may be malicious
                                t.url = t.url + " may be malicious"
                                info = "W: find a bad url: {} => {} => {}".format(
                                    url, s.group("url"), t.url)
                                info += "\nmsg link: "
                                info += await get_msg_link(msg)
                                mp(info)
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

            new_text += "\n"
            url_index = 0
            for url in urls:
                url_index += 1
                new_text += "\n[%s]: %s" % (url_index, url)
                text = new_text

    if client == NB:
        max_file_size = 10000000
    else:
        max_file_size = 64000000
    media = ""
    if msg.file and msg.file.size > max_file_size:
        if text:
            media += "\n\n"
        media = "[file is too big. tg link: {} ]".format(await
                                                         get_msg_link(msg))
    if msg.file and msg.file.size < max_file_size and msg.media and type(
            msg.media) != MessageMediaWebPage and type(
                msg.media) != MessageMediaUnsupported:
        #    print(await get_media(msg))
        res = await media2link(msg)
        if res:
            urls = res[0]
            if len(res) == 2:
                name = res[1]
            else:
                name = "media"
            if text:
                media += "\n\n"
            media += '[{}]({})'.format(name, urls)
            grouped_id = msg.grouped_id
            msg_id = msg.id
            if grouped_id:
                async for msgn in client.iter_messages(
                        event.chat_id,
                        limit=8,
                        ids=list(range(msg_id + 1, msg_id + 4))):

                    #    for id in range(msg_id,msg_id+8):
                    #        msgn = await client.get_messages(chat, ids=id)
                    #        msgn = await client.get_messages(event.chat_id, ids=id)
                    if msgn and msgn.grouped_id == grouped_id:
                        res = await media2link(msgn)
                        if res:
                            urls = res[0]
                            if len(res) == 2:
                                name = res[1]
                            else:
                                name = "media"
                        else:
                            break
                        if msgn.raw_text:
                            media += '\n\n[{}]({})'.format(
                                msgn.raw_text.replace("\n", " "), urls)
                        else:
                            media += '\n[{}]({})'.format(name, urls)
        #        if hasattr(msgn, 'message') and msgn.message:
        #                text+='\n![{}]({})'.format(msgn.message, url)
        #            text+='\n\n[{}]({})'.format(msgn.raw_text.replace("\n", " "), urls)

                    else:
                        break

    if media:
        if not text:
            text = media
        else:
            text += media

    if text:
#        if msg.fwd_from:
        if msg.forward:
            f = msg.forward
            #      fwd_info="Forwarded from "
            fwd_info = "转自 "
            # username? firstname?
            if f.from_name:
                fwd_info += f.from_name
            else:
                fwd_info += await get_name_from_peer(f.from_id,
                                                     event=event)

            fwd_info += ": "
            text = fwd_info + text

        return text
    else:
        return "null"


@tg_exceptions_handler
async def get_peer(name,
                   chat=None,
                   event=None,
                   client=None,
                   no_client2=False,
                   input=False):
    """name: name or id or peer
  chat: name or id or peer"""

    if not name:
        return None
    if client is None:
        if event:
            client = event.client
        else:
            client = UB

    if type(name) == str:
        if chat:
            users = []
            try:
                #        if type(chat) == int:
                #          chat= await get_peer(chat, client=client)
                #          chat=utils.get_peer_id(chat)
                async for user in client.iter_participants(chat, search=name):
                    if user.username:
                        if name != user.username:
                            continue
                    elif user.first_name != name:
                        continue
                    users.append(user)
            except:
                pass
            if users:
                return users
            elif len(name) < 5:
                return None
            logger.warning("not find user: {} in chat".format(name))
        if name.isnumeric():
            id = utils.resolve_id(int(name))[0]
        elif name[0] == "-" and name[1:].isnumeric():
            id = utils.resolve_id(int(name))[0]
        elif name[0] == "@":
            id = name[1:]
        elif len(name.split('/')) >= 4 and name.split('/')[2] == "t.me":
            if name.split('/')[3] == "c":
                id = int(name.split('/')[4])
            elif name.split('/')[3] == "s":
                # username is ok for get_entity
                id = name.split('/')[4]
            else:
                # username is ok for get_entity
                id = name.split('/')[3]
        else:
            id = name
    elif type(name) == int:
        id = utils.resolve_id(name)[0]
    else:
        #    id=utils.resolve_id(name)[0]
        id = name

    peer = None
    if input:
        try:
            peer = await client.get_input_entity(id)
        except (ValueError, PeerIdInvalidError) as e:
            logger.warning("can not find input peer for: {} {}".format(id, e))
            pass
    if peer:
        return peer

    try:
        peer = await client.get_entity(id)
    except (ValueError, PeerIdInvalidError) as e:
        logger.warning("can not find peer for: {} {}".format(id, e))
        pass
    if peer:
        return peer

    client2 = get_another_client(client)
    if input:
        try:
            peer = await client2.get_input_entity(id)
        except (ValueError, PeerIdInvalidError) as e:
            logger.warning("client 2 can not find input peer for: {} {}".format(id, e))
            pass
    if peer:
        return peer

    try:
        peer = await client2.get_entity(id)
    except (ValueError, PeerIdInvalidError) as e:
        logger.warning("client 2 can not find peer for: {} {}".format(id, e))
    return peer


async def get_msg_from_url(url, event=None, client=UB):
    if event:
        client = event.client

#  elif cmd[0] == "link":
#    url=cmd[1]
    msg = None
    if len(url.split('/')) >= 5 and url.split('/')[2] == "t.me":
        cid = await get_id(url)
        id = await get_msg_id(url)
#        msg = await get_msg(cid, ids=id, event=event)
        msg = await get_msg(cid, ids=id, client=client)
        if not msg:
            await client.send_message(
                MY_ID, "E: all clients: can't find the msg: {}".format(url))
            return None
    else:
        await client.send_message(MY_ID, "E: error url: {}".format(url))
        return None
    return msg


def get_client2(client):
    if client == UB:
        return NB
    else:
        return UB


async def get_fwd_info(event):
    if event.forward:
        msgf = event.forward
        info = "fwd: "
        if msgf.saved_from_peer:
            cid = utils.get_peer_id(msgf.saved_from_peer)
            chatf = await get_peer(cid, event=event)
            rcid = utils.resolve_id(cid)[0]
            if chatf.username:
                info += "\nfrom group: https://t.me/" + chatf.username + "/" + str(
                    msgf.saved_from_msg_id)
            else:
                info += "\nfrom group: https://t.me/c/" + str(
                    rcid) + "/" + str(msgf.saved_from_msg_id)
            if chatf.username:
                info += "\ngroup: @" + chatf.username
            info += "\ncid: `" + str(cid) + "`"
            info += " tg://openmessage?chat_id=" + str(rcid)
        if msgf.from_id:
            cid = utils.get_peer_id(msgf.from_id)
            chatf = await get_peer(cid, event=event)
            rcid = utils.resolve_id(cid)[0]
            if msgf.channel_post:
                if chatf.username:
                    info += "\nfrom channel: https://t.me/" + chatf.username + "/" + str(
                        msgf.channel_post)
                else:
                    info += "\nfrom channel: https://t.me/c/" + str(
                        rcid) + "/" + str(msgf.channel_post)
            info += "\nsent by:"
            if chatf.username:
                info += " @" + chatf.username
            else:
                if cid > 0:
                    info += " tg://openmessage?user_id=" + str(rcid)
                else:
                    info += " tg://openmessage?chat_id=" + str(rcid)
            info += "\nfrom id: `" + str(cid) + "`"
        elif msgf.from_name:
            info += "\nsent by:"
            info += "only name: " + msgf.from_name
        else:
            info += "None"
    else:
        info = None
    return info


async def get_msg(chat_id=GID, ids=1, event=None, client=None):
    if client is None:
        if event:
            client = event.client
        else:
            client = UB
    msg = None
    try:
        #        peer = await get_peer(cid, client=client, no_client2=True)
        msg = await client.get_messages(chat_id, ids=ids)
        if not msg:
            raise ValueError
    except (ValueError, PeerIdInvalidError):
        logger.warning("can not get msg")
    if msg:
        return msg
    try:
        client2 = get_client2(client)
        msg = await client2.get_messages(chat_id, ids=ids)
    except (ValueError, PeerIdInvalidError):
        logger.warning("can not get msg")
    if msg:
        return msg
    try:
        msg = await UB2.get_messages(chat_id, ids=ids)
    except (ValueError, PeerIdInvalidError):
        logger.warning("can not get msg")
    return msg


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

#@events.register(events.NewMessage)
#  async def run_cmd_for_bots(event):
#    client = event.client
#  sender=await client.get_input_entity(sender_id)
#  try:
#  if msg.via_bot:
#    return
#  if type(event.peer_id) == PeerUser and chat.bot:
#    return
#  if sender and sender.bot:
#    return


@tg_exceptions_handler
async def myprint(msg,
                  parse_mode="text",
                  event=None,
                  client=None,
                  *args,
                  **kwagrs):
    if client is None:
        if event:
            client = event.client
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
    if event and event.chat_id:
        id = event.chat_id
    else:
        id = MY_ID
    if parse_mode == "md":
        #    return await client.send_message(log_cid, msg, parse_mode=parse_mode)
        #        return await client.send_message(log_cid, msg, parse_mode=parse_mode)

        return await client.send_message(id, msg, parse_mode=parse_mode)
    else:
        return await client.send_message(id, msg)


async def myprintmd(msg, *args, **kwagrs):
    return await myprint(msg, parse_mode="md", *args, **kwagrs)


async def myprintraw(msg, *args, **kwagrs):
    #  return await myprintmd("`"+msg.replace("`","\\`")+"`")
    if len(msg) > MAX_MSG_LEN:
        return await myprint(msg, *args, **kwagrs)
    else:
        return await myprintmd("```\n" + msg + "\n```", *args, **kwagrs)


#    msg=mdraw(msg,"code")


@tg_exceptions_handler
async def get_id(url, event=None):
    """get id"""
    if not url:
        return None
    if event is None:
        client = UB
    else:
        client = event.client
    id = 0
    if type(url) == int:
        id = url
        if id < 0:
            id = utils.resolve_id(id)[0]
        return id
    elif type(url) == str:
        if url[0] == "@":
            #          peer=await client.get_input_entity(cmd[1][1:])
            #          await client.send_message(me.id, str(peer.id))
            #        id=url[1:]
            if False:
                try:
                    peer = await client.get_entity(url[1:])
    #        except ValueError:
                except (ValueError, PeerIdInvalidError) as e:
                    client2 = get_client2(client)
                    peer = await client2.get_entity(url[1:])
            peer = await get_peer(url[1:], event=event)
            id = utils.resolve_id(utils.get_peer_id(peer))[0]
        elif len(url.split('/')) >= 4 and url.split('/')[2] == "t.me":
            if url.split('/')[3] == "c":
                id = int(url.split('/')[4])
            elif url.split('/')[3] == "s":
                peer = await get_peer(url.split('/')[4], event=event)
                id = utils.resolve_id(utils.get_peer_id(peer))[0]
            else:
                peer = await get_peer(url.split('/')[3], event=event)
#                id = peer.id
#                id = utils.get_peer_id(peer)
                id = utils.resolve_id(utils.get_peer_id(peer))[0]
        elif url.isnumeric():
#            id = int(url)
            id = utils.resolve_id(int(name))[0]
        elif url[0] == "-" and url[1:].isnumeric():
            id = utils.resolve_id(int(url))[0]
        else:
#            id = int(url)
            id = utils.resolve_id(utils.get_peer_id(id))[0]

        if "?comment=" in url:
            id = await get_linked_cid(id, event)
        if id:
            return id
        else:
            return None
    else:
        return url


async def get_msg_link(msg):
    """meg to link"""
    if msg.chat is not None and msg.chat.username:
        name = msg.chat.username
    else:
        name = f"c/{utils.resolve_id(msg.chat_id)[0]}"
    return "https://t.me/" + name + "/" + str(msg.id)
    return "msg link: https://t.me/c/" + str(utils.resolve_id(
        msg.chat_id)[0]) + "/" + str(msg.id)


#group
@tg_exceptions_handler
async def get_admins(chat, event=None):

    if event is None:
        client = UB
    else:
        client = event.client
    if type(chat) == str or type(chat) == int:
        #        chat=await client.get_entity(await get_id(chat))
        chat = await get_peer(chat, event=event)
    info = "admin: "
    if chat.username:
        info = info + "@" + chat.username
    try:
        # Filter by admins
        #        async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        try:
            users = await client.get_participants(
                chat, filter=ChannelParticipantsAdmins)
        except ChannelInvalidError:
            client2 = get_client2(client)
            users = await client2.get_participants(
                chat, filter=ChannelParticipantsAdmins)
        for user in users:
            #      for user in await client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            #        print(user.first_name)
            info = info + "\n"
            if user.bot:
                info = info + "bot"
            else:
                info = info + str(user.id)
            if user.username:
                info = info + " @" + user.username
            if user.first_name:
                info = info + " " + user.first_name
    except ChatAdminRequiredError:
        info = "E: need admin"
        if event.chat_id == MY_ID and chat.broadcast:
            info = info + ", but:\n"
            info = info + str(await get_admin_of_channel(chat.id, event))
    return info


#small group: Chat
@tg_exceptions_handler
async def get_admin_of_group(msg, event=None):
    if event is None:
        client = UB
    else:
        client = event.client
    peer = await get_peer(msg, event)
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
@tg_exceptions_handler
async def get_admin_of_channel(msg, event=None):
    if event is None:
        client = UB
    else:
        client = event.client
#  id=await get_id(msg)
#      peer=await client.get_entity(await get_id(msg))
    peer = await get_peer(msg, event)
    #  if type(peer) == User:
    #  if type(peer) == Channel:
    #      if peer.broadcast or peer.megagroup or peer.gigagroup:
    if peer.broadcast:
        info = "id: `" + str(utils.get_peer_id(peer))
        if peer.username:
            info = info + "` @" + peer.username
        else:
            info = info + "` no username, tg://openmessage?chat_id=" + str(
                peer.id)
        try:
            full = await client(functions.channels.GetFullChannelRequest(peer))
        except:
            client2 = get_client2(client)
            full = await client2(functions.channels.GetFullChannelRequest(peer)
                                 )
        full_chat = full.full_chat
        if full_chat.exported_invite:
            id = str(full_chat.exported_invite.admin_id)
            info = info + "\nadmin id: `" + id + "` tg://openmessage?user_id=" + id
        elif full_chat.linked_chat_id:
            info = info + "\nlinked id: `" + str(
                utils.get_peer_id(types.PeerChannel(full_chat.linked_chat_id)))
            if len(full.chats) == 2:
                if full.chats[1].username:
                    info = info + "` @" + full.chats[1].username
                else:
                    info = info + "` no username, tg://openmessage?chat_id=" + str(
                        full_chat.linked_chat_id)
            else:
                info = info + "` unknown group, tg://openmessage?chat_id=" + str(
                    full_chat.linked_chat_id)
#          if peer.broadcast:
#        info=info+"\n==\n"+await get_admin_of_channel(peer.id)
            info = info + "\n" + (await get_admins(full_chat.linked_chat_id,
                                                   event=event))
        else:
            info = info + "\nno linked group or channel"


#      elif type(peer) == Chat:
#        info=await get_admin_of_group(peer.id)
    elif type(peer) == Chat or type(peer) == Channel:
        info = await get_admins(peer, event=event)
    else:
        #    await myprint(peer.stringify())
        info = "wtf: " + str(type(peer)) + " " + str(utils.get_peer_id(peer))
    return info


@tg_exceptions_handler
async def get_linked_cid(id, event=None):
    if event is None:
        client = UB
    else:
        client = event.client
    peer = await client.get_input_entity(id)
    if not peer:
        peer = await client.get_input_entity(await get_peer(id, event=event))
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


#https://docs.python.org/3/library/asyncio-task.html#asyncio.run
async def download_media(msg, event=None):
    if event:
        client = event.client
    else:
        if msg:
            client = msg.client
        else:
            client = UB
    msg_before_return = [None]

    async def download_media_callback(current, total):
        """  # Printing download progress  #https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.downloads.DownloadMethods.download_media """

        nonlocal msg_before_return
        #      print('Downloaded', current, 'out of', total,'bytes: {:.2%}'.format(current / total))
        #      await myprint('Downloaded', current, 'out of', total,'bytes: {:.2%}'.format(current / total))
        msg_before_return[0] = (
            'Downloaded ' + str(current) + ' out of ' + str(total) +
            ' bytes: {:.2%}'.format(current / total)).strip()

#    nonlocal msg_before_return

    task = asyncio.create_task(
        msg.download_media(file=DOWNLOAD_PATH + "/",
                           progress_callback=download_media_callback))
    last_msg = ""
    msg = ""
    while True:
        await asyncio.sleep(1)
        if task.done():
            break
        elif not msg_before_return[0]:
            if last_msg != msg_before_return[0]:
                last_msg = msg_before_return[0]
                #            await myprint(msg_before_return)
                if msg:
                    await msg.edit(msg_before_return)
                else:
                    msg = await client.send_message(msg.chat_id,
                                                    msg_before_return)


#      msg.delete()
    return task.result()


async def my_method(custom_method):
    result = await client(
        functions.bots.SendCustomRequestRequest(
            custom_method=custom_method,
            params=types.DataJSON(data='some string here')))
    await myprint(result.stringify())


@tg_exceptions_handler
async def update_profile(msg):
    client = UB
    result = await client(
        functions.account.UpdateProfileRequest(first_name='some string here',
                                               last_name='some string here',
                                               about='some string here'))
    await myprint(result.stringify())


@tg_exceptions_handler
async def update_name(msg):
    client = UB
    #      result = await client(functions.account.UpdateProfileRequest(
    result = await client(
        functions.account.UpdateProfileRequest(first_name=msg))
    await myprint(result.stringify())


@tg_exceptions_handler
async def ban_chat(chat, target, event=None):
    if event is None:
        client = UB
    else:
        client = event.client
    chat = await get_peer(chat, event=event)
    target = await get_peer(target, event=event)
    result = await client(
        functions.channels.EditBannedRequest(
            channel=chat,
            participant=target,
            banned_rights=types.ChatBannedRights(view_messages=True,
                                                 send_messages=False,
                                                 send_media=False,
                                                 send_stickers=False,
                                                 send_gifs=False,
                                                 send_games=False,
                                                 send_inline=False,
                                                 send_polls=False,
                                                 change_info=False,
                                                 invite_users=False,
                                                 pin_messages=False,
                                                 until_date=0)))

    info = "ban result: {}".format(result)
    logger.info(info)
    await cmd_answer(info)



async def set_bot_cmd(event):

    client = event.client
    if client != NB:
        return

    tg_cmd = "help ping myid dc uptime free"

    commands = []
    buttons=[]
    for i in tg_cmd.split(" "):
        if event.is_private:
            if 0b010 & cmd_dict[i][0] == 0:
                continue
        if event.is_group:
            if 0b001 & cmd_dict[i][0] == 0:
                continue
        if event.chat_id != MY_ID:
            if 0b100 & cmd_dict[i][0] == 0:
                continue

        if len(cmd_dict[i]) > 1:
            commands.append(
                types.BotCommand(command=i, description=cmd_dict[i][1]))
        else:
            commands.append(types.BotCommand(command=i, description=i))
        if event.is_group:
            i = "/"+i
#        buttons.append(Button.text(i, resize=True, single_use=True))
        buttons.append(Button.text(i, resize=True, single_use=False))
    if buttons:
        tmp=[[]]
        for i in buttons:
            if len(tmp[-1]) == 4:
                tmp.append([])
            tmp[-1].append(i)

        buttons = tmp

    scope = types.BotCommandScopeDefault()
    if event.chat_id != MY_ID:
        if event.is_private:
            #          scope=types.BotCommandScopeDefault()
            #          scope=types.BotCommandScopePeer(await get_peer(event.sender_id))
            scope = types.BotCommandScopeUsers()
        elif event.is_group:
            scope = types.BotCommandScopeChats()
#          scope=types.BotCommandScopePeer(await get_peer(event.chat_id))
#          scope=types.BotCommandScopeChatAdmins() #for admin of group https://core.telegram.org/constructor/botCommandScopeChatAdmins
    else:
        #      peer=await bot.get_input_entity(event.chat_id)
        if event.is_private:
            if event.sender:
                peer = event.sender
            else:
                peer = await get_peer(event.sender_id, event=event, input=True)
            peer = await client.get_input_entity(peer)
            #          scope=types.BotCommandScopeDefault()
            #          scope=types.BotCommandScopePeerAdmins(peer=event.chat_id)
            #          peer=await bot.get_input_entity(event.chat_id)
            #          peer=await bot.get_entity(event.chat_id)
            #          scope=types.BotCommandScopePeerAdmins(peer)
            scope = types.BotCommandScopePeer(peer)
        elif event.is_group:
            if event.chat:
                peer = event.chat
            else:
                peer = await get_peer(event.chat_id, event=event, input=True)
            peer = await client.get_input_entity(peer)
            #          scope=types.BotCommandScopeChatAdmins()
            #          scope=types.BotCommandScopeDefault()
            scope = types.BotCommandScopePeerUser(peer, MY_ID)
#      result = await client(functions.bots.SetBotCommandsRequest(
    try:
        await client(
            functions.bots.SetBotCommandsRequest(
                scope=scope,
                #        lang_code='en',
                #        lang_code='zh-hans',
                lang_code='',
                commands=commands))

        # await NB.send_message(event.chat_id, 'Welcome', buttons=[Button.text('Thanks!', resize=True, single_use=True),Button.request_phone('Send phone'),Button.request_location('Send location')])


        if buttons:
            await NB.send_message(event.chat_id, 'button is ok', buttons=buttons)
    except:
        logger.error(peer.stringify())
        raise


#    async def admin_cmd(cmd=[]):
@tg_exceptions_handler
async def run_cmd(cmd=[], event=None, client=None):
    if client is None:
        if event:
            client = event.client
        else:
            client = UB

    global auto_forward_list, debug, auto_msg_list, feed_list
    auto_forward_list = CONFIG[0]
    auto_msg_list = CONFIG[1]
    feed_list = CONFIG[2]

    chat_id = event.chat_id
    sender_id = event.sender_id
    chat = event.chat
    sender = event.sender
    msg = event.message

    if cmd[0] == "ping":
        if len(cmd) == 1:
            #          await client.send_message(event.chat_id, "pong")
            await event.reply("pong")
    elif cmd[0] == "dc":
        pass
    elif cmd[0] == "help":
        if client == NB:
            await set_bot_cmd(event)
        await client.send_message(event.chat_id, "use cmd")
    elif cmd[0] == "start":
        if client == bot:
            await set_bot_cmd(event)
        await client.send_message(event.chat_id, "ok")
    elif cmd[0] == "dg":
        if len(cmd) == 1:
            debug = not debug
        await myprint(str(debug))
    elif cmd[0] == "myid" and len(cmd) == 1:
        if event.is_private:
            await event.reply(str(sender_id))
        else:
            if event.is_reply:
                replied = await event.get_reply_message()
                if replied:
                    await event.reply(str(replied.sender_id))
            else:
                await event.reply(str(sender_id))

    elif cmd[0] == "save":
        await save_config()
        await client.send_message(
            event.chat_id,
            str([auto_forward_list, auto_msg_list,
                 feed_list]).replace(" ", "").strip())
    elif cmd[0] == "unpin":
        peer = await client.get_input_entity(await get_id(cmd[1]))
        if not peer:
            peer = await client.get_entity(await get_id(cmd[1]))
        result = await client(functions.messages.UnpinAllMessagesRequest(peer))
        await client.send_message(event.chat_id, result.stringify())
    elif cmd[0] == "me":
        if len(cmd) == 1:
            await client.send_message(event.chat_id, "me name|all text")
        elif cmd[1] == "name":
            await update_name(event.raw_text.split(" ", 2)[2])

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
        #        msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md', schedule=timedelta(seconds=delay))
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
                msg = await client.send_file(event.chat_id, file=file)
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
        if event.raw_text == "am":
            await myprint(str(auto_msg_list))
        elif len(cmd) != 4:
            #          await myprint("id [ctime interval target text]")
            await myprint("am interval target text")

        else:
            ctime = time.time()
            interval = int(cmd[1])
            target = int(cmd[2])
            text = event.raw_text.split(' ', 3)[3]
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
        auto_msg_list = ast.literal_eval(event.raw_text.split(' ', 1)[1])
        await myprint(str(auto_msg_list))
    elif cmd[0] == "amdel":
        auto_msg_list.pop(int(cmd[1]))
        await myprint(str(auto_msg_list))
    elif cmd[0] == "amclear":
        auto_msg_list = {}
        await myprint(str(auto_msg_list))
    elif cmd[0] == "af":
        if event.raw_text == "af":
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
        #        auto_forward_list=json.loads(event.raw_text.split(' ',1)[1])
        #        auto_forward_list=eval(event.raw_text.split(' ',1)[1])
        import ast
        auto_forward_list = ast.literal_eval(event.raw_text.split(' ', 1)[1])
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
                                         message_ids=list(
                                             range(1, max_msg_id + 1)))
            await client.send_message(me.id, "clear ok")
        else:
            await client.send_message(me.id, "格式有误")


async def forward_msg(event):
    client = event.client
    global auto_forward_list
    chat_id = event.chat_id
    #https://www.runoob.com/python/att-dictionary-has_key.html
    #    elif chat_id in auto_forward_list and not await is_debug("auto_forward"):
    if chat_id in auto_forward_list:
        #      schat=utils.resolve_id(chat_id)[1]
        #      schat=await client.get_entity(chat_id)
        cid = auto_forward_list[chat_id]
        # chat=await client.get_entity(cid)
        #      chat=PeerChannel(cid)
        #      chat=utils.resolve_id(cid)[1]
        #    chat=await client.get_input_entity(cid)
        chat = cid
        if chat:
            # msg = event.message
            if event.grouped_id:
                if type(event) == events.album.Album.Event:
                    pass
                else:
                # if type(event) == events.newmessage.NewMessage.Event:
                    return
            await event.forward_to(cid)


@tg_exceptions_handler
async def update_stdouterr(data):
    while data[2].poll() == None:
        await asyncio.sleep(0.1)
        try:
            data[0], data[1] = data[2].communicate(timeout=0.2)
        except subprocess.TimeoutExpired as e:
            if e.stdout:
                data[0] = e.stdout.decode("utf-8")
            if e.stderr:
                data[1] = e.stderr.decode("utf-8")


@tg_exceptions_handler
async def update_stdout(data):
    while True:
        print(1)
        await asyncio.sleep(0.2)
        tmp = await data[2].stdout.readline()
        if tmp:
            data[0] = data[0] + tmp.decode("utf-8")
        else:
            break
    logger.info(11)


@tg_exceptions_handler
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


@tg_exceptions_handler
async def my_popen(cmd,
                   shell=True,
                   max_time=512,
                   msg=None,
                   combine=True,
                   executable='/bin/bash',
                   **args):
    mp(cmd)
    #        args=shlex.split(event.raw_text.split(' ',1)[1])

    #        p=subprocess.Popen(event.raw_text.split(' '))
    #        p=subprocess.Popen(event.raw_text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #        p=subprocess.Popen(shlex.split(event.raw_text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)

    #        p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #        p=Popen(args,text=True,universal_newlines=True,bufsize=1,stdout=PIPE, stderr=PIPE)
    #        p=Popen(args,text=True,stdout=PIPE, stderr=PIPE)
    #        p=await asyncio.create_subprocess_shell(event.raw_text.split(' ',1)[1],stdout=PIPE, stderr=PIPE)#limit=None
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

    #      if client == userbot and event.chat_id < 0:
    #      if client == userbot and event.is_group:
    #      msg=await cmd_answer("...",cmd_msg)

    start_time = time.time()
    await asyncio.sleep(0.5)
    #        await myprintraw(str(args))
    logger.info(str(p.args))
    if p.poll() == None and p.returncode == None:
        info = ""
        errs = ""
        data = ["", "", p]
        asyncio.create_task(update_stdouterr(data))
        while p.poll() == None and p.returncode == None:
            if time.time() - start_time > max_time:
                p.kill()
                info = "my_popen: timeout, killed, cmd: {}".format(cmd)
                logger.error(info)
                await cmd_answer(info, msg)
                break
            await asyncio.sleep(0.5)
            info = data[0]
            errs = data[1]

            tmp = "running...\n" + info + "\n==\nE: \n" + errs
            tmp = tmp.strip()
            if msg:
                if tmp != msg.raw_text:
                    try:
                        msg = await cmd_answer(tmp, msg, **args)
                    except MessageNotModifiedError:
                        logger.error("E: wtf? MessageNotModifiedError")
                        await asyncio.sleep(2)
                    except:
                        logger.error("can not send tmp")
                        msg = await NB.send_message(MY_ID, tmp)
            else:
                pass
            await asyncio.sleep(2)

    try:
        info, errs = p.communicate(timeout=5)
    except subprocess.TimeoutExpired as e:
        logger.error("wait timeout")
        info = e.stdout
        errs = e.stderr

    if info:
        if type(info) == bytes:
            info = info.decode()
    if errs:
        if type(errs) == bytes:
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
    logger.info("popen exit")
    if msg:
        msg = await cmd_answer(res, msg, **args)
    if combine:
        return res
    else:
        return p.returncode, info, errs


@tg_exceptions_handler
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


@tg_exceptions_handler
async def my_exec(cmd, msg=None, **args):
    #  exec(cmd) #return always is None
    #  p=Popen("my_exec.py "+event.raw_text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    #    await my_popen(["python3", "my_exec.py", cmd], shell=False, msg=msg)
    #    await my_popen([ SH_PATH + "/my_exec.py", cmd], shell=False, msg=msg, executable="/usr/bin/python3")
    res = await my_popen(cmd,
                         shell=True,
                         msg=msg,
                         executable="/usr/bin/python3",
                         **args)
    return res


@tg_exceptions_handler
async def my_eval(cmd, msg=None, **args):
    res = eval(cmd)
    logger.info(str(res) + "\n" + str(type(res)))
    res = await cmd_answer(str(res), msg, **args)
    return res


#    res = await msg.client.send_message(msg.chat_id, str(res))


class MyBash():

    def __init__(self, cmd, msg=None, event=None):
        """msg is needed"""
        self.cmd = cmd
        if event:
            self.msg = event.message
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
    if type(msg) == str:
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


#  print(res)


async def get_msg_id_from_text(text,
                               chat_id=None,
                               name=None,
                               client=None,
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
                    if text in msg.raw_text.splitlines():
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
                    if text in msg.raw_text.splitlines():
                        return msg.id
                    if my_jaccard(msg.raw_text, text):
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
                if my_jaccard(msg.raw_text, text):
                    return msg.id
                if msg.raw_text.endswith(text):
                    if msg.raw_text[0] == protocol:
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
                    if my_jaccard(msg.raw_text, text):
                        return msg.id
                async for msg in client.iter_messages(chat_id,
                                                      limit=int(limit /
                                                                10)):
                    if my_jaccard(msg.raw_text, text):
                        return msg.id
                    for line2 in msg.raw_text:
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

wait_for_list = {}


async def set_event(msg):
    global wait_for_list
    chat_id = msg.chat_id
    if chat_id in wait_for_list:
        chat = wait_for_list[chat_id]
        if msg.id < chat[5]:
            return
        if chat[4] == 0:
            return
        if chat[3] and chat[3] in msg.raw_text:
            return
        if chat[2]:
            if chat[2] not in msg.raw_text:
                return

        chat[4] -= 1
        if chat[4] == 0:
            event = chat[1]
            event.set()


# async def get_info_from_bot(text, uid, key=None, skip=None, wait=1, client=UB, return_msg=False):
async def get_info_from_bot(text, uid, key=None, skip=None, wait=1, client=UB2, return_msg=False, return_msg_id=False, fun=None):
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
            event = wait_for_list[chat_id][1]
            if event.is_set():
                event.clear()
            wait_for_list[chat_id][2] = key
            wait_for_list[chat_id][3] = skip
            wait_for_list[chat_id][4] = wait
        except asyncio.TimeoutError:
            wait_for_list.pop(chat_id)


    if chat_id not in wait_for_list:
        lock = asyncio.Lock()
        await lock.acquire()
        event = asyncio.Event()
        if event.is_set():
            event.clear()
        wait_for_list.update({chat_id: [lock, event, key, skip, wait]})
        wait_for_list[chat_id].append(0)

    msg = await client.send_message(chat_id, text)
    wait_for_list[chat_id][5] = msg.id
    try:
        await asyncio.wait_for(event.wait(), timeout=30)
    except asyncio.TimeoutError:
        return info + "timeout"
#    await asyncio.sleep(5)
    msg_id = msg.id
    if return_msg_id:
        return msg_id
#        msg = await client.get_messages(chat_id, ids=msg.id+1)
#    async for msg in client.iter_messages(chat_id, ids=list(range(msg_id + 1, msg_id + 64))):
    # https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.get_messages
#    async for msg in client.iter_messages(chat_id, min_id=msg_id+1, limit=64, from_user=chat_id):
    msg = None
    tmp = None
    async for msg in client.iter_messages(chat_id, limit=32):
        if msg:
#            if msg.out:
#                continue
            if skip:
                if skip in msg.raw_text:
                    continue

            if key:
                if key in msg.raw_text:
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
            info += "{}".format(msg.raw_text)
            return info
    else:
        logger.error("not get msg")



from .tools import pastebin, ipfs_add


async def text2link(text, max_len=MAX_MSG_LEN):
    "pastebin or ipfs"
    return await pastebin(text)

    msg = subprocess.run(
        ["bash", SH_PATH + "/change_long_text.sh", text,
         str(max_len)],
        stdout=subprocess.PIPE,
        text=True).stdout
    return msg



async def text2tg(text):
    if len(text.encode()) > 4096:
        return await ipfs_add(text)
    msg = await NB.send_message(GID, text)
    link = await get_msg_link(msg)
    return link


async def get_text_from_msg(url, event=None):
    if type(url) == int:
        url = f"https://t.me/c/{GID}/{url}"
    info = None
    url = url.split(" ")[-1]
    if url.startswith("https://t.me/"):
        msg = await get_msg_from_url(url, event)
        if msg is not None:
            info = msg.raw_text
            if info is None:
                info = "None"
    else:
        info = await http(url)
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






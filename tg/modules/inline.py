from . import *
import struct


#from telethon.errors.rpcerrorlist import QueryIdInvalidError
# from telethon.errors.rpcerrorlist import MessageTooLongError, ButtonUrlInvalidError

from ..config import SH_PATH
from ..utils.tools import encode_base64, decode_base64
from ..utils.tools import enstr, destr, chr_list, ennum, denum
from ..utils.tools import get_from_url, url_only_re, ipfs_add, pastebin, http, save_to_telegraph, rgb_re



from ..telegram import text2link, get_id, text2tg, get_text_from_msg, DOWNLOAD_PATH, tg_exceptions_handler, get_msg

import os
import io
# from telethon import Button
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto)


logger = logging.getLogger(__name__)
mp = logger.info

ERROR_INFO = "error, contact to @liqsliu please"


def add(res, title, des, text, buttons=None):
    if buttons:
        reply_markup=InlineKeyboardMarkup(buttons)
    else:
        reply_markup = None
#        res.append(InlineQueryResultArticle(title, description=des, input_message_content=InputTextMessageContent(text)))
    res.append(InlineQueryResultArticle(title, description=des, input_message_content=InputTextMessageContent(text, None), reply_markup=reply_markup))



#def get_text(event, m):
def get_text(event):
    # text = event.text
    text = event.query
    if text:
        pass
    else:
        return None, None
    key = text.split(" ", 1)[0]
    if event.offset:
        key = event.offset
    elif key in cmds:
        # if key != text:
        if len(text) - len(key) > 1:
            text = text.split(" ", 1)[1]
        else:
            text = None
    else:
        # key = None
        key = cmds_list[0]
    if text is not None:
        text = text.strip()
        # if text[:1] == MARK:
        # text = f"{MARK}{text}"
        if text == "":
            text = None
    return text, key


MAX_MSG_LEN = 200  # for inline


def split_text(text):
    text = text.strip()
#    if len(text.encode()) > 4096:
    if len(text.encode()) > MAX_MSG_LEN:
        text = text[:MAX_MSG_LEN]
        if len(text.encode()) > MAX_MSG_LEN:
            text = text[:MAX_MSG_LEN//2]
        text = text.strip()
        text = "{}\n...".format(text)
        return text
    else:
        return text




async def _download_media(msg):
    def _down(msg):
#        path = await msg.download_media(DOWNLOAD_PATH)
#        path = asyncio.run(msg.download_media(DOWNLOAD_PATH))
        async def __down(msg, fut):
            print(msg.stringify())
            path = await msg.download_media(DOWNLOAD_PATH)
            if not path:
                print("fail to default dir")
                path = await msg.download_media(SH_PATH+"/tmp")
            print(path)
            fut.set_result(path)
            print("future ok")
#        loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        fut = loop.create_future()
        loop.create_task(__down(msg, fut))
        path = loop.run_until_complete(fut)

        return path
#    path = await asyncio.to_thread(msg.download_media, DOWNLOAD_PATH)
    path = await asyncio.to_thread(_down, msg)
    return path

async def _download_media(msg):
    def _down(msg):
        async def __down(msg):
            print(msg.stringify())
            path = await msg.download_media(DOWNLOAD_PATH)
            if not path:
                print("fail to default dir")
                path = await msg.download_media(SH_PATH+"/tmp")
            return path
        path = asyncio.run(__down(msg))

        return path
    path = await asyncio.to_thread(_down, msg)
    return path


import threading

async def _download_media(msg):
    fut = LOOP.create_future()
    def _down(msg=msg, fut=fut):
#        path = await msg.download_media(DOWNLOAD_PATH)
#        path = asyncio.run(msg.download_media(DOWNLOAD_PATH))
        async def __down(msg=msg):
            print(msg.stringify())
            path = await msg.download_media(DOWNLOAD_PATH)
            if not path:
                print("fail to default dir")
                path = await msg.download_media(SH_PATH+"/tmp")
            return path
        path = asyncio.run(__down())
        fut.set_result(path)

#    path = await asyncio.to_thread(msg.download_media, DOWNLOAD_PATH)
#    path = await asyncio.to_thread(_down, msg)
    t_1 = threading.Thread(target=_down, daemon=True)
    t_1.start()
    await fut
    path = fut.result()

    return path

async def _download_media(msg):
    fut = LOOP.create_future()
    def _down(msg=msg, fut=fut):
#        path = await msg.download_media(DOWNLOAD_PATH)
#        path = asyncio.run(msg.download_media(DOWNLOAD_PATH))
        async def __down(msg=msg):
            print(msg.stringify())
            path = await msg.download_media(DOWNLOAD_PATH)
            if not path:
                print("fail to default dir")
                path = await msg.download_media(SH_PATH+"/tmp")
            return path
        path = asyncio.run(__down())
        fut.set_result(path)

#    path = await asyncio.to_thread(msg.download_media, DOWNLOAD_PATH)
#    path = await asyncio.to_thread(_down, msg)
    t_1 = threading.Thread(target=_down, daemon=True)
    t_1.start()
    await fut
    path = fut.result()
#    future = asyncio.run_coroutine_threadsafe(MSG_QUEUE.put(msg), LOOP)

    return path


# https://blog.azhangbaobao.cn/2019/05/30/python%E5%9C%A8%E5%A4%9A%E4%B8%AA%E7%BA%BF%E7%A8%8B%E4%B8%AD%E5%BC%80%E5%90%AF%E5%A4%9A%E4%B8%AA%E4%BA%8B%E4%BB%B6%E5%BE%AA%E7%8E%AF.html
def set_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def stop_loop(loop):
    loop.stop()

from functools import partial

async def _download_media(msg):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=set_loop, args=(loop,), daemon=True)
    t.start()
    print(msg.stringify())
    future = asyncio.run_coroutine_threadsafe(msg.download_media(DOWNLOAD_PATH), loop)
    try:
        pass
#        path = future.result(8)
    except:
        print("timeout")
        path = None
    future = asyncio.wrap_future(future, loop=LOOP)
    print("wait for result")
    await future

    path = future.result()
    print(path)

    loop.call_soon_threadsafe(partial(stop_loop, loop))
    if t.isAlive():
        logger.error("fail to stop")
        await asyncio.sleep(2)
        if t.isAlive():
            logger.error("fail to stop")
    return path


from ..telegram import download_media

async def qr_decode(msg):
#    path = await asyncio.to_thread(msg.download_media, DOWNLOAD_PATH)
    path = await download_media(UB, msg)
    print("download ok")
    print(path)
    if path:
        from ..utils.qr import decode
        try:
#            barcode = zxing_reader.decode(path)
            barcode = decode(path)
            return barcode.raw
        finally:
            os.remove(path)

    else:
        return "error: fail to download"




async def qr(event):
    text, key = get_text(event)
    res = []
    buttons = []
    if len(text.encode()) < 64:
        data = text
        text_bt = "see"
    else:
        data = MARK+"qr_de"
        link = await text2tg(text, get_sender_id(event))
        if link:
            mid = link.split("/")[-1]
            data += MARK+str(mid)
        text_bt = "decode"
    buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    from ..utils.qr import encode
    file = encode(text, out_type="JPEG")

#    file = await event.client.upload_file(file)

#    res.append(await builder.photo(file, include_media=True, buttons=buttons))
#    file = await pastebin(file, filename="qr.jpg")
    file = await ipfs_add(file, filename="qr.jpg")
    #  file = io.BytesIO(file)
    #  from ..utils.tools import tmp_save
    #  path = tmp_save(file, ".jpg")
    #  with open(path, "rb") as file:
    #      #  res.append(InlineQueryResultPhoto(file, reply_markup=InlineKeyboardMarkup(buttons)))
    #  os.remove(path)
    res.append(InlineQueryResultPhoto(file, title="qr code", description="msg has been saved", reply_markup=InlineKeyboardMarkup(buttons)))

    return res



from ..utils.text2img import text2img

async def text2pic(event):
    text, key = get_text(event)
    res = []
    buttons = []
    file = io.BytesIO()
    bg = None
    if text.startswith("0 "):
        fill = 0
        text = text.split(" ", 1)[1]
    elif text.startswith("1 "):
        fill = 1
        text = text.split(" ", 1)[1]
    elif " " in text and rgb_re.match(text.split(" ", 1)[0]):
        fill = text.split(" ", 1)[0]
        text = text.split(" ", 1)[1]

    else:
        fill = "#000000"

    if " " in text and rgb_re.match(text.split(" ")[1]):
        bg = text.split(" ", 1)[0]
        text = text.split(" ", 1)[1]

    width = 1
    if text.startswith(MARK+" "):
        text = text.split(" ", 1)[1]
        width = None

    if not text:
        return await get_help(builder, key)
#    img = text2img(text, fill=fill)
#    img = text2img(text, width=1, fill=fill, bg=bg)
#    img = await asyncio.to_thread(partial(text2img, text, width=1, fill=fill, bg=bg))

    img = await asyncio.to_thread(text2img, text, width=width, fill=fill, bg=bg)

    img.save(file, format="png")
    img=file.getvalue()
    file.close()
    file = img
#    file = await event.client.upload_file(file)
    if len(text.encode()) < 64:
        data = text
        text_bt = "see"
        buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
    buttons.append([InlineKeyboardButton('try same', switch_inline_query_current_chat=event.query)])
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    file = await ipfs_add(file, filename="text.png")
    res.append(InlineQueryResultPhoto(file, title="send pic", description="text has been saved", reply_markup=InlineKeyboardMarkup(buttons)))
    return res

async def ss(event):
    text, key = get_text(event)
    res = []
#    text = text[::-1]
    info = "\u200b".join(text)
    buttons = []
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    title = "insert space ok"
    des = info
    add(res, title, des, info, buttons)
    return res


async def rd(event):
    text, key = get_text(event)
    res = []
#    text = text[::-1]
    info = "\u200f".join(reversed(text))
    info = "\u200f"+info
    buttons = []
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    add(res, "recerse and reverse", info, info, buttons)
    return res





async def bs(event):
    text, key = get_text(event)
    res = []
    decode_ok = False
    try:
        info = decode_base64(text)

        if info:
            info = info.decode()
            if info:
                info = split_text(info)
                add(res, "base64 decode ok", info, info)
                decode_ok = True
        else:
            info = "fail to decode"
    except UnicodeDecodeError as e:
        pass
    except AttributeError as e:
        # 'NoneType' object has no attribute 'decode'
        pass
    info = encode_base64(text)
    if info:
        buttons = []
        data = MARK+"bs_de"
        link = await text2tg(text, get_sender_id(event))
        if link:
            mid = link.split("/")[-1]
            data += MARK+str(mid)
        link = None
        if len(info) > 4096:
            data = None
#                link = await text2link(text, max_len=0)
#            link = await text2link(info, max_len=0)
#            link = await asyncio.to_thread(ipfs_add, text.encode())
#            link = await asyncio.to_thread(pastebin, text)
            link = await pastebin(text)
            if link and "//" in link:
#                link = link.split(" ")[-1]
#                data = link.split("//")[1].split(".")[0]
                data = link
            else:
                logger.error(link)
                link = None
            if not data:
                info = ERROR_INFO
                data = "E: need to fix"
            else:
                info = "ipfs cid: {}".format(data)
                data = MARK + data
        if link:
            title = "using ipfs"
            des = "msg is too long, click to send ipfs cid"
            text_bt = "decode"
        else:
            title = "base64 encode"
            des = info
            text_bt = "see"
        buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
        if link:
            ipfs_bt = [InlineKeyboardButton("ipfs url", url=link)]
            buttons.append(ipfs_bt)
        buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
        add(res, title, des, info, buttons)

    return res


from ..utils.morse import encode as encode_morse
from ..utils.morse import decode as decode_morse

async def morse(event):
    text, key = get_text(event)
    res = []
    decode_ok = False
    info = decode_morse(text)
    if info:
        info = split_text(info)
        add(res, "decode ok", info, info)
        decode_ok = True
    else:
        info = "fail to decode"

    if not decode_ok:
        info = encode_morse(text)
        if info:
            buttons = []
            data = MARK+"ms_de"
            link = await text2tg(text, get_sender_id(event))
            if link:
                mid = link.split("/")[-1]
                data += MARK+str(mid)
            link = None
            if len(info) > 4096:
                data = None
#                link = await pastebin(text)
                link = await ipfs_add(text)
                if link and "//" in link:
                    data = link
                else:
                    logger.error(link)
                    link = None
                if not data:
                    info = ERROR_INFO
                    data = "E: need to fix"
                else:
                    info = "ipfs cid: {}".format(data)
#                    data = "$url"
                    data = MARK + data
            if link:
                title = "using ipfs"
                des = "msg is too long, click to send ipfs cid"
                text_bt = "decode"
            else:
                title = "morse encode"
                des = info
                text_bt = "see"
            buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
            if link:
                buttons.append([InlineKeyboardButton("ipfs", url=link)])
            buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
            add(res, title, des, info, buttons)

    return res

async def whisper(event):
    text, key = get_text(event)
    res = []
    buttons = []
    data = "None"
    link = None
    if not text.startswith("@") or " " not in text.strip():
        return await get_help(key)
    name = text.split(" ", 1)[0]
#    uid = await get_id(name)
    uid = await get_id(name)
    text = text.split(" ", 1)[1]
    if text.strip() == "":
        return await get_help(key)
    info = text
    if len(info) > 4096:
        info = ERROR_INFO
        data = "E: msg is too long"
    else:
        data = None
#        link = await pastebin(text)
        link = await text2tg(text, get_sender_id(event))
        if link and "//" in link:
#            data = link.split(" ")[-1]
            data = link
        else:
            logger.error(link)
            link = None
        if not data:
            info = ERROR_INFO
            data = "E: need to fix"
        else:
            info = link
            mid = link.split("/")[-1]
            data = MARK+f"tg {uid} {mid}"
    if link:
        title = "send whiper msg"
        info = f"A whisper message for {name} , only he can open it"
        des = info
        text_bt = "see"
        buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
    else:
        title = data
        des = info
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
#    res.append(await builder.article(title, text=info, description=des, buttons=buttons))
    add(res, title, des, info, buttons)

    return res


#from archivenow import archivenow
import savepagenow
from ..utils.tools import UA


async def ia(event):
    text, key = get_text(event)
    res = []
    if url_only_re.match(text):
        pass
    else:
        add(res, "error url", "your url is wrong", "error url")
        return res

    buttons = []
    link = None
    data = None
#    link = await text2link(text, max_len=0)
#    from .an import get_iv_from_bot
#    link = await get_iv_from_bot(text)


#    link = await asyncio.to_thread(archivenow.push, text, "ia")
    link, new = await asyncio.to_thread(savepagenow.capture_or_cache, url, UA)

    if link:
        link = link[0]
        s = url_only_re.match(link)
        if s:
            link = s.group("url")
    if link and "//" in link:
        data = link
    else:
        logger.error(link)
        link = None
    if not data:
        data = ERROR_INFO
        info = data
    else:
        info = link

    if link:
        if url_only_re.match(text):
            buttons.append([InlineKeyboardButton("url", url=text)])
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    if link:
        title = "send link"
        des = "using archive.org"
        text = link
    else:
        title = "error"
        des = ERROR_INFO
        text = info
    add(res, title, des, info, buttons)
    return res



async def tg(event):
    text, key = get_text(event)
    res = []
    buttons = []
    link = None
    data = None
    link = await save_to_telegraph(text)
    if link and "//" in link:
        data = link
    else:
        logger.error(link)
        link = None
    if not data:
        data = ERROR_INFO
        info = data
    else:
        info = link

    if link:
        if len(text.encode()) < 64:
            if url_only_re.match(text):
                buttons.append([InlineKeyboardButton("url", url=text)])
            else:
                text_bt = "see"
                data = text
                buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    if link:
        title = "send link"
        des = link
        info = link
    else:
        title = "error"
        des = ERROR_INFO
        info = info
    add(res, title, des, info, buttons)
    return res


async def tg2(event):
    text, key = get_text(event)
    res = []
    buttons = []
    link = None
    data = None
    if url_only_re.match(text):
        pass
    else:
        res.append(await builder.article('error url', description=text, text="for telegraph", buttons=buttons))
        return res
    from .an import get_iv_from_bot
    link = await get_iv_from_bot(text)
    if link and "//" in link:
        data = link
    else:
        logger.error(link)
        if link:
            info = link
        link = None

    if not data:
        data = ERROR_INFO
        if not info:
            info = data
    else:
        info = link

    if link:
        if len(text.encode()) < 64:
            buttons.append([Button.url('url', url=text)])
        else:
            pass
    buttons.append([Button.switch_inline('try', query=key+" ", same_peer=True)])
    if link:
        res.append(await builder.article('send tg link', description=link, text=link, buttons=buttons))
    else:
        res.append(await builder.article('error', description=ERROR_INFO, text=info, buttons=buttons))
    return res



async def pb(event):
    text, key = get_text(event)
    res = []

    buttons = []
    link = None
    data = None
#    link = await text2link(text, max_len=0)
#    link = await asyncio.to_thread(pastebin, text)
    link = await pastebin(text)
    if link and "//" in link:
        data = link
    else:
        logger.error(link)
        link = None
    if not data:
        data = ERROR_INFO
        info = data
    else:
        info = link

    if link:
        if len(text.encode()) < 64:
            text_bt = "see"
            data = text
        else:
            text_bt = "get"
            #  data = MARK+"url"
            data = MARK+"tg"
            link = await text2tg(text, get_sender_id(event))
            if link:
                mid = link.split("/")[-1]
                data += MARK+str(mid)
        buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    if link:
        title = "send link"
        des = link
        text = link
    else:
        title = "error"
        des = ERROR_INFO
    add(res, title, des, info, buttons)
    return res



async def ipfs(event):
    text, key = get_text(event)
    res = []

    buttons = []
    link = None
    data = None
#    link = await asyncio.to_thread(ipfs_add, text.encode())
    link = await ipfs_add(text)
    if link and "//" in link:
        data = link
    else:
        logger.error(link)
        link = None
    if not data:
        data = ERROR_INFO
        info = data
    else:
        data = MARK + data
        info = link

# [Button.switch_inline('try', query="sp ", same_peer=True)]
    if link:
        if len(text.encode()) < 64:
            data = text
            text_bt = "see"
        else:
            text_bt = "decode"
            #  data = MARK+"url"
            data = MARK+"tg"
            link = await text2tg(text, get_sender_id(event))
            if link:
                mid = link.split("/")[-1]
                data += MARK+str(mid)
        buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
    buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
    if link:
        title = "send link"
        des = link
        info = link
    else:
        title = "error"
        des = ERROR_INFO
        info = info
    add(res, title, des, info, buttons)
    return res



async def sp(event):
    text, key = get_text(event)
#    key = cmds_for_fun[sp.__name__]
#    text = get_text(event, "h")
    res = []

    decode_ok = False
    try:
        info = destr(text)
        if info is not None:
            info = split_text(info)
            add(res, "decode ok", info, info)
            decode_ok = True
        else:
            info = "fail to decode"
#    except ValueError:
    except UnicodeDecodeError as e:
        info = f"error: {e=}"

    if not decode_ok:
        info = enstr(text)
        buttons = []
        link = None
        if info is not None:
            if len(info.encode()) > 64:
                if len(info.encode()) > 4096:
                    data = None
#                    link = await text2link(text, max_len=0)
#                    link = await asyncio.to_thread(ipfs_add, text.encode(), "1.txt")
#                    link = await asyncio.to_thread(ipfs_add, text.encode())
                    link = await ipfs_add(text)
                    if link and "//" in link:
                        link = link.split(" ")[-1]
#                        data = link.split("//")[1].split(".")[0]
                        data = link
                    else:
                        logger.error(link)
                        link = None
                    if not data:
                        data = ERROR_INFO
                    else:
                        data = MARK + data
                elif len(text.encode()) < 64:
                    data = text
                else:
                    link = await text2tg(text, get_sender_id(event))
                    if link:
                        mid = link.split("/")[-1]
                        data = MARK+f"tg {mid}"
            else:
                data = info

            if link:
                text_bt = "get"
            else:
                text_bt = "see"
            buttons.append([InlineKeyboardButton(text_bt, callback_data=data)])
            s = url_only_re.match(text)
            if s:
                if s.group("url").startswith("https://t.me/"):
                    text_bt = "open tg url"
                else:
                    text_bt = "open url"

                buttons.append([InlineKeyboardButton(text_bt, url=s.group("url"))])

#            if link:
            if len(info.encode()) > 4096:
                ipfs_bt = [InlineKeyboardButton("ipfs url", url=link)]
                buttons.append(ipfs_bt)
            buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])

#            if not link and len(info.encode()) > 4096:
            if not link and len(text.encode()) >= 64:
                add(res, "error", "msg is too long and ipfs/tg is not ok, this may be a bug", info, buttons)
            else:
                if len(info.encode()) <= 4096:
                    add(res, "send hidden str", "use sapce", info, buttons)
                if link:
                    des = "using link"
                else:
                    des = "msd has been saved"
                mask = "█████"
                add(res, mask, des, mask, buttons)
#                if link:
                if len(info.encode()) > 4096:
                    buttons.remove(ipfs_bt)
                    add(res, "send link", "msg is too long", text, buttons)
    return res





async def default(event):
    builder = event.builder
    res = []
    if event.text == "id":
        res += [
                await builder.article('chat_id', text="chat_id: "+str(event.chat_id)),
                await builder.article('my_id', text="my_id: "+str(event.sender_id))
                ]
    elif event.text:
        pass
    else:
        pass
    return res



async def get(msg, client=NB):
    "get new msg, because of text: https://docs.pyrogram.org/api/types/CallbackQuery#pyrogram.types.CallbackQuery "
    print(msg)
    return (await client.get_messages(get_chat_id(msg), msg.message_id)).text




async def get_data(client, event):
    data = event.data
    if type(data) == bytes:
        data = data.decode()
    if data[0] == MARK:
        cmd = data.split(MARK)[1:]
    else:
        cmd = None
    msg = event.message
    if msg is None:
        text = None
    else:
        text = msg.text
    return cmd, data, msg, text




async def get_ex_text(client, event, cmd):

    text = None
    if len(cmd) > 1:
        link = cmd[1]
        if link.isnumeric():
            link = int(link)
        text = await get_text_from_msg(link, client)
        if not text:
            text = " ".join(cmd[1:])
    else:
        msg = await get_inline_msg(event)
        if msg:
            text = msg
    return text



async def get_inline_msg(event):
    "may fail if this is a private chat or group"

    if hasattr(event, "inline_message_id"):
    # https://github.com/LonamiWebs/Telethon/blob/08bb72ea6b49486efde98ba0100bbd32676646bf/telethon/_events/callbackquery.py#L79
        tmp = decode_base64(event.inline_message_id, altchars=b'-_')
        _, tmp, _ = struct.unpack("<iqq", tmp)
        msg_id, pid = struct.unpack('<ii', struct.pack('<q', tmp))
        pid = (await get_peer(pid, client=UB)).id
        #  print(msg_id, pid)
        #  msg = await get_msg(pid, msg_id, client)
        msg = await get_msg(pid, msg_id, UB)
        return msg


# @NB.on(events.CallbackQuery)
@NB.on_callback_query()
@tg_exceptions_handler
async def __(client, event):
    if not event.data:
        await event.answer("E: error, need fix")
        return
    cmd, data, msg, text = await get_data(client, event)
    info = None
    if cmd is None:
        if text and text[0] in chr_list:
            info = destr(text)
        elif data[0] in chr_list:
            info = destr(data)
        else:
            info = data
    elif cmd[0].startswith("baf"):
        if text and text[0] in chr_list:
            info = destr(text)
        else:
            ipfs_cid = data[1:]
            link = "https://{}.ipfs.infura-ipfs.io/".format(ipfs_cid)
            info = await http(link)
    elif data[:2] == MARK*2:
        info = data[1:]
    else:
        if not text:
            text = await get_ex_text(client, event, cmd)
        if isinstance(text, str):
            info = text
        elif text is not None:
            msg = text
            text = text.text

        if cmd[0] == "url":
#        url_data = await asyncio.to_thread(get_from_url, link)
            if not info:
                #  info = text
                info = await http(text)
        elif cmd[0] == "sp_sp":
            # sp sapce
            if not info:
                info = destr(text)
        elif cmd[0] == "bs_de":
            # base64 decode
            if not info:
                info = decode_base64(text)
                if info:
                    info = info.decode()
        elif cmd[0] == "ms_de":
            if not info:
                info = decode_morse(text)
        elif cmd[0] == "qr_de":
            if not info:
                info = await qr_decode(msg)
        #  elif cmd[0] == "tg":
        elif cmd[0].isnumeric():
            if len(cmd) == 2:
                uid = int(cmd[1])
                sender_id = get_sender_id(event)
                if sender_id != uid:
                    info = "you are not allowed to read this message"

        else:
            info = data

    if not info:
        info = "None"
    else:
        info = split_text(info)

    try:
        # await event.answer(info, cache_time=300, alert=True)
        cache_time = 300
        await event.answer(info, cache_time=cache_time, show_alert=True)
    # except MessageTooLongError:
    except Exception as e:
        from ..utils.telegram import put
        put(f"{e=}")



cmds = {
        "h": [sp, "h str: hide my msg"],
        "w": [whisper, "w @name str: whisper"],
        "b": [bs, "b str: base64"],
        "m": [morse, "m str: morse"],
        "i": [ss, "i str: insert sapce"],
        "r": [rd, "r str: reverse"],
        "q": [qr, "q str: qr"],
        "2": [text2pic, "2 str: pic"],
        "p": [pb, "p str: pastebin"],
        "ia": [ia, "ia url: archive.org"],
        "t": [tg, "t str/url: telegra.ph"],
        "tt": [tg2, "tt url: telegra.ph 2, slow"],
        "ipfs": [ipfs, "ipfs str: ipfs"]
        }

cmds_list = [x for x in cmds]

cmds_help = "\n".join([cmds[x][1] for x in cmds])
cmds_help_text = f"hide my message\nbot: @{BOT_NAME}\n----\n{cmds_help}\n\nstr: default(expand all available options)"
cmds_help = " // ".join([cmds[x][1] for x in cmds])


def get_offset(now):
    if now and now in cmds_list:
        now = cmds_list.index(now)
        if now+1 < len(cmds_list):
            return cmds_list[now+1]
        else:
            return None

    else:
#        return None
        return cmds_list[0]


async def get_help(offset=None):
    res = []
    if offset:
        key = offset
        helps = cmds[key][1].split(": ", 1)
        buttons = []
        buttons.append([InlineKeyboardButton('try', switch_inline_query_current_chat=key+" ")])
        res.append(InlineQueryResultArticle(helps[1], description=helps[0], input_message_content=InputTextMessageContent(cmds[key][1]), reply_markup=InlineKeyboardMarkup(buttons)))
    else:
        for i in cmds:
            res += await get_help(i)
    return res


MARK = " "

mp = logger.warning

#@NB.on(events.InlineQuery(blacklist_users=True))
#@NB.on(events.InlineQuery(users=[MY_ID, UB2_ID]))
# @NB.on(events.InlineQuery)
@NB.on_inline_query()
@tg_exceptions_handler
async def __(client, event):
    res = []
    # res.append(InlineQueryResultArticle('debug', description="dump mag: {}".format(event.offset), input_message_content=InputTextMessageContent(str(event))))
    next_offset = None
    link = "https://github.com/liqsliu/toxbot"
    next_offset = None
    text, key = get_text(event)
    if key and key in cmds:
        if text is not None:
            res = await cmds[key][0](event)
            if not event.query.startswith(f"{key} "):
                next_offset = get_offset(key)
        else:
            res = await get_help(key)
        # if event.offset:
    else:
        pass

    if not res:
        if text:
            while not res:
                if next_offset is None:
                    break
                res = await cmds[next_offset][0](event)
                next_offset = get_offset(next_offset)
            if not res:
                res.append(InlineQueryResultArticle('error', description=ERROR_INFO, input_message_content=InputTextMessageContent(ERROR_INFO)))
        else:
            buttons = []
            for i in cmds:
                buttons.append([InlineKeyboardButton('try{}'.format(cmds[i][1].split(":", 1)[1]), switch_inline_query_current_chat="{} ".format(i))])
            buttons.append([InlineKeyboardButton('try all', switch_inline_query_current_chat="")])
            res.append(InlineQueryResultArticle('help: click to send full info', description=cmds_help, input_message_content=InputTextMessageContent(cmds_help_text), reply_markup=InlineKeyboardMarkup(buttons)))
            res += await get_help()
            res.append(InlineQueryResultArticle('my id', description="send my id to the chat", input_message_content=InputTextMessageContent(get_sender_id(event))))
            res.append(InlineQueryResultArticle('debug', description="dump mag: {}".format(event.offset), input_message_content=InputTextMessageContent(str(event))))
            res.append(InlineQueryResultArticle('src', description="source link", input_message_content=InputTextMessageContent(link)))

    if text and text.rstrip(" ") not in cmds:
        private = True
        cache_time = 600
    else:
        private = False
        cache_time = 6000
    for i in res:
#        print(dir(i))
        # if hasattr(i.send_message, "message"):
        if hasattr(i.input_message_content, "message_text"):
            if i.input_message_content.message_text == ERROR_INFO:
                logger.error(f"error query: {text}")
                logger.error(f"error in inline result: {i}")
                from ..telegram import put
                put(f"error query: {text}")
                cache_time = 15
                break
    try:
        # await event.answer(res, cache_time=cache_time, private=private, next_offset=next_offset)
        return await event.answer(results=res, cache_time=cache_time, is_personal=private, next_offset=next_offset)
    except Exception as e:
#        logger.error(e)
#        from ..telegram import put
#        put(str(e))
        urls = ""
        for i in res:
            if hasattr(i, "url"):
                # urls += f"error url: {i.url=}{i.title=}{i.send_message.message=}"
                urls += f"error url: {i.url=}{i.title=}{i.input_message_content.message_text=}"
        if urls:
            logger.error(urls)
            put(urls)
        raise


#        await event.answer(res, cache_time=60, switch_pm="private chat", switch_pm_param="test")



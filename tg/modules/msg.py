#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

from pyrogram.errors.exceptions import bad_request_400

from ..telegram import get_msg_from_url, get_real_id, get_client2, get_id, get_msg_id, put
from ..utils.tools import url_re

from ..utils import db


logger = logging.getLogger(__name__)








async def print_res(res=None):
    if res is not None:
        info = f"{offset} + {len(res)} / {limit}"
        info += "\n"
        for i in res:
            #  info += f"{i['chat']} {i['id']} {i['text']}"
            info += "\n"
            #  info += f"https://t.me/c/{get_real_id(i['chat'])}/{i['id']}\n{i['text']}\n"
            info += f"https://t.me/c/{get_real_id(i['chat'])}/{i['id']}\n{i['sender']} {i['text']}\n"
        info = info.strip()
    return info








async def _(client, event):
    cmd = await get_cmd(client, event)
    info = ""
    limit = 5
    offset = 0
    if len(cmd) == 1:
        info = "msg link"
        info += "\npin [num] [id/url]"
        info += "\nse like %_"
        info += "\nse glob *?"
        info += "\nse only"
        info += "\nsf first_name"
        info += "\nsu username"
        info += "\nsg cid"
        info += "\npin"

    elif url_re.search(cmd[1]):
        url = url_re.search(cmd[1])
        url = url.group()
        chat_id = get_chat_id(event)
        #  client = UB
        msg = await get_msg_from_url(url, client)
        app = client
        #  info = str(msg)
        if msg and msg.empty or not msg:
            app = get_client2(client)
            msg = await get_msg_from_url(url, app)
            #  await client.send_message(MY_ID, "use client2")
            info += "using client2"
        if msg:
            if msg.empty:
                info += "\nEmpty messages cannot be copied."
            else:
                #  info += str(msg)
                #  print(msg)
                try:
                    await msg.copy(get_chat_id(event))
                except Exception as e:
                    put(e)

                try:
                    await msg.forward(get_chat_id(event))
                except bad_request_400.ChatForwardsRestricted as e:
                    put(e)

        else:
            info += "no msg"

    elif cmd[1] == "sf":
        if len(cmd) > 2:
            res = db.search(" ".join(cmd[2:]), key="first_name", table="user")
            if res is not None:
                info = ""
                for i in res:
                    info += f"{i['first_name']} tg://openmessage?user_id={i['id']}\n"
                    info += "\n"
                info = info.strip()
    elif cmd[1] == "su":
        if len(cmd) > 2:
            res = db.search(" ".join(cmd[2:]), key="username", table="user")
            info = await print_res(res)
            if res is not None:
                info = ""
                for i in res:
                    info += f"@{i['username']} {i['id']}\n"
                    info += "\n"
                info = info.strip()

    elif cmd[1] == "sg":
        if len(cmd) > 2:
            if len(cmd) > 3:
                if cmd[2].isnumeric():
                    pass
                    limit = int(cmd[2])
                    query = " ".join(cmd[3:])
                elif cmd[2][0] == "-" and cmd[2][1:].isnumeric():
                    limit = 10
                    offset = (int(cmd[2][1:]) - 1) * limit
                    query = " ".join(cmd[3:])
                else:
                    query = " ".join(cmd[2:])
            res = db.search(int(query), key="chat", table="message", limit=limit, offset=offset)
            info = await print_res(res)
    elif cmd[1] == "si":
        if len(cmd) > 2:
            if len(cmd) > 3:
                if cmd[2].isnumeric():
                    pass
                    limit = int(cmd[2])
                    query = " ".join(cmd[3:])
                elif cmd[2][0] == "-" and cmd[2][1:].isnumeric():
                    limit = 10
                    offset = (int(cmd[2][1:]) - 1) * limit
                    query = " ".join(cmd[3:])
                else:
                    query = " ".join(cmd[2:])
            res = db.search(int(query), key="id", table="message", limit=limit, offset=offset)
            info = await print_res(res)
    elif cmd[1] == "se":
        if len(cmd) > 2:
            if cmd[2].isnumeric():
                pass
                limit = int(cmd[2])
                query = " ".join(cmd[3:])
            elif cmd[2][0] == "-" and cmd[2][1:].isnumeric():
                limit = 10
                offset = (int(cmd[2][1:]) - 1) * limit
                query = " ".join(cmd[3:])
            else:
                query = " ".join(cmd[2:])
            res = db.search(query, limit=limit, offset=offset)
            info = await print_res(res)
    elif cmd[1] == "pin":
        #  if len(cmd) == 2:
        limit = 15
        chat_id = None
        if len(cmd) > 2:
            ex = cmd[2]
            if ex.isnumeric():
                if len(ex) < 5:
                    if len(cmd) > 2:
                        limit = int(cmd[2])
                        if limit == 0:
                            limit = None
                        chat_id = get_chat_id(event)
                    elif len(cmd) > 3:
                        url = cmd[3]
                else:
                    chat_id = int(cmd[2])
            else:
                url = cmd[2]
        else:
            chat_id = get_chat_id(event)
        if chat_id is None:
            if "/" in url and url[-1].isnumeric():
                msg = await get_msg_from_url(url, client)
                chat_id = get_chat_id(msg)
            else:
                chat_id = await get_id(url)

        client = UB
        #  async for msg in client.search_messages(chat_id, filter="pinned", limit=limit):
        async for msg in client.search_messages(chat_id, filter=enums.MessagesFilter.PINNED, limit=limit):
            info += f"\n{msg.link}"
        if not info:
            info = "no pinned message"
        else:
            if len(info.splitlines()) > limit:
                info = f"pinned messages: limit: {limit}\n{info}"
            else:
                info = f"pinned messages:\n{info}"
    elif cmd[1] == "delme":
        pass
    else:
        info = "msg link?"
    if info:
        pass
    else:
        info = "None"
    await cmd_answer(info, client,  event)


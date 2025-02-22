from . import *

from pyrogram.types import User

from pyrogram.file_id import FileId

from ..telegram import get_another_client
from ..telegram import MAX_MSG_LEN
from ..telegram import mdraw, is_reply, get_real_id, get_msg_from_url


from .dc import get_dc

logger = logging.getLogger(__name__)

async def _(client, event):
    "id"
    info = ""
    cmd = await get_cmd(client, event)
    msg = None
    if is_reply(event):
        msg = event.reply_to_message
    elif cmd[-1].startswith("https://t.me/"):
        tmp = cmd[-1]
        url = None
        if len(tmp.split("?", 1)[0].split("/")) == 5:
            url = tmp
        elif tmp.startswith("https://t.me/c/"):
            if len(tmp.split("?", 1)[0].split("/")) == 6:
                url = tmp
        if url:
            msg = await get_msg_from_url(url, client)
            if msg and msg.empty or not msg:
                app = get_client2(client)
                msg = await get_msg_from_url(url, app)
            cmd.pop(-1)
    if msg:
        sender = get_sender(msg)
        chat_id = get_chat_id(msg)
    else:
        sender = get_sender(event)
        chat_id = get_chat_id(event)
    if len(cmd) == 1:
        if msg:
            if sender is not None:
                info = f"sender id: {sender.id}"
        else:
            info = "tg://openmessage?user_id="
            info += "\ntg://openmessage?chat_id="
            event = await cmd_answer(info, client, event)
            info = "id $name/$id"
            info += "\nid u"
            info += "\nid c"
            info += "\nid m"
            info += "\nid dc"
            info += "\nid f"
    elif cmd[1] == "u":
        info = sender.id
    elif cmd[1] == "dc":
        if msg:
            if sender.dc_id:
                dc_id = sender.dc_id
                info += f"user: dc{dc_id}"
            else:
                info += f"user: no avatar"
                dc = await get_dc(sender, client, get_chat_id(msg))
                if dc:
                    info += "\nbut: dc" + str(dc)
            if msg.media:
                i = getattr(msg, msg.media).file_id
                file = FileId.decode(i)
                dc_id = file.dc_id
                info += f"\n{msg.media}: dc{dc_id}"
        else:
            info += "need fix"
    elif cmd[1] == "c":
        info = chat_id
    elif cmd[1] == "m":
        if msg:
            info = msg.id
    elif cmd[1] == "f":
        if msg:
            info = str(msg)
        else:
            peer = await get_peer(cmd[2], client=client)
            info = str(peer)
    else:
        peer = await get_peer(cmd[1], client=client)
        if not peer:
            info = "None"
        else:
            if type(peer) == User:
                if peer.username:
                    name = "@" + peer.username
                else:
                    name = peer.first_name
                if name:
                    info = name
                    info = info + " tg://openmessage?user_id=" + str(get_real_id(peer))
                else:
                    info = "deleted user: tg://openmessage?user_id=" + str(get_real_id(peer))
            else:
                info = "tg://openmessage?chat_id=" + str(get_real_id(peer))
            info += "\n" + str(type(peer)) + ": `" + str(peer.id) + "`"
        #  await client.send_message(chat_id, info)
    return await cmd_answer(info, client, event, parse_mode=enums.ParseMode.MARKDOWN)


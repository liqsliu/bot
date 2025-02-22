#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

from ..telegram import get_msg_from_url
from ..telegram import media2link, is_reply, MEDIAS

logger = logging.getLogger(__name__)


from ..utils.tools import http, pastebin, ipfs_add, url_only_re, catbox, pb_0x0

async def _(client, event):
    cmd = await get_cmd(client, event)
    msg = None
    use_pb = False
    info = None
    just = False
    ex = None
    if len(cmd) == 1:
        if is_reply(event):
            r = event.reply_to_message
            msg = r
        else:
            info = "reply to save, or give me msg link"
            await cmd_answer(info, client, event)
            return
    else:
        if is_reply(event):
            r = event.reply_to_message
            msg = r
            if len(cmd) > 1:
                if cmd[1] == "pb":
                    use_pb = True
                elif cmd[1] == "noup":
                    ex = "just"
                elif cmd[1] == "x":
                    ex = "ddd"
                elif cmd[1] == "catbox":
                    ex = "ddddd"
                elif cmd[1] == "catbox2":
                    ex = "dddddd"
        else:
            if cmd[1].startswith("https://t.me/"):
                msg = await get_msg_from_url(cmd[1], client)
                if len(cmd) > 2:
                    if cmd[2] == "pb":
                        use_pb = True
                    elif cmd[2] == "noup":
                        ex = "just"
                    elif cmd[2] == "x":
                        ex = "ddd"
                    elif cmd[2] == "catbox":
                        ex = "ddddd"
                    elif cmd[2] == "catbox2":
                        ex = "dddddd"
            elif url_only_re.match(cmd[1]):
                info = await catbox(cmd[1])

    if msg:
        if msg.media:
            # if event.is_private:
                # if msg.client == client:
                    # await msg.client.send_message(chat_id, file=msg.media)
                # else:
                    # info = "client error, need fix"
            #  if msg.media in ["audio","document","photo","sticker","video","animation","voice","video_note"]:
            if msg.media in MEDIAS:
                file = getattr(msg, msg.media.value)
                size = file.file_size
            else:
                file = None
            if file:
                max_file_size=512000000
                #  if 1:
                #  if size < 200000000:
                if size < max_file_size:
                    if use_pb:
                        info = await media2link(client, msg, use_pb, max_file_size=max_file_size)
                    else:
                        if ex:
                            info = await media2link(client, msg, ex=ex, max_file_size=max_file_size)
                        else:
                            info = await media2link(client, msg, max_file_size=max_file_size)
                        if info:
                            info = "name: " + info[1] + "\nlink: " + info[0]
                else:
                    info = "file is too big: {}".format(size)
            else:
                info = "no file"
        elif msg.text:
            text = msg.text
            if use_pb:
                link = await pastebin(text)
            elif ex == "ddd":
                link = await pb_0x0(text)
            elif ex == "ddddd":
                link = await catbox(text)
            else:
                link = await ipfs_add(text)
            if link:
                info = f"saved text to: {link}"
            else:
                info = f"error {link}"

        else:
            info = "nothing"
    elif info is not None:
        pass
    else:
        info = "no msg"
    await cmd_answer(info, client, event)

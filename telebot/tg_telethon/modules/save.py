#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

from ..utils.telegram import get_msg_from_url
from ..utils.telegram import media2link

logger = logging.getLogger(__name__)
mp = logger.info



from ..utils.tools import http, pastebin, ipfs_add

async def _(event):
    logger.info("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  mp("{}: ping".format(event.sender_id, event.raw_text))
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    #    await run_task_for_event(event)
    #    await event.reply("pong")
    #  await UB.send_message(MY_ID, "ok")
    client = event.client
    cmd = await get_cmd(event)
    msg = None
    use_pb = False
    if len(cmd) == 1:
        if event.is_reply:
            replied = await event.get_reply_message()
            msg = replied
        else:
            info = "reply to save, or give me msg link"
            await cmd_answer(info, event)
            return
    else:
        if event.is_reply:
            replied = await event.get_reply_message()
            msg = replied
            if len(cmd) > 1:
                if cmd[1] == "pb":
                    use_pb = True
        else:
            msg = await get_msg_from_url(cmd[1], event)
            if len(cmd) > 2:
                if cmd[2] == "pb":
                    use_pb = True

    if not msg:
        await cmd_answer("no msg", event)
        return

    info = None
    if msg.media:
        if event.is_private:
            if msg.client == client:
                await msg.client.send_message(event.chat_id, file=msg.media)
            else:
                info = "client error, need fix"
        if msg.file:
            if msg.file.size < 64000000:
                if use_pb:
                    info = await media2link(msg, use_pb)
                else:
                    info = await media2link(msg)
                    if info:
                        info = "name: " + info[1] + "\nlink: " + info[0]
            else:
                info = "file is too big: {}".format(msg.file.size)
        else:
            info = "no file"
    elif msg.raw_text:
        text = msg.raw_text
        if use_pb:
            link = await pastebin(text)
        else:
            link = await ipfs_add(text)
        if link:
            info = f"saved text to: {link}"
        else:
            info = "error"

    else:
#        await msg.client.send_message(event.chat_id, "nothing")
        info = "nothing"
    await cmd_answer(info, event)


cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

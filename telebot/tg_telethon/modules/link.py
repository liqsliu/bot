#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import get_msg_from_url

from ..utils.telegram import get_fwd_info

from telethon import utils

async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  mp("{}: ping".format(event.sender_id, event.raw_text))
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    #    await run_task_for_event(event)
    #    await event.reply("pong")
    #  await UB.send_message(MY_ID, "ok")
    client = event.client
    sender = event.sender
    info = ""
    cmd = await get_cmd(event)

    if event.is_reply:
        msg = await event.get_reply_message()
        url = None
    elif len(cmd) == 1:
        info = "link url"
        await cmd_answer(info, event)
        return
    else:
        url = cmd[1]
        #          chat=utils.resolve_id(cid)[1]
        if len(cmd) == 3:
            if cmd[2] == "0":
                client = UB
            elif cmd[2] == "1":
                client = NB
            else:
                client = UB2
            msg = await get_msg_from_url(cmd[1], client=client)
            client = event.client
        else:
            msg = await get_msg_from_url(cmd[1], event)
    if msg:
        #          info=mdraw(msg.stringify(),"code")
        #    info=mdraw(msg.stringify(),"`")
        #    info="```\n"+info+"\n```"
        info = msg.stringify()
        await cmd_answer(info, event)

        #    info="\n\n"
        info = ""

        info += "tg://openmessage?chat_id=" + str(
            utils.resolve_id(msg.chat_id)[0])
        info += "\ncid: `" + str(msg.chat_id) + "`"
        if msg.sender_id and msg.chat_id != msg.sender_id:
            if msg.sender_id > 0:
                info += "\n\ntg://openmessage?user_id=" + str(msg.sender_id)
                info += "\nuid: `" + str(msg.sender_id) + "`"
            else:
                info += "\n\ntg://openmessage?chat_id=" + str(utils.resolve_id(msg.sender_id)[0])
                info += "\ncid: `" + str(msg.sender_id) + "`"
        if url is not None and "?comment=" in url:
            chat = msg.chat
            if chat.username:
                info += "\nmsg link: https://t.me/" + chat.username + "/" + str( msg.id)
            else:
                info += "\n\nmsg link: https://t.me/c/" + str(utils.resolve_id(utils.get_peer_id(chat))[0]) + "/" + str( msg.id)


#    await client.send_message(event.chat_id, info)
        await cmd_answer(info, event, parse_mode="md")
        if msg.fwd_from:
            info = await get_fwd_info(msg)
            if info:
                await cmd_answer(info, event, parse_mode="md")
    else:
        #          info=mdraw(msg.stringify(),"code")
        info = "no msg"
        #        await client.send_message(me.id, "msg:" + msg)
        #        await myprint("msg: " + msg)
        await cmd_answer(info, event)


cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

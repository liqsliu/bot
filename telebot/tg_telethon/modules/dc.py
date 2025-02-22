#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info


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

    sender = event.sender
    info = ""
    cmd = await get_cmd(event)
    if (len(cmd) > 1 and cmd[1] == "f") or not sender:
        sender = await event.get_sender()
    if not sender:
        if sender_id:
            sender = await get_peer(sender_id, event=event)

    if not sender or not sender.photo:
        if sender_id:
            client2 = get_another_client(client)
            sender = await client2.get_entity(sender_id)
            info += "(via bot2): "

    if sender:
        if sender.photo:
            info += "dc" + str(sender.photo.dc_id)
        else:
            info += "no photo"
    else:
        info += "error"
    if event.is_private:

        info += """
```
DC1
MIA, Miami FL, USA
149.154.175.53
2001:b28:f23d:f001::a
DC2
AMS, Amsterdam, NL
149.154.167.51
2001:67c:4e8:f002::a
DC3*
MIA, Miami FL, USA
149.154.175.100
2001:b28:f23d:f003::a
DC4
AMS, Amsterdam, NL
149.154.167.91
2001:67c:4e8:f004::a
DC5
SIN, Singapore, SG
91.108.56.130
2001:b28:f23f:f005::a
```
"""
        info += "\nhttps://core.telegram.org/getProxyConfig"
        info += "\nhttps://docs.pyrogram.org/faq/what-are-the-ip-addresses-of-telegram-data-centers"

    await event.reply(info)



need = need & ~CMD.is_admin

cmd = __name__.split(".")[-1]

CMD.add(_, cmd=cmd, need=need, forbid=forbid)


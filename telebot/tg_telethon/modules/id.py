#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

from ..utils.telegram import mdraw
from ..utils.telegram import get_another_client
from ..utils.telegram import MAX_MSG_LEN

from telethon import utils

logger = logging.getLogger(__name__)
mp = logger.info

async def _(event):
    "id"
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
    if len(cmd) == 1:
        if event.is_reply:
            r = await event.get_reply_message()
            if r.sender is not None:
                u = r.sender
            else:
                u = await r.get_sender()
            uid = utils.get_peer_id(u)
            info = f"your id: {uid}"
        else:
            info = "tg://openmessage?user_id="
            await cmd_answer(info, event)
            info = "tg://openmessage?chat_id="
        await cmd_answer(info, event)
    elif cmd[1] == "u":
        r = await event.get_reply_message()
        if r.sender:
            uid = utils.get_peer_id(r.sender)
        else:
            u = await r.get_sender()
            uid = utils.get_peer_id(u)
        await cmd_answer(uid, event)
    elif cmd[1] == "m":
        r = await event.get_reply_message()
        await cmd_answer(r.id, event)
    else:
        #          await client.send_message(me.id, str(type(peer)))
        #          if type(peer) == PeerUser:
        #        peer=await client.get_entity(id)
        peer = await get_peer(cmd[1], event=event)
        if not peer:
            await cmd_answer("null", event)
            return
#    info = info+"\n"+str(type(peer))+ ": `" +str(utils.get_peer_id(peer))+"`"
#    info = info+"\n"+str(type(peer))+ ": `" +str(utils.get_peer_id(peer))+"`"
        await cmd_answer(peer.stringify(), event)
        if type(peer) == User:
            if peer.username:
                name = "@" + peer.username
            else:
                name = peer.first_name
#          await client.send_message(me.id, "["+str(peer.id)+"](tg://user?id="+str(peer.id)+")", parse_mode="md")
            if name:
                #        info="["+name+"](tg://openmessage?user_id="+str(peer.id)+")"
                info = name
                info = info + " tg://openmessage?user_id=" + str(peer.id)
            else:
                info = "deleted user: tg://openmessage?user_id=" + str(peer.id)
        else:
            #          "\ntg://openmessage?chat_id="+str(cid))+"\ntg://openmessage?user_id="+str(msg.sender_id))+"\n\nby draft\ncid: `"+str(cid)+"`\nuid: `"+str(msg.sender_id)+"`"
            info = "tg://openmessage?chat_id=" + str(peer.id)


#        info = "```\n"+ mdraw(peer.stringify(),"code") +"\n```\n\n"+ info+"\n"+str(type(peer))+ ": `" +str(utils.get_peer_id(peer))+"`"
        info += "\n" + str(type(peer)) + ": `" + str(
            utils.get_peer_id(peer)) + "`"
        await client.send_message(event.chat_id, info)



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

from telethon import events
from telethon.events import StopPropagation

from telethon.tl.types import PeerChannel

#from .modules import *
from .bot import *
#from .cmd import CMD
#from .bot import MY_ID
#from .bot import logging
#import logging

logger = logging.getLogger(__name__)
mp = logger.warning

#func= lambda x:x.chat_id=MY_ID and not await get_cmd(event)

from .utils.config import cid_wtfipfs, cid_ipfsrss, cid_tw, TG_BOT_ID_FOR_MT

from .utils.telegram import tg_exceptions_handler, forward_msg, MSG_QUEUE, parse_msg_for_mt, parse_bridge_name, send_msg_of_queue, send_cmd_to_bash, ban_chat, get_msg, set_event, get_id

from .utils.mt import mt_send, mt_read

from telethon import utils



need = CMD.is_UB2+CMD.is_all
forbid = CMD.is_out
CMD.add(set_event, need=need, forbid=forbid)




from .utils import db
from .utils.tools import num2byte, byte2num
from .cmd import is_channel
from .cmd import is_group
from .cmd import is_bot

async def save(e, table, in_group=None):
    if e is None:
        return
    data = {}
    cs = db.columns(table)
    if table == "messages":
        d = e.message.to_dict()
        d["chat_id"] = await get_id(e.chat_id)
        d["sender_id"] = await get_id(e.sender_id)
        if e.raw_text:
            d["text"] = e.raw_text
        else:
            return
            d["text"] = None
    elif table == "groups":
        d = e.to_dict()
        d["id"] = await get_id(e)

    else:
        d = e.to_dict()
    if "id" not in d:
        d["id"] = await get_id(e)
    if d["id"] is None:
        logger.error(f"need fix: id not found: {d}")
        return

    if table == "users":
        # if d["first_name"] is None:
        if d.get("first_name", None) is None:
            return
    elif table == "messages":
        if d.get("chat_id", None) is None:
            return
    elif table == "groups":
        if d.get("title", None) is None:
            return

    if "date" in cs:
        d["date"] = int(e.date.timestamp())

    for i in cs:
        if i in d:
            # if d.get(i, None) is not None:
            data.update({i: d.get(i)})
    if table == "users" and in_group is not None:
        id2 = db.get(in_group, "groups")["id2"]
        u = db.get(d["id"], "users")
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
    elif table == "groups":
        g = db.get(data["id"], "groups")
        if g is not None:
            g.pop("id2")
            if data == g:
                logger.warning(f"skip {data['id']}")
                return
    # print(data)
    db.save(data, table)
    return data



#@NB.on(events.NewMessage)
# @UB.on(events.NewMessage)
async def _(event):
    "log, just for test"
    # users = ["id", "first_name", "last_name", "username", ]
    if event.is_private:
        await save(event.chat, "users")
        await save(event, "messages")
    elif is_channel(event):
        pass
    elif is_group(event):
        g = await save(event.chat, "groups")
        u = await save(event.sender, "users", await get_id(event.chat_id))
        m = await save(event, "messages")
        if g and u and m:
            info = f"""{g["title"]} {u["first_name"]}: {m["text"]}"""
            print(info)
    else:
        logger.error(f"unknown event: {type(event)}")
            



need = CMD.is_new
need += CMD.is_UB
# need += CMD.is_admin
forbid = CMD.is_bot
forbid += CMD.is_channel
# CMD.add(_, need=need, forbid=forbid)






async def unpin(event):
    if event.sender_id == cid_tw:
        await event.unpin()
        raise StopPropagation
    else:
        mp("I: get a channel msg in wtf from: " + str(event.sender_id))
#        await ban_chat(event.chat_id, event.sender_id, event=event)
#        await event.delete()
#        raise StopPropagation


need = CMD.is_UB+CMD.is_new
need += CMD.is_my_group
need += CMD.is_anon_msg
forbid = CMD.is_out
CMD.add(unpin, need=need, forbid=forbid)




from .utils.config import MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg

# backup some channels
#@UB.on(events.NewMessage(incoming=True, func=lambda x: not x.grouped_id and x.is_channel and x.chat.broadcast))
#@UB.on(events.Album(func=lambda x: x.is_channel and x.chat.broadcast))
async def forward(event):
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    await forward_msg(event)
    chat_id = event.chat_id
    if chat_id in MT_GATEWAY_LIST_for_tg:
        if MT_GATEWAY_LIST_for_tg[chat_id] == "gateway5":  # need not to send in order
            msg = await parse_msg_for_mt(event)
            if msg:
                pass
                await mt_send(msg[0], msg[1], msg[2], msg[3])
    raise StopPropagation


need = CMD.is_UB+CMD.is_all
need += CMD.is_channel
forbid = CMD.is_edit
CMD.add(forward, need=need, forbid=forbid)






async def chatbot(event):
    "chat bot"
    client = event.client
    sender_id = event.sender_id
    if sender_id == MY_ID:
        if event.is_reply:
            replied = await event.get_reply_message()
            if replied:
                lines = replied.raw_text.split("\n")
                if lines[0] == "new msg":
                    target_id = int(lines[-1].split(" ")[1])
                    target = await client.get_entity(target_id)
                    if target:
                        if target.status:
                            msg_t = await event.forward_to(target)
                            await client.send_message(MY_ID, "I: ok")
                            raise StopPropagation
                        else:
                            await client.send_message(
                                MY_ID,
                                "E: can not send, stopped or deleted chat")
                    else:
                        await client.send_message(MY_ID, "E: wtf: no entity")
                    return

    else:
        chat_id = event.chat_id
        msg_info = "new msg\n"
        from_info = "\nmsg_id " + str(event.id) + "\nfrom " + str(
            sender_id) + " tg://openmessage?user_id=" + str(sender_id)
        if event.is_private:
            chat = await client.get_entity(MY_ID)
            if chat.status:
                msg = await event.forward_to(MY_ID)
                await msg.reply(msg_info + from_info)
                await client.send_message(chat_id, "msg has been sent")
            else:
                if event.raw_text and event.raw_text[0] == "/":
                    pass
                else:
                    if MY_NAME:
                        await client.send_message(
                            chat_id, "error: forwarding failed, @" + MY_NAME +
                            " has stopped forwarding, please chat directly")
                    else:
                        await client.send_message(
                            chat_id,
                            "error: forwarding failed, please chat directly")
                        raise StopPropagation
        else:
            if event.mentioned:
                # album no
                await event.forward_to(MY_ID)
                chat_info = "\nchat_id: " + str(chat_id) + " tg://openmessage?chat_id=" + str(await get_id(event.chat_id))
#                        utils.resolve_id(msg.chat_id)[0])
                await msg.reply(msg_info + chat_info + from_info)

need = CMD.is_NB+CMD.is_new
#need = CMD.is_NB+CMD.is_all
#need += CMD.is_private
forbid = 0
forbid = CMD.is_out
CMD.add(chatbot, need=need, forbid=forbid)



asyncio.create_task(send_msg_of_queue(), name="tg_send")

# for msg order
locks = {}
# read msg from matterbridge api
asyncio.create_task(mt_read(MSG_QUEUE), name="mt_read")

async def send2mt(event):
    "get msg for matterbridge api"
    if event.raw_text == "test":
        print("fun get texr")
    chat_id = event.chat_id
    if chat_id in MT_GATEWAY_LIST_for_tg:
#        logger.warning(f"send 2 mt: {event.raw_text}")
        logger.warning("start to mt")
#        if event.fwd_from:
        if event.forward:
            if event.sender_id == cid_tw:
                print("I: ignore a msg from tw")
                raise StopPropagation
#        if event.sender_id == 1494863126:
            # wtfipfsbot
#            pass
        if event.sender_id == 420415423:
            # t2bot
            if event.raw_text.startswith("bot: "):
                await event.delete()
                raise StopPropagation
        if MT_GATEWAY_LIST_for_tg[chat_id] == "gateway5":  # need not to send in order
            if type(event) == events.messageedited.MessageEdited.Event:
                raise StopPropagation
            msg = await parse_msg_for_mt(event)
            if msg:
                await mt_send(msg[0], msg[1], msg[2], msg[3])
        else:
            global locks
            if chat_id in locks:
                pass
            else:
                locks.update({chat_id: asyncio.Lock()})
            lock = locks[chat_id]
            async with lock:
                msg = await parse_msg_for_mt(event)  # return [text, username, gateway, qt]
                if msg:
                    pass
                    if event.sender_id == BOT_ID:
                        pass
                    elif event.sender_id == TG_BOT_ID_FOR_MT:
                        pass
                    elif await parse_bridge_name(msg[1].rstrip(": ")):
                        msg[1] = await parse_bridge_name(msg[1].rstrip(": "))
                    else:
                        await mt_send(msg[0], msg[1], msg[2], msg[3])

                    if msg[2] == "gateway11":
                        msg[2] = "gateway1"
                    #for cmd answer
                    if msg[1].endswith(": "):
                        msg[1] = msg[1].strip(": ")
                    if msg[1] != "C bot":
                        if await CMD.check_cmd(event):
                            logger.warning("cmd ok")
                            pass
                        else:
                            logger.warning("use bash")
                            asyncio.create_task(send_cmd_to_bash(msg))
                            raise StopPropagation
#        if event.out:
#            raise StopPropagation



need = CMD.is_UB+CMD.is_all
#need += CMD.is_group
forbid = CMD.is_admin
CMD.add(send2mt, need=need, forbid=forbid)

need = CMD.is_UB2+CMD.is_all
need += CMD.is_admin
forbid = 0
CMD.add(send2mt, need=need, forbid=forbid)



get_cmd = CMD.get_cmd
from .utils.telegram import get_fwd_info, cmd_answer, mdraw, myprint, myprintmd, get_peer, MAX_MSG_LEN


@NB.on(events.NewMessage(from_users=MY_ID, func=lambda e: not e.is_reply))
@UB.on(events.NewMessage(from_users=MY_ID, func=lambda e: not e.is_reply))
# async def run_task_for_event(event):
async def _(event):
    """my task"""
# need = CMD.is_new
# need += CMD.is_admin
# forbid = CMD.is_reply
# forbid += CMD.is_UB2
# CMD.add(_, need=need, forbid=forbid)


    client = event.client

    if client == NB:
        client_id = BOT_ID
        client2 = UB
    else:
        client_id = MY_ID
        client2 = NB

    cmd = await get_cmd(event)
    if NB:
        client = NB

    #https://stackoverflow.com/a/53519143
    #    if event.peer_id.broadcast:
    #    if event.from_id == None:
    # https://docs.telethon.dev/en/latest/modules/custom.html#telethon.tl.custom.chatgetter.ChatGetter
    if event.chat_id != MY_ID:
        return
    #for admin: dump msg
    msg = event.message
    #    await cmd_answer(event.original_update.stringify(), msg=event)
    if not event.forward:
        await client.send_message(event.chat_id,
                                  msg.stringify(),
                                  parse_mode=None)

    msg = event.forward
    if msg is None:
        return
    info = await get_fwd_info(event)
    await cmd_answer(info, msg=event, parse_mode="md")
#            await myprintmd(info, event=event, client=client)

    chat_id = None
    sender_id = None
    info = ""

    peer = msg.from_id
    if peer:
        sender_id = utils.get_peer_id(peer)
        if sender_id:
            info = info + "from: " + str(type(peer))
            if sender_id < 0:
                info = info + "\ncid: `" + str(sender_id) + "`"
            else:
                info = info + "\nuid: `" + str(sender_id) + "`"
#          sender_id = msg.sender_id

    peer = msg.saved_from_peer
    msg_id = msg.saved_from_msg_id
    if peer:
        chat_id = utils.get_peer_id(peer)
        if sender_id and chat_id and sender_id != chat_id:
            info = info + "\n\nchat: " + str(type(peer))
            info = info + "\ncid: `" + str(chat_id) + "`"

    if True:
        async for draft in UB.iter_drafts():
            if draft.text == "":
                msg_id = draft.reply_to_msg_id
                if msg_id is not  None:
                    msg = await UB.get_messages(draft.entity,
                                                ids=msg_id)

                    chat = msg.chat
                    if msg:
                        chat_id = msg.chat_id
                        msg_id = msg.id
                        await draft.set_message(
                            text="[" + str(msg.sender_id) +
                            "](tg://user?id=" + str(msg.sender_id) +
                            ")",
                            parse_mode="md")
                        info = "```\n" + mdraw(
                            msg.stringify(), "code"
                        ) + "\n```\n\ntg://openmessage?chat_id=" + str(
                            utils.resolve_id(chat_id)
                            [0]) + "\ntg://openmessage?user_id=" + str(
                                msg.sender_id
                            ) + "\n\nby draft\ncid: `" + str(
                                chat_id) + "`\nuid: `" + str(
                                    msg.sender_id) + "`"


    if chat_id and msg_id:
        info = info + "\nmsg link: https://t.me/c/" + str(
            utils.resolve_id(chat_id)[0]) + "/" + str(msg_id)
    if len(info) > MAX_MSG_LEN:
        info = "tg://openmessage?chat_id=" + str(
            utils.resolve_id(chat_id)
            [0]) + "\ntg://openmessage?user_id=" + str(
                msg.sender_id) + "\n\nby draft\ncid: `" + str(
                    chat_id) + "`\nuid: `" + str(msg.sender_id) + "`"
        if chat_id and msg_id:
            if not chat.username:
                if chat.is_private:
                    chat = await msg.get_sender()
                else:
                    chat = await msg.get_chat()
                if not chat.username:
                    #                chat=await client.get_entity(chat.id)
                    chat = await get_peer(chat.id, event=event)
            if chat.username:
                info = info + "\nmsg link: https://t.me/" + chat.username + "/" + str(
                    msg_id)
            else:
                info = info + "\nmsg link: https://t.me/c/" + str(
                    utils.resolve_id(chat_id)[0]) + "/" + str(msg_id)
            info = info + "\nmsg link2: tg://openmessage?chat_id=" + str(utils.resolve_id(chat_id)[0]) + "&message_id=" + str(msg_id)
        if len(msg.stringify()) > MAX_MSG_LEN:
            await myprintmd(info, event=event, client=client)
            await myprint(msg.stringify(), event=event, client=client)
        else:
            await myprint(msg.stringify(), event=event, client=client)
            await myprintmd(info, event=event, client=client)
    else:
        await myprintmd(info, event=event, client=client)
    return True








async def ok():
    info = await CMD.print_cmd()
    await NB.send_message(MY_ID, info)


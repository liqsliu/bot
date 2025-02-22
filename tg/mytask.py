from . import *  # noqa: F403
import logging

from pyrogram import StopPropagation, filters
from pyrogram.raw import functions
from pyrogram.raw import types


logger = logging.getLogger(__name__)
mp = logger.warning

#func= lambda x:x.chat_id=MY_ID and not await get_cmd(event)

from .config import cid_wtfipfs, cid_ipfsrss, cid_tw, TG_BOT_ID_FOR_MT, cid_test
from .utils import db
from .utils.tools import num2byte, byte2num
from .utils.mt import mt_send, mt_read

from .telegram import (tg_exceptions_handler, forward_msg, MSG_QUEUE, save2db, parse_msg_for_mt, parse_bridge_name, send_msg_of_queue, send_cmd_to_bash, faq_get, cmd_answer_for_my_group,
ban_chat, get_msg, set_event, get_id, is_private, is_channel, is_group,
get_sender_id, get_chat_id, is_reply, get_peer, is_edit, is_forward, is_my_group, get_msg_link)

from .telegram import CMD, cmd_answer





# async def _(event):
async def _(client, message):
    "log, just for test"
    # users = ["id", "first_name", "last_name", "username", ]
    chat_id = get_chat_id(message)
    if chat_id in (MY_ID, BOT_ID, cid_test):
        return
    if is_private(message):
        g = await save2db(message.chat, "user")
        #  await save2db(message, "message")
    elif is_channel(message):
        b = await save2db(message.chat, "channel")
    elif is_group(message):
        g = await save2db(message.chat, "chat")
        u = await save2db(message.from_user, "user", get_chat_id(message))
        m = await save2db(message, "message")
        return
        if g and u and m:
            info = f"""{g["title"]} {u["first_name"]}: {m["text"]}"""
            print(info)
    else:
        logger.error(f"unknown message: {type(message)}")
            



need = CMD.is_new
#  need = CMD.is_text
need += CMD.is_UB
forbid = CMD.is_bot
#  forbid += CMD.is_channel
CMD.add(_, need=need, forbid=forbid)





async def unpin_all(chat_id=cid_wtfipfs):
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError as e:
        return
    await UB.unpin_all_chat_messages(chat_id)


async def unpin(client, message):
    if message.sender_chat and message.sender_chat.id == cid_tw:
        #  await message.unpin()
        #  await asyncio.sleep(3)
        #  tasks = []
        for j in asyncio.all_tasks():
            #  tasks.append(j.get_name())
            if j.get_name() == "unpin_all":
                j.cancel()
        asyncio.create_task(unpin_all(), name="unpin_all")

        raise StopPropagation
    elif get_sender_id(message) == TG_BOT_ID_FOR_MT:
        put(f"wtf, need fix: {message}")
        raise StopPropagation
    else:
        mp("I: get a channel msg in wtf from: " + str(message.sender_chat.id))
#        await ban_chat(message.chat_id, message.sender_id, message=message)
        await ban_chat(client, message)
        #  await message.delete()
        raise StopPropagation


need = CMD.is_UB+CMD.is_new
need += CMD.is_my_group
need += CMD.is_anon_msg
forbid = CMD.is_out
CMD.add(unpin, need=need, forbid=forbid)


from .config import MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg

async def forward(client, message):
    "backup some channels"
    "copy them to mt"
    await forward_msg(client, message)
    raise StopPropagation


# need = CMD.is_UB+CMD.is_all
need = CMD.is_UB+CMD.is_new
need += CMD.is_channel
forbid = CMD.is_edit
CMD.add(forward, need=need, forbid=forbid)


async def chatbot(client, message):
    "chat bot"
    sender_id = get_sender_id(message)
    if sender_id == MY_ID:
        if is_reply(message):
            replied = message.reply_to_message
            if replied:
                pass
            else:
                return
            if bool(replied.text):
                lines = replied.text.split("\n")
            else:
                return
            if lines[0] == "new msg":
                target_id = int(lines[-1].split(" ")[1])
                # target = await client.get_entity(target_id)
                target = await get_peer(target_id)
                if target:
                    if target.status:
                        msg_t = await message.forward(target_id)
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
        chat_id = get_chat_id(message)
        msg_info = "new msg\n"
        from_info = "\nmsg_id " + str(message.id) + "\nfrom " + str(
            sender_id) + " tg://openmessage?user_id=" + str(sender_id)
        if is_private(message):
            chat = await get_peer(MY_ID)
            if chat.status:
                msg = await message.forward(MY_ID)
                await msg.reply(msg_info + from_info)
                if CMD.check_cmd(client, message):
                    pass
                else:
                    await client.send_message(chat_id, "msg has been sent")
            else:
                if message.text and message.text[0] == "/":
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
            if message.mentioned:
                # album no
                msg = await message.forward(MY_ID)
                chat_info = "\nchat_id: " + str(chat_id) + " tg://openmessage?chat_id=" + str(chat_id)
                await msg.reply(msg_info + chat_info + from_info)

need = CMD.is_NB+CMD.is_new
#need = CMD.is_NB+CMD.is_all
#need += CMD.is_private
forbid = 0
forbid = CMD.is_out
CMD.add(chatbot, need=need, forbid=forbid)










# asyncio.create_task(send_msg_of_queue(), name="tg_send")

# for msg order
locks = {}
# read msg from matterbridge api
asyncio.create_task(mt_read(MSG_QUEUE), name="mt_read")

async def send2mt(client, message):
    "get msg for matterbridge api"
    chat_id = get_chat_id(message)
    if chat_id in MT_GATEWAY_LIST_for_tg:
        sender_id = get_sender_id(message)
#        logger.warning(f"send 2 mt: {message.raw_text}")
        logger.debug("start to mt")
#        if message.fwd_from:
        if is_forward(message):
            if sender_id == cid_tw:
                logger.info("I: ignore a msg from tw")
                raise StopPropagation
#        if message.sender_id == 1494863126:
            # wtfipfsbot
#            pass
        if sender_id == 420415423:
            # t2bot
            if message.text.startswith("bot: "):
                await message.delete()
                raise StopPropagation
        if MT_GATEWAY_LIST_for_tg[chat_id] == "gateway5":  # need not to send in order
            if is_edit(message):
                raise StopPropagation
            msg = await parse_msg_for_mt(client, message)
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
                msg = await parse_msg_for_mt(client, message)  # return [text, username, gateway, qt]
                if msg:
                    if sender_id == BOT_ID:
                        pass
                    elif sender_id == TG_BOT_ID_FOR_MT:
                        pass
                    elif await parse_bridge_name(msg[1].rstrip(": ")):
                        msg[1] = await parse_bridge_name(msg[1].rstrip(": "))
                    else:
                        #  if is_my_group(client, message):
                        # if is_me(client, message):
                            #  print(message)
                            #  print(msg)
                        await mt_send(msg[0], msg[1], msg[2], msg[3])
                    #  if message.media is not None:
                    #      return
                    if not is_my_group(client, message):
                        return
                    if msg[2] == "gateway11":
                        msg[2] = "gateway1"
                    #for cmd answer
                    if msg[1].endswith(": "):
                        msg[1] = msg[1].strip(": ")
                    if msg[1] != "C bot":
                        if await CMD.check_cmd(client, message):
                            logger.debug("cmd ok")
                            pass
                        else:
                            text = msg[0]
                            #  cmd = text.split(': ', 1)[1]
                            cmd = text
                            faq = await faq_get(cmd)
                            if faq:
                                await cmd_answer_for_my_group(faq, message)
                                
                            elif cmd.startswith('.'):
                                logger.info("use bash")
                                asyncio.create_task(send_cmd_to_bash(msg))
                                raise StopPropagation
#        if message.out:
#            raise StopPropagation



need = CMD.is_UB+CMD.is_new
#  need += CMD.is_group
#  forbid = CMD.is_me
forbid = 0
CMD.add(send2mt, need=need, forbid=forbid)

#  need = CMD.is_UB2+CMD.is_new
#  need += CMD.is_me
#  forbid = 0
#  CMD.add(send2mt, need=need, forbid=forbid)


from .utils.tools import put
from .telegram import cmd_answer


@NB.on_message(filters.chat(MY_ID) & ~filters.reply)
@tg_exceptions_handler
async def my_task(client, message):
    """my task"""

    #  from .telegram import cmd_answer
    #  put(str(type(cmd_answer)))
    #  res = await client.send_message(MY_ID, message)

    msg = None
    drafts = await UB.invoke(functions.messages.GetAllDrafts())
    if drafts.updates:

        for d in drafts.updates:
            if d.peer:
                chat_id = await get_id(d.peer)
                info = f"{d}\n\ntype: {type(d)}"
                if chat_id < 1:
                    info += "\ncid: " + str(chat_id)
                else:
                    info += "\nuid: " + str(chat_id)
                #  res = await cmd_answer(info, client=NB, msg=message, parse_mode=enums.ParseMode.MARKDOWN)
                res = await cmd_answer(info, client=NB, msg=message)
                await asyncio.sleep(3)

        for d in drafts.updates:
            if d.peer and await get_id(d.peer) == -747790754:
                print(d)
                put(f"wtf draft: {d}")
                continue
            if d.draft.reply_to_msg_id:
                try:
                    msg = await get_msg(await get_id(d.peer, client=UB), d.draft.reply_to_msg_id, client=UB)
                except Exception as e:
                    print(d)
                    logger.error(e)
                    continue
                break
        await UB.invoke(functions.messages.ClearAllDrafts())
    else:
        res = await cmd_answer(message, client=NB, msg=message)

    if msg:
        #  text="[" + str(msg.sender_id) + "](tg://user?id=" + str(msg.sender_id) + ")",
        sender_id = get_sender_id(msg)
        res = await UB.invoke(
                functions.messages.SaveDraft(
                    peer = await UB.resolve_peer(await get_id(d.peer, client=UB)),
                    message = str(sender_id),
                    reply_to_msg_id = msg.id,
                    entities = [
                        #  types.MessageEntityMentionName(
                        types.InputMessageEntityMentionName(
                            offset = 0,
                            length = len(str(sender_id)),
                            #  user_id = sender_id
                            user_id = await UB.resolve_peer(sender_id)
                        )
                    ]
                )
            )
        chat_id = get_chat_id(msg)
        info = "by draft\ncid: `" + str(chat_id) + "`"
        if sender_id != chat_id:
            if sender_id < 0:
                info += "\ncid: `" + str(sender_id) + "`"
            else:
                info += "\nuid: `" + str(sender_id) + "`"
        if msg.link:
            info += f"\nlink: {msg.link}"
        else:
            info += f"\nlink: {await get_msg_link(msg)}"
        res = await cmd_answer(info, client=NB, msg=message)
    return True





async def ok():
    info = await CMD.print_cmd()
    await NB.send_message(MY_ID, info)


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))


else:
    print('{} 运行'.format(__file__))
    asyncio.create_task(ok())

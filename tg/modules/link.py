#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)

from ..telegram import get_msg_from_url
from ..telegram import get_fwd_info, is_reply, get_real_id


async def _(client, event):

    #  chat_id = get_chat_id(event)
    #  sender_id = get_sender_id(event)
    info = ""
    cmd = await get_cmd(client, event)

    if is_reply(event):
        msg = event.reply_to_message
        url = None
    elif len(cmd) == 1:
        info = "link url"
        return await cmd_answer(info, client, event)
    else:
        url = cmd[1]
        #          chat=utils.resolve_id(cid)[1]
        if len(cmd) == 3:
            client = globals()[cmd[2]]
            msg = await get_msg_from_url(cmd[1], client=client)
        else:
            msg = await get_msg_from_url(cmd[1], client)
    if msg:
        info = str(msg)
        event = await cmd_answer(info, client, event)
        chat_id = get_chat_id(msg)
        sender_id = get_sender_id(msg)
        sender = get_sender(msg)

        info = ""
        info += "tg://openmessage?chat_id=" + str(get_real_id(msg.chat))
        info += "\ncid: `" + str(chat_id) + "`"
        if sender_id and chat_id != sender_id:
            if sender_id > 0:
                info += "\n\ntg://openmessage?user_id=" + str(sender_id)
                info += "\nuid: `" + str(sender_id) + "`"
            else:
                info += "\n\ntg://openmessage?chat_id=" + str(get_real_id(sender))
                info += "\ncid: `" + str(sender_id) + "`"
        if url is not None and "?comment=" in url:
            chat = msg.chat
            if chat.username:
                info += "\n\nmsg link: https://t.me/" + chat.username + "/" + str(msg.message_id)
            else:
                info += "\n\nmsg link: https://t.me/c/" + str(get_real_id(chat)) + "/" + str(msg.message_id)
            info += f"\nlinked channel: {url.split('?',1)[0]}"


        event = await cmd_answer(info, client, event, parse_mode=enums.ParseMode.MARKDOWN)
        if msg.forward_date:
            info = await get_fwd_info(client, msg)
            if info:
                event = await cmd_answer(info, client, event, parse_mode=enums.ParseMode.MARKDOWN)
    else:
        #          info=mdraw(msg.stringify(),"code")
        info = "no msg"
        return await cmd_answer(info, client, event)

#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

from ..utils.telegram import get_msg_from_url
from ..utils.tools import url_re

from ..utils import db


logger = logging.getLogger(__name__)
mp = logger.info

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
    info = ""
    if len(cmd) == 1:
        info = "msg link"
        await cmd_answer(info, event)
    elif url_re.search(cmd[1]):
        url = url_re.search(cmd[1])
        url = url.group()
        msg = await get_msg_from_url(url, event)
        if not msg:
            await cmd_answer("null", event)
            return

        await msg.client.send_message(MY_ID, message=msg)
    elif cmd[1] == "se":
        if len(cmd) == 3:
            res = db.search(" ".join(cmd[2:]))
            if res is not None:
                info = ""
                for i in res:
                    info += f"{i['chat_id']} {i['id']} {i['text']}"
                    info += "\n"
                info = info.strip()
    else:
        info = "msg link?"
    if info:
        pass
    else:
        info = "None"
    await cmd_answer(info, event)


cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

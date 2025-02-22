#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)

mp = logger.info

from ..utils.telegram import set_bot_cmd

from ..cmd import CMD

async def _(event):
    "print help info"
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  await UB.send_message(MY_ID, "ok")
    client = event.client
    if client == NB:
        await set_bot_cmd(event)
    chat_id = event.chat_id
    if chat_id == MY_ID:
        info = await CMD.print_cmd()
#        await client.send_message(event.chat_id, "ok")
    else:
        info = await CMD.list_cmd(event)
    await cmd_answer(info, event)



need = need ^ CMD.is_admin

cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

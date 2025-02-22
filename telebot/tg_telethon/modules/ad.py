from . import *

logger = logging.getLogger(__name__)

mp = logger.info

from ..utils.telegram import get_admins

async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  await UB.send_message(MY_ID, "ok")
    client = event.client
    #  await client.send_message(event.chat_id, "use cmd")
    cmd = await get_cmd(event)

    if cmd[0] == "ad":
        #        info=await get_admin_of_channel(cmd[1])
        info = await get_admins(cmd[1])
        await cmd_answer(info, event)




cmd = __name__.split(".")[-1]

CMD.add(_, cmd=cmd, need=need, forbid=forbid)


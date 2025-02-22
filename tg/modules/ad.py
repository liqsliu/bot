from . import *

logger = logging.getLogger(__name__)


from ..telegram import get_admins

async def _(client, message):
    cmd = await get_cmd(client, message)

    #  if cmd[0] == "ad":
    if len(cmd) == 1:
        cmd.append(get_chat(message))
        #        info=await get_admin_of_channel(cmd[1])
    info = await get_admins(cmd[1], client=UB)
    await cmd_answer(info, client, message, parse_mode=enums.ParseMode.MARKDOWN)



from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_popen, is_group

async def _(client, message):
    "echo"
    cmd = await get_cmd(client, message)
    if len(cmd) == 1:
        if is_group(client, message):
            await cmd_answer("/{}@{} helloworld".format(cmd[0], BOT_NAME), client, msg=message)
        else:
            await cmd_answer("/{} helloworld".format(cmd[0]), client, msg=message)
    else:
        #  await my_popen(cmd, shell=False, client=client, msg=message)
        await my_popen(" ".join(cmd), client=client, msg=message)


#need = need ^ CMD.is_me
#need = need | CMD.is_my_group

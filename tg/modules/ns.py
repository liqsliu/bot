from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_popen

async def _(client, message):
    cmd = await get_cmd(client, message)
    times = 5
    if len(cmd) == 1:
        pass
    else:
        if cmd[1].isnumeric():
            times = cmd[1]
        else:
            await cmd_answer("need a number", client, message)
            return
    await my_popen("{}/ns.sh {}".format(SH_PATH, times), shell=True, msg=message, client=client)


from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..telegram import my_popen


async def _(client, event):
    "bash -c 'free -h'"
    cmd = await get_cmd(client, event)
    if cmd[0] == "free":
        await my_popen("free -h; echo; df -h", client=client, msg=event)


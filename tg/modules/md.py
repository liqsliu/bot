from . import *

logger = logging.getLogger(__name__)


async def _(client, event):
    "print str in markdown mode"
    cmd = await get_cmd(client, event)
    await cmd_answer(" ".join(cmd[1:]), client, event, parse_mode="md")

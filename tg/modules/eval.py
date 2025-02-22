from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_eval


from .exec import async_exec

async def _(client, event):
    "exec"
    msg = event
    cmd = await get_cmd(client, event)
    cmd_str = None
    parse_mode = None
    if len(cmd) == 1:
        info = "eval 1+1"
    elif cmd[1] == "md":
        cmd_str = " ".join(cmd[2:])
        parse_mode="md"
    else:
        cmd_str = " ".join(cmd[1:])
    if cmd_str:
        try:
            info = await async_exec(cmd_str, event)
        except:
            info = "E: "
            info += str(sys.exc_info())
    await cmd_answer(info, client, msg, parse_mode=parse_mode)


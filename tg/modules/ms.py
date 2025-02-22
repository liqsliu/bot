from . import *

logger = logging.getLogger(__name__)

from ..utils.morse import encode, decode


async def _(client, event):
    "morse code(encode/decode)"
    cmd = await get_cmd(client, event)
    if len(cmd) == 1:
        info = "morse code"
        info += "\nms e str"
        info += "\nms [d] str"
    elif cmd[1] == "e":
        info = encode(" ".join(cmd[2:]))
    elif cmd[1] == "d":
        info = decode(" ".join(cmd[2:]))
    else:
        info = decode(" ".join(cmd[1:]))

    await cmd_answer(info, client, event)

need = need & ~CMD.is_me

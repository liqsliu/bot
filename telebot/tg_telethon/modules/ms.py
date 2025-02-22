#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
#from ..bot import *

from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.morse import encode, decode


async def _(event):
    "morse"
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    cmd = await CMD.get_cmd(event)
    if len(cmd) == 1:
        info = "morse code"
        info += "\nms e str"
        info += "\nms d str"
    elif cmd[1] == "e":
        info = encode(" ".join(cmd[2:]))
    elif cmd[1] == "d":
        info = decode(" ".join(cmd[2:]))
    else:
        info = decode(" ".join(cmd[1:]))

    await cmd_answer(info, event)







need = need & ~CMD.is_admin
cmd = __name__.split(".")[-1]

CMD.add(_, cmd=cmd, need=need, forbid=forbid)

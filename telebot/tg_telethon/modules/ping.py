#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info


async def _(event):
    "pong"
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    await event.reply("pong")

cmd = __name__.split(".")[-1]

need = need & ~CMD.is_admin

CMD.add(_, cmd=cmd, need=need, forbid=forbid)



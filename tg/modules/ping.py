#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)


async def _(client, message):
    "pong"
    #  await message.reply("pong")
    return await cmd_answer("pong", client, message)



need = need & ~CMD.is_me

# CMD.add(_, cmd=__name__.split(".")[-1], need=need, forbid=forbid)


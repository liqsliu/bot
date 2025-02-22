#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)

mp = logger.info

async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    result = await client.send_message(event.chat_id,
                                       event.raw_text.split(" ", 1)[1],
                                       parse_mode="htm")
    await client.send_message(event.chat_id, result.stringify())




cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

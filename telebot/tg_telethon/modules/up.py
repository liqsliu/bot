#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info


from telethon import functions

async def _(event):
    client = event.client
    peer = await get_peer(event.chat_id, event=event)
    result = await client(functions.messages.UnpinAllMessagesRequest(peer=peer)
                          )
    #  print(result.stringify())
    msg = await cmd_answer("ok", event)
    await asyncio.sleep(5)
    await msg.delete()
    raise StopPropagation



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

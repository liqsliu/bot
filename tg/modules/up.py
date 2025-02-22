from . import *

logger = logging.getLogger(__name__)


from telethon import functions

async def _(client, message):
    "unpin all msg"
    chat_id = get_chat_id(message)
    await client.unpin_all_chat_messages(chat_id)
    await cmd_answer("ok", client, message)


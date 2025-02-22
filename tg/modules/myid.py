from . import *

logger = logging.getLogger(__name__)

async def _(client, message):
    "get telegram id"
    await message.reply(str(get_sender_id(message)))



need = need & ~CMD.is_me

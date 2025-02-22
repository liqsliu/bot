from . import *

logger = logging.getLogger(__name__)

async def _(client, event):
    "set log level"
    cmd = await get_cmd(client, event)
    chat_id = get_chat_id(event)
    if len(cmd) == 1:
        LOGGER.setLevel(logging.INFO)
        await client.send_message(chat_id, "info")
    elif cmd[1] == "d":
        LOGGER.setLevel(logging.DEBUG)
        #    OUT.setLevel(logging.DEBUG)
        await client.send_message(chat_id, "debug")
    elif cmd[1] == "i":
        LOGGER.setLevel(logging.INFO)
        await client.send_message(chat_id, "info")
    elif cmd[1] == "w":
        LOGGER.setLevel(logging.WARNING)
        await client.send_message(chat_id, "warning")
    elif cmd[1] == "e":
        LOGGER.setLevel(logging.ERROR)
        #    OUT.setLevel(logging.ERROR)
        await client.send_message(chat_id, "error")
    else:
        await client.send_message(chat_id, "info?")


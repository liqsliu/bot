#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

async def _(event):
    "set log level"
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    #    await run_task_for_event(event)
    #    await event.reply("pong")
    client = event.client
    cmd = await get_cmd(event)
    if len(cmd) == 1:
        LOGGER.setLevel(logging.INFO)
        await client.send_message(event.chat_id, "info")
    elif cmd[1] == "d":
        LOGGER.setLevel(logging.DEBUG)
        #    OUT.setLevel(logging.DEBUG)
        await client.send_message(event.chat_id, "debug")
    elif cmd[1] == "i":
        LOGGER.setLevel(logging.INFO)
        await client.send_message(event.chat_id, "info")
    elif cmd[1] == "w":
        LOGGER.setLevel(logging.WARNING)
        await client.send_message(event.chat_id, "warning")
    elif cmd[1] == "e":
        LOGGER.setLevel(logging.ERROR)
        #    OUT.setLevel(logging.ERROR)
        await client.send_message(event.chat_id, "error")
    else:
        await client.send_message(event.chat_id, "?")






cmd = __name__.split(".")[-1]

CMD.add(_, cmd=cmd, need=need, forbid=forbid)


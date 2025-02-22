#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import my_popen



async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  mp("{}: ping".format(event.sender_id, event.raw_text))
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    #    await run_task_for_event(event)
    #    await event.reply("pong")
    #  await UB.send_message(MY_ID, "ok")

    client = event.client
    cmd = await get_cmd(event)
    tasks = []
    for j in asyncio.all_tasks():
        tasks.append(j.get_name())
    info = "queue: {}\nall tasks: {}\n{}".format(MSG_QUEUE.qsize(), len(tasks),
                                                 "\n".join(tasks))
    await client.send_message(event.chat_id, info)

    await my_popen(event.raw_text.lstrip("./"), msg=event)

    if len(cmd) > 1:
        for j in asyncio.all_tasks():
            if cmd[1] == j.get_name():
                await client.send_message(event.chat_id, str(j))

    msg = event.message
    await my_popen("{}/ns.sh {}".format(SH_PATH, 5), shell=True, msg=msg)


cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

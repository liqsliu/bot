#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import my_popen

async def _(event):
    logger.info("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    msg = event.message
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    #    await run_task_for_event(event)
    #    await event.reply("pong")
    #  await UB.send_message(MY_ID, "ok")

    #  await my_popen(event.raw_text.lstrip("./"), msg=event)
    cmd = await get_cmd(event)
    #  asyncio.create_task(my_exec(" ".join(cmd[1:]), msg=event), name="py")
    #  await my_exec(" ".join(cmd[1:]), msg=event.message)
    #  await client.send_message(event.chat_id, "end")
    times = 5
    if len(cmd) == 1:
        pass
    else:
        if cmd[1].isnumeric():
            times = cmd[1]
        else:
            await cmd_answer("need number", event)
            return


#  shell_cmd=[times]
    await my_popen("{}/ns.sh {}".format(SH_PATH, times), shell=True, msg=msg)


cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

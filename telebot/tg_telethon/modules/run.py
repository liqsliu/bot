#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import my_eval



from .exec import async_exec

async def _(event):
    mp("cmd {}: {}: {}".format(
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
    #  await client.send_message(event.chat_id, "end")
    parse_mode="md"
    if len(cmd) == 1:
        info = "run return 1+1"
    else:
        cmd_str = " ".join(cmd[1:])
        res = await async_exec(cmd_str, event)

        info = """**run**:
```{}```

**return**:
```{}```""".format(cmd_str, res)
    await cmd_answer(info, msg, parse_mode=parse_mode)



    return
    info = ""
    try:
#        info = exec(cmd_str)
        for i in cmd_str.splitlines():
            tmp = exec(i)
            if asyncio.iscoroutine(tmp):
                tmp = await tmp
            if tmp:
                info += str(tmp)
                info += "\n"
    except:
        if info:
            info += "\n"
        info += "E: "
        info += str(sys.exc_info())
    await cmd_answer(info, msg, parse_mode=parse_mode)



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

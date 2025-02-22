#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import my_popen

#pattern=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( |$)')

async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
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
    #  msg=event.message
    msg = event
    if len(cmd) == 1:
        info = """run shell
sh c: cpu top 10
sh m: mem top 10
"""
        #          await myprint(info)
        await cmd_answer(info, msg)
    elif len(cmd) == 2:
        if cmd[1] == "c":
            shell_cmd = "ps -eo user,pid,pcpu,pmem,args --sort=-pcpu  |head -n 10"
        elif cmd[1] == "cc":
            shell_cmd = "ps -eo user,pcpu,pmem,args --sort=-pcpu  |head -n 10"
        elif cmd[1] == "ccc":
            shell_cmd = "ps -eo pcpu,args --sort=-pcpu  |head -n 10"
        elif cmd[1] == "m":
            shell_cmd = "ps -eo user,pid,pcpu,pmem,args --sort=-pmem  |head -n 10"
        elif cmd[1] == "mm":
            shell_cmd = "ps -eo user,pcpu,pmem,args --sort=-pmem  |head -n 10"
        elif cmd[1] == "mmm":
            shell_cmd = "ps -eo pmem,args --sort=-pmem  |head -n 10"
        else:
            shell_cmd = cmd[1]
        await my_popen(shell_cmd, msg=msg)
    else:
        await my_popen(" ".join(cmd[1:]), shell=True, msg=msg)



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

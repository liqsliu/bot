#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import my_eval

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
    if cmd[0] == "p" or cmd[0] == "cal":
        if len(cmd) == 1:
            code = '''https://docs.python.org/zh-cn/3/howto/unicode.html'''
            code = '"""' + code + '"""'
            await my_eval(code, msg=msg)
        elif cmd[1] == "md":
            await my_eval(event.raw_text.split(' ', 2)[2], msg=msg, parse_mode="md")
        elif cmd[1] == "hm":
            await my_eval(event.raw_text.split(' ', 2)[2], msg=msg, parse_mode="hm")
        else:
            await my_eval(event.raw_text.split(' ', 1)[1], msg=msg)



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

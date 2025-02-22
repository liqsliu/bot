#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info


async def __async_exec(code, event=None):
    # https://stackoverflow.com/a/67199177
    t = [None]
    exec('async def _async_exec(event):\n return {}\nt[0] = asyncio.ensure_future(_async_exec(event))'.format(code))
    return await t[0]


async def async_exec(code, event=None):
#    if "\n" not in code:
#        code = " return " + code
#    else:
    tmp = code.splitlines()
    if not tmp[-1].startswith("return "):
        tmp[-1] = "return " + tmp[-1]
    code = "\n ".join(tmp)
    try:
        res = [None]
        exec("""async def _async_exec(event):
 {}
res[0] = asyncio.create_task(_async_exec(event))""".format(code))
        info = await res[0]
        if asyncio.iscoroutine(info):
            info = await info
    except:
        info = "E: "
        info += str(sys.exc_info())
    return info

async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    msg = event.message
    cmd = await get_cmd(event)
    #  await client.send_message(event.chat_id, "end")
    parse_mode=None
    cmd_str = None
    if len(cmd) == 1:
        info = "exec return 1+1"
    elif cmd[1] == "md":
        cmd_str = " ".join(cmd[2:])
        parse_mode="md"
    else:
        cmd_str = " ".join(cmd[1:])

    if cmd_str:
        try:
            info = await async_exec(cmd_str, event)
        except:
            info = "E: "
            info += str(sys.exc_info())
    if info:
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
    if info:
        await cmd_answer(info, msg, parse_mode=parse_mode)





cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)



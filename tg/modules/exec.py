from . import *

logger = logging.getLogger(__name__)
mp = logger.info


async def __async_exec(code, event=None):
    # https://stackoverflow.com/a/67199177
    t = [None]
    exec('async def _async_exec(event):\n return {}\nt[0] = asyncio.ensure_future(_async_exec(event))'.format(code))
    return await t[0]


async def async_exec(code, client=None, message=None, timeout=55):
#    if "\n" not in code:
#        code = " return " + code
#    else:
    tmp = code.splitlines()
    if not tmp[-1].startswith("return "):
        tmp[-1] = "return " + tmp[-1]
    code = "\n ".join(tmp)
    try:
        res = [None]
        exec("""async def _async_exec(client, message):
 {}
res[0] = asyncio.create_task(_async_exec(client, message))""".format(code))
        #  info = await res[0]
        if timeout:
            info = await asyncio.wait_for(res[0], timeout=timeout)
        else:
            info = await asyncio.wait_for(res[0], timeout=None)
        if asyncio.iscoroutine(info):
            info = await info
    except Exception as e:
        info = f"E: {e=}"
        from ..utils.tools import my_traceback
        my_traceback(e)
    return info

async def _(client, message):
    "exec with trackback, return the original res"
    cmd = await get_cmd(client, message)
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
            info = await async_exec(cmd_str, client, message)
        except Exception as e:
            info = f"E: {e=}"
            from ..utils.tools import my_traceback
            my_traceback(e)
    if info:
        await cmd_answer(str(info), client, message, parse_mode=parse_mode)



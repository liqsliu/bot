from . import *

logger = logging.getLogger(__name__)
from ..telegram import my_eval


async def _(client, event):
    "eval of python"
    msg = event
    cmd = await get_cmd(client, event)
    if len(cmd) == 1:
        code = '''https://docs.python.org/zh-cn/3/howto/unicode.html'''
        code = '"""' + code + '"""'
        await my_eval(code, client=client, msg=msg)
    else:
        code = " ".join(cmd[1:])
    await my_eval(code, client=client, msg=msg)


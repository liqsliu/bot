#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_eval

async def _(client, event):
    msg = event
    cmd = await get_cmd(client, event)
    if cmd[0] == "p" or cmd[0] == "cal":
        if len(cmd) == 1:
            code = '''https://docs.python.org/zh-cn/3/howto/unicode.html'''
            code = '"""' + code + '"""'
            await my_eval(code, client=client, msg=msg)
        elif cmd[1] == "md":
            await my_eval(event.text.split(' ', 2)[2], client=client, msg=msg, parse_mode=enums.ParseMode.MARKDOWN)
        elif cmd[1] == "html":
            await my_eval(event.text.split(' ', 2)[2], client=client, msg=msg, parse_mode=enums.ParseMode.HTML)
        else:
            await my_eval(event.text.split(' ', 1)[1], client=client, msg=msg, parse_mode=enums.ParseMode.DISABLED)


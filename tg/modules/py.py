#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..telegram import my_exec

async def _(client, message):
    cmd = await get_cmd(client, message)
    if len(cmd) == 1:
        info="__test__"
        await client.send_message(MY_ID, info, parse_mode=enums.ParseMode.MARKDOWN)
    elif cmd[1] == "md":
        info="markdown mode"
        await client.send_message(MY_ID, info, parse_mode=enums.ParseMode.MARKDOWN)
        cmd_str = " ".join(cmd[2:])
        await my_exec(cmd_str, msg=message, parse_mode=enums.ParseMode.MARKDOWN)
    elif cmd[1] == "run":
        cmd_str = " ".join(cmd[1:])
        await my_exec(cmd_str, msg=message)
    else:
        cmd_str = " ".join(cmd[1:])
#        await my_exec(cmd_str, msg=message.message)
#        return
        res = await my_exec(cmd_str)
        info = """**python**:
```{}```

**out**:
```{}```""".format(cmd_str, res)
        chat_id = get_chat_id(message)
        await client.send_message(chat_id, info, parse_mode=enums.ParseMode.MARKDOWN)



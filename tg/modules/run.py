#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..telegram import my_eval

from .exec import async_exec

init = """chat = message.chat
chat_id = get_chat_id(message)
cid = chat_id
reply = message.reply_to_message
if reply:
    sender = get_sender(reply)
    sender_id = get_sender_id(reply)
    uid = sender_id
    mid = reply.id
    media = reply.media
    link = reply.link
"""

async def _(client, message):
    "run and print in md"
    cmd = await get_cmd(client, message)
    parse_mode=enums.ParseMode.MARKDOWN
    timeout = 300
    if len(cmd) == 1:
        info = "run return 1+1"
        await cmd_answer(info, client, message, parse_mode=parse_mode)
        return
    elif cmd[1].isnumeric():
        timeout=int(cmd[1])
        cmd_str = " ".join(cmd[2:])
    else:
        cmd_str = " ".join(cmd[1:])
        #  cmd.insert(1, init)
    res = await async_exec(init+cmd_str, client, message, timeout=timeout)

    info = """**run**:
```{}```

**return**:
```{}```""".format(cmd_str, res)
    await cmd_answer(info, client, message, parse_mode=parse_mode)




# CMD.add(_, cmd=__name__.split(".")[-1], need=need, forbid=forbid)

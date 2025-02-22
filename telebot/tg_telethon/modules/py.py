#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.telegram import my_exec

#pattern=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( |$)')

async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    cmd = await get_cmd(event)
    #  asyncio.create_task(my_exec(" ".join(cmd[1:]), msg=event), name="py")
    client=event.client
    if len(cmd) == 1:
        info="__test__"
        await client.send_message(MY_ID, info, parse_mode="md")
#        info="\_\_test\_\_"
#        await client.send_message(MY_ID, info, parse_mode="md")
#        info="```__test__```"
#        await client.send_message(MY_ID, info, parse_mode="md")
#        info="```__te\`st__```"
#        await client.send_message(MY_ID, info, parse_mode="md")
#        info="```__te\\`st__```"
#        await client.send_message(MY_ID, info, parse_mode="md")
    elif cmd[1] == "md":
        info="markdown mode"
        await client.send_message(MY_ID, info, parse_mode="md")
        cmd_str = " ".join(cmd[2:])
        await my_exec(cmd_str, msg=event.message, parse_mode="md")
    elif cmd[1] == "run":
        cmd_str = " ".join(cmd[1:])
        await my_exec(cmd_str, msg=event.message)
    else:
        cmd_str = " ".join(cmd[1:])
#        await my_exec(cmd_str, msg=event.message)
#        return
        res = await my_exec(cmd_str)
        info = """**python**:
```{}```

**out**:
```{}```""".format(cmd_str, res)
        await client.send_message(event.chat_id, info, parse_mode="md")


#  await client.send_message(event.chat_id, "end")


cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)




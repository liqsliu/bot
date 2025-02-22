#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..telegram import my_popen

#pattern=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( |$)')

async def _(client, event):
    cmd = await get_cmd(client, event)
    msg = event
    if len(cmd) == 1:
        info = """run shell
sh c: cpu top 10
sh m: mem top 10
"""
        await cmd_answer(info, client=client, msg=msg)
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
        await my_popen(shell_cmd, client=client, msg=msg)
    else:
        await my_popen(" ".join(cmd[1:]), client=client, msg=msg)



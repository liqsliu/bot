#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

from ..utils.tools import ennum, denum, denum_auto, chr_list, enstr, destr

logger = logging.getLogger(__name__)
mp = logger.info

async def _(event):
    "str to num to sapce"
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
#    await event.reply("pong")
#    if event.chat_id == MY_ID:

    cmd = await get_cmd(event)
    if len(cmd) == 1:
        info = "num [d] $spaces"
        info += "\nnum e $str"
        info += "\nnum sd $spaces"
        info += "\nnum se $str"
        s = ""
        for i in range(len(chr_list)):
            s += "\n{}{}".format(i, ascii(chr_list[i])[1:-1])
        info += s
        info += "\n\nall: "+str(len(chr_list))

    elif cmd[1] == "e":
        info = ennum(int(cmd[2]))
        await cmd_answer(f"{info}", event)
        if info is not None:
            info = '"{}"'.format(info)
    elif cmd[1] == "se":
        info = enstr(" ".join(cmd[2:]))
        await cmd_answer(f"{info}", event)
        if info is not None:
            info = '"{}"'.format(info)
    elif cmd[1] == "sd":
        info = destr(" ".join(cmd[2:]))
    elif cmd[1] == "d":
        info = denum(cmd[2])
    else:
        info = denum_auto(" ".join(cmd[1:]))
    await cmd_answer(f"{info}", event)



need = need & ~CMD.is_admin

cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

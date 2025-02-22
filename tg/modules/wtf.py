from . import *

logger = logging.getLogger(__name__)

from ..telegram import set_bot_cmd, get_chat_id

from ..utils.tools import nbnhhsh, wtf


async def _(client, message):
    "wtf nbnhhsh"
    #  chat_id = get_chat_id(message)
    cmd = await get_cmd(client, message)
    info = ""
    if len(cmd) == 1:
        info = "能不能好好说话?"
        info += "\n拼音首字母缩写释义工具"
        info += "\n用法: wtf 缩写"
        info += "\n"
        info += "\nlink: https://lab.magiconch.com/nbnhhsh"
        #  info += "\nlink: https://lab.magiconch.com/api/nbnhhsh/guess"
        info += "\nhttps://api.muxiaoguo.cn/api/hybrid"
    #  elif cmd[0] == "wtf":
    #      info = await wtf(cmd[1])
    #  elif cmd[0] == "hhsh":
    #      info = await nbnhhsh(cmd[1])
    #  elif cmd[0] == "nbnhhsh":
    #      info = await nbnhhsh(cmd[1])
    #      info += "\n\n"
    #      info += await wtf(cmd[1])
    #  else:
    #      info = await wtf(cmd[1])
    else:
        info = await nbnhhsh(cmd[1])
    await cmd_answer(info, client, message, parse_mode=enums.ParseMode.MARKDOWN)



need = need ^ CMD.is_me


# cmd of wtf will be added automatically
CMD.add(_, "hhsh", need, forbid)
CMD.add(_, "nbnhhsh", need, forbid)



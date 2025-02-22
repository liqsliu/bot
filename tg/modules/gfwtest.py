from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_popen, text2link, get_info_from_bot


async def _(client, event):
    "gfwtest"
    msg = event
    chat_id = get_chat_id(event)
    cmd = await get_cmd(client, event)
    if len(cmd) == 1:
        #  info = await get_info_from_bot("/"+" ".join(cmd), uid=573173175, key="使用方式")
        #  info = info.replace("/gfwtest", ".gfwtest")
        info = "使用方式: .gfwtest dns [host]"
        info += "\n使用方式: .gfwtest tcp [host] [port]"
        info += "\n--"
    else:
        info = await get_info_from_bot("/"+" ".join(cmd), uid=573173175, skip="正在请求中")
    if info:
        info += "\ntelegram bot: @WooMaiBot"
#        info += "\n----\n"
    else:
        info = ""

    await cmd_answer(info, client, event)


need = need ^ CMD.is_me

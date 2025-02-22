from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_popen, text2link, get_info_from_bot, send_cmd_to_bash





async def _(client, event):
    "ip domain/ip"
    msg = event
    chat_id = get_chat_id(event)

    cmd = await get_cmd(client, event)
    info = "{}".format(await send_cmd_to_bash("."+" ".join(cmd)))
    await cmd_answer(info, client, event)
    if len(cmd) == 1:
        info = await get_info_from_bot("/ip", uid=573173175, key="使用方式")
    else:
#        info = await get_info_from_bot("/ipinfo "+" ".join(cmd[1:]), uid=573173175, key="查询目标", skip="正在查询")
        url = " ".join(cmd[1:])
        if "://" in url:
            url = url.split("/")[2]
        info = await get_info_from_bot("/ip "+url, uid=573173175, skip="正在查询")
    if info:
        #  info = info.replace("/ipinfo ", ".ip ")
        if len(cmd) == 1:
            info += "\n--\n"
            info += "\ntelegram bot: @WooMaiBot"
        #  info += "\n----\n"
    else:
        info = ""

    await cmd_answer(info, client, event)


need = need & ~CMD.is_me

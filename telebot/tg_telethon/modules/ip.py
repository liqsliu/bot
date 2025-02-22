#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

from . import *

logger = logging.getLogger(__name__)

from ..utils.telegram import my_popen, text2link, get_info_from_bot, send_cmd_to_bash


async def _(event):
    "ip domain/ip"
    logger.info("cmd {}: {}: {}".format( __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    msg = event.message
    chat_id = event.chat_id

    cmd = await get_cmd(event)
    if len(cmd) == 1:
        info = await get_info_from_bot("/ipinfo "+" ".join(cmd[1:]), uid=573173175, key="使用方式")
    else:
#        info = await get_info_from_bot("/ipinfo "+" ".join(cmd[1:]), uid=573173175, key="查询目标", skip="正在查询")
        info = await get_info_from_bot("/ipinfo "+" ".join(cmd[1:]), uid=573173175, skip="正在查询")
    if info:
        info += "\ntelegram bot: @WooMaiBot"
        info += "\n----\n"
    else:
        info = ""

#    if len(cmd) == 1:
#  elif len(cmd) == 2:
#    elif cmd[1] == "down":
    info += "{}".format(await send_cmd_to_bash("."+" ".join(cmd)))
    await cmd_answer(info, event)


cmd = __name__.split(".")[-1]

need = need & ~CMD.is_admin

CMD.add(_, cmd=cmd, need=need, forbid=forbid)


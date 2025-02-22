#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

from . import *

logger = logging.getLogger(__name__)

from ..utils.telegram import my_popen, text2link, get_info_from_bot



async def _(event):
    logger.info("cmd {}: {}: {}".format( __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    msg = event.message
    chat_id = event.chat_id

    cmd = await get_cmd(event)
    if len(cmd) == 1:
        info = await get_info_from_bot("/"+" ".join(cmd), uid=573173175, key="使用方式")
    else:
#        info = await get_info_from_bot("/"+" ".join(cmd), uid=573173175, key="域名")
        info = await get_info_from_bot("/"+" ".join(cmd), uid=573173175, skip="正在请求中")
    if info:
        info += "\ntelegram bot: @WooMaiBot"
#        info += "\n----\n"
    else:
        info = ""
    await cmd_answer(info, event)

#    if len(cmd) == 1:
#  elif len(cmd) == 2:
#    elif cmd[1] == "down":


cmd = __name__.split(".")[-1]
need = need & ~CMD.is_admin
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

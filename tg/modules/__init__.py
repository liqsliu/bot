# for modules

from .. import *


#from ..config import cid_wtfipfs, cid_ipfsrss, cid_tw, cid_btrss, MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg

from ..telegram import tg_exceptions_handler as exceptions_handler
from ..telegram import CMD, cmd_answer, MSG_QUEUE, MAX_MSG_LEN, MAX_MSG_LINE, get_peer, get_chat_id, get_sender_id, get_sender, get_chat

get_cmd = CMD.get_cmd


need = CMD.is_text
need += CMD.is_me

forbid = CMD.is_bot
forbid += CMD.is_not_mentioned_in_group


from pathlib import Path
from ..utils.loader import get_modules

ALL_MODULES = get_modules(Path(__file__).parent)




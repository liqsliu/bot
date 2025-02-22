# for modules

from telethon.errors import *
from telethon.errors.rpcerrorlist import *
from telethon import events
from telethon.events import StopPropagation
from telethon.tl.types import PeerChat, PeerUser, PeerChannel, Chat, User, Channel, ChatFull, UserFull, ChannelFull, InputPeerUser, InputPeerChat, InputPeerChannel, MessageEntityTextUrl, MessageMediaUnsupported, MessageMediaWebPage

from ..bot import *
#from ..cmd import CMD

from ..utils.tools import SH_PATH
from ..utils.config import cid_wtfipfs, cid_ipfsrss, cid_tw, cid_btrss, MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg

from ..utils.telegram import tg_exceptions_handler, get_pattern, cmd_answer, MSG_QUEUE, MAX_MSG_LEN, MAX_MSG_LINE, get_peer


get_cmd = CMD.get_cmd


need = CMD.is_new
need += CMD.is_text
need += CMD.is_admin

forbid = CMD.is_bot
forbid += CMD.is_not_mentioned_in_group


""" Bot modules loader"""
from pathlib import Path
from ..utils.loader import get_modules

ALL_MODULES = get_modules(Path(__file__).parent)

# __all__ = ALL_MODULES + ["ALL_MODULES"]

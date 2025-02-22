from . import *
from ..telegram import is_private, is_forward, get_msg_link

logger = logging.getLogger(__name__)


from pyrogram.file_id import FileId


from pyrogram import enums




from ..telegram import MEDIAS
medias = MEDIAS.copy()
medias.remove(enums.MessageMediaType.STICKER)

async def get_dc(user, client, chat_id):
    if client.bot_token:
        return
    limit = 64
    ok = False
    #  async for msg in client.search_messages(chat_id, query=text, limit=limit, from_user=user.id):
    #  async for msg in client.search_messages(chat_id, limit=limit, from_user=user.id, filter="photo"):
    async for msg in client.search_messages(chat_id, limit=limit, from_user=user.id):
        if is_forward(client, msg):
            continue
        #  if msg.media == "sticker":
        if msg.media == enums.MessageMediaType.STICKER:
            continue
        #  if msg.media in ("photo", "video", "document"):
        if msg.media:
            if hasattr(getattr(msg, msg.media.value), "file_id"):
                ok = True
                break
        #  async for msg in client.search_messages(chat_id, limit=limit, from_user=user.id, filter="video"):
    #  for filter in ("photo", "video", "document", "photo_video", "animation"):
    #  for filter in ("photo", "document", "video", "audio", "voice", "animation"):
    for filter in medias:
        if not ok:
            async for msg in client.search_messages(chat_id, limit=limit, filter=filter):
                if is_forward(client, msg):
                    continue
                if get_sender_id(message) != user.id:
                    continue
                if msg.media:
                    if hasattr(getattr(msg, msg.media.value), "file_id"):
                        ok = True
                        break
    if ok:
        i = getattr(msg, msg.media.value).file_id
        dc_id = FileId.decode(i)
        dc_id = dc_id.dc_id
        #  return dc_id
        return f"{dc_id}, according to {await get_msg_link(msg)}"




async def _(client, message):
    "get telegram dc"
    sender = get_sender(message)
    if sender:
        if hasattr(sender, "dc_id") and sender.dc_id:
            info = "dc" + str(sender.dc_id)
        else:
            info = "no avatar"
            dc = await get_dc(sender, client, get_chat_id(message))
            if dc:
                info += "\nbut: dc" + str(dc)
    else:
        info = "error"
    if is_private(message):

        info += """

```
DC1
MIA, Miami FL, USA
149.154.175.53
2001:b28:f23d:f001::a
DC2
AMS, Amsterdam, NL
149.154.167.51
2001:67c:4e8:f002::a
DC3*
MIA, Miami FL, USA
149.154.175.100
2001:b28:f23d:f003::a
DC4
AMS, Amsterdam, NL
149.154.167.91
2001:67c:4e8:f004::a
DC5
SIN, Singapore, SG
91.108.56.130
2001:b28:f23f:f005::a
```
"""
        info += "\nhttps://core.telegram.org/getProxyConfig"
        info += "\nhttps://core.telegram.org/getProxyConfigV6"
        info += "\n"
        info += "\nhttps://docs.pyrogram.org/faq/what-are-the-ip-addresses-of-telegram-data-centers"

    await message.reply(info, parse_mode=enums.ParseMode.MARKDOWN)



need = need & ~CMD.is_me


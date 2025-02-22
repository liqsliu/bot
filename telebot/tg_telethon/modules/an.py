#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

from . import *

logger = logging.getLogger(__name__)

from ..utils.telegram import my_popen, text2link, get_info_from_bot

from ..utils.tools import url_re, pastebin, ipfs_add, save_to_telegraph

from telethon.tl.types import MessageEntityTextUrl

import savepagenow
from ..utils.tools import UA

async def get_iv_from_bot(url):
    # use @CorsaBot
    chat_id = 171977108
    info = "InstantViewBot: "
    url_s = url.split("?")[0].split("#")[0]

    async def fun(msg, url_s=url_s):
#        nonlocal url_s
        iv_url = None
        error = None

        if msg.entities:
            entities = msg.entities
            if len(entities) == 0:
                if msg.raw_text == "It looks like a file link":
                    return msg.raw_text
                return
            elif len(entities) == 1:
#                    if entities[0].url == url:
                if entities[0].url.startswith(url_s):
                    error = msg.raw_text
                return
            else:
                for e in entities:
                    if type(e) == MessageEntityTextUrl:
                        if e.url.startswith("https://telegra.ph/"):
                            return e.url
                return msg.raw_text
        else:
            error = msg.raw_text
            return
        return iv_url

    tmp = await get_info_from_bot(url, chat_id, skip="Waiting", fun=fun)
    if tmp:
        return tmp
    else:
        return info+"unknown error"




async def _(event):
    "archive content to: ipfs/pb/tg/ia/is"
    logger.info("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    msg = event.message
    chat_id = event.chat_id

    cmd = await get_cmd(event)
    if event.is_reply:
        r = await event.get_reply_message()
        if r and r.raw_text:
            text = r.raw_text
            cmd.append(text)
#    if event.is_reply:
#        text = (await event.get_reply_message()).raw_text
#        cmd.append(text)
    if len(cmd) == 1:
        info = "an $url"
        info += "\nan ia $url"
        info += "\nan ipfs $text"
        info += "\nan text $text"
        info += "\nan pb $text"
        info += "\nan tg $text/$url"
        info += "\nan tg2 $url"
        info += "\n"
        info += "\nall $url"
        info += "\nhelp"
        info += "\n"
        info += "\n--"
        info += "\ntg Use telegra.ph"
        info += "\nia Use The Internet Archive"
        info += "\nis Use The Archive.is"
        info += "\nipfs save text to ipfs public gateway"
        info += "\npb fars.ee"
        info += "\n"
        info += "\n----"
        info += "\nhttps://telegra.ph/"
        info += "\ntelegram bot: @CorsaBot"
#        info += "\nhttps://archive.org/"
        info += "\nhttps://archive.org/web/web.php"
        info += "\nhttps://archive.is/"
        info += "\nhttps://www.outline.com/"
        info += "\nhttps://github.com/oduwsdl/archivenow"
        info += "\nhttps://github.com/palewire/savepagenow"
        await cmd_answer(info, event)


    elif cmd[1] == "text" or cmd[1] == "ipfs":
        if len(cmd) == 2:
            info = "save text to ipfs"
        else:
            link = await ipfs_add(" ".join(cmd[2:]))
            if link:
                await cmd_answer(link, event)
            else:
                await cmd_answer("E: error", event)

    elif cmd[1] == "pb":
        if len(cmd) == 2:
            info = "save text to pb"
        else:
            link = await pastebin(" ".join(cmd[2:]))
            if link:
                await cmd_answer(link, event)
            else:
                await cmd_answer("E: error", event)
    elif cmd[1] == "down":
        if event.is_reply:
            replied = await event.get_reply_message()
            if replied.media:
                link = await media2link(replied)
                if link:
                    pass
                    info = link[0]
                else:
                    link = await media2link(replied, pb=True)
                    if not link:
                        info = "E: error"
            else:
                info = "no media"
        else:
            if len(cmd) == 2:
                info = "reply the msg to download"
            else:
                url = cmd[2]
                info = "E: need fix"

        await cmd_answer(info, event)
    elif cmd[1] == "tg":
        text = " ".join(cmd[2:])
        link = await save_to_telegraph(text)
        if link:
            await cmd_answer(link, msg)
        else:
            await cmd_answer("fail", msg)
    elif cmd[1] == "tg2":
        text = cmd[2]
        url = url_re.search(text)
        if url:
            url = url.group()
            asyncio.create_task(cmd_answer(await get_iv_from_bot(url), msg=msg))
        else:
            await cmd_answer("tg2 for url only", msg)
    else:
        shell_cmd = None
        an_cmd = "cd ~/tmp/; archivenow"
        ex_cmd = " "
        text = " ".join(cmd[1:])
        if len(cmd) > 1:
            if cmd[1] == "ia" or cmd[1] == "is" or cmd[1] == "all":
                ex_cmd = f" --{cmd[1]} "
                text = " ".join(cmd[2:])
            if cmd[1] == "help":
                ex_cmd = f" --{cmd[1]} "
                text = None

        if text is not None:
            url = url_re.search(text)
            if url:
                url = url.group()
                shell_cmd = an_cmd + ex_cmd + url

        if shell_cmd is not None:
            if event.is_private:
                asyncio.create_task(cmd_answer(await get_iv_from_bot(url)), msg=msg)
            if len(cmd) == 2:
#                url, new = savepagenow.capture_or_cache(url, user_agent=UA)
                url, new = await asyncio.to_thread(savepagenow.capture_or_cache, url, UA)
                if new:
                    info = url
                else:
                    info = f"cache: {url}"
                await cmd_answer(info, msg)
            else:
                if client == UB and chat_id < 0:
                    await my_popen(shell_cmd, msg=msg)
                else:
                    await my_popen(shell_cmd, max_time=300, msg=msg)
        elif cmd[1] == "help":
            shell_cmd = an_cmd + ex_cmd
            await my_popen(shell_cmd, msg=msg)
        else:
            await cmd_answer("E: no url", msg)
            if chat_id == MY_ID:
                shell_cmd = an_cmd + ex_cmd + event.raw_text.split(" ", 1)[1]
                await my_popen(shell_cmd, msg=msg)



need = need & ~CMD.is_admin
cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)




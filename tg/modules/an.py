#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_popen, text2link, get_info_from_bot, is_reply, is_private

from ..utils.tools import url_re, pastebin, ipfs_add, save_to_telegraph

#from telethon.tl.types import MessageEntityTextUrl

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
                if msg.text == "It looks like a file link":
                    return msg.text.markdown
                return
            elif len(entities) == 1:
#                    if entities[0].url == url:
                if entities[0].url.startswith(url_s):
                    error = msg.text.markdown
                return
            else:
                for e in entities:
                    #  if type(e) == MessageEntityTextUrl:
                    #  if e.type == "text_link":
                    if e.type == enums.MessageEntityType.TEXT_LINK:
                        if e.url.startswith("https://telegra.ph/"):
                            return e.url
                return msg.text.markdown
        else:
            error = msg.text.markdown
            return
        return iv_url

    tmp = await get_info_from_bot(url, chat_id, skip="Waiting", fun=fun)
    if tmp:
        return tmp
    else:
        return info+"unknown error"




async def _(client, message):
    "archive content to: ipfs/pb/tg/ia/is"
    msg = message
    chat_id = get_chat_id(msg)

    cmd = await get_cmd(client, message)
    if is_reply(msg):
        r = message.reply_to_message
        if r and r.text:
            text = r.text
            cmd.append(text)
    if len(cmd) == 1:
        info = "用法："
        info += "\nan $url"
        info += "\nan ia $url: use archivenow"
        info += "\nan all $url"
        info += "\nan help"
        info += "\nan tg $text/$url"
        info += "\nan tg2 $url"
        info += "\nan ipfs|text $text"
        info += "\nan pb $text"
        info += "\n"
        info += "\n--"
        info += "\n参数含义"
        info += "\nia Use The Internet Archive"
        info += "\nipfs save text to ipfs public gateway"
        info += "\ntg Use telegra.ph"
        info += "\npb fars.ee"
        info += "\n--"
        info += "\n默认 an 命令会调用 https://github.com/palewire/savepagenow"
        info += "\nan ia 会调用 https://github.com/oduwsdl/archivenow"
        info += "\n前者快，后者稳"
        info += "\n--"
        info += "\nhttps://telegra.ph/"
        info += "\ntelegram bot: @CorsaBot"
#        info += "\nhttps://archive.org/"
        info += "\nhttps://web.archive.org/save"
        info += "\nhttps://archive.today/"
        info += "\nhttps://www.outline.com/"
        await cmd_answer(info, client, message)


    elif cmd[1] == "text" or cmd[1] == "ipfs":
        if len(cmd) == 2:
            info = "save text to ipfs"
        else:
            link = await ipfs_add(" ".join(cmd[2:]))
            if link:
                await cmd_answer(link, client, message)
            else:
                await cmd_answer("E: error", client, message)

    elif cmd[1] == "pb":
        if len(cmd) == 2:
            info = "save text to pb"
        else:
            link = await pastebin(" ".join(cmd[2:]))
            if link:
                await cmd_answer(link, client, message)
            else:
                await cmd_answer("E: error", client, message)
    elif cmd[1] == "down":
        if message.is_reply:
            replied = message.reply_to_message
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

        await cmd_answer(info, client, message)
    elif cmd[1] == "tg":
        text = " ".join(cmd[2:])
        link = await save_to_telegraph(text)
        if link:
            await cmd_answer(link, client, msg)
        else:
            await cmd_answer("fail", client, msg)
    elif cmd[1] == "tg2":
        text = cmd[2]
        url = url_re.search(text)
        if url:
            url = url.group()
            asyncio.create_task(cmd_answer(await get_iv_from_bot(url), client, msg=msg))
        else:
            await cmd_answer("tg2 for url only", client, msg)
    else:
        shell_cmd = None
        an_cmd = "cd ~/tmp/; archivenow"
        ex_cmd = " "
        text = " ".join(cmd[1:])
        if cmd[1] == "ia" or cmd[1] == "is" or cmd[1] == "all":
            ex_cmd = f" --{cmd[1]} "
            text = " ".join(cmd[2:])
        elif cmd[1] == "help":
            ex_cmd = f" --{cmd[1]} "
            text = None

        if text is not None:
            url = url_re.search(text)
            if url:
                url = url.group()
                if "#" in url:
                    url = url.split("#")[0]
                logger.warning(url)
                #  if '"' not in text and "'" not in text:
                tmp = f"'{url}'"
                shell_cmd = an_cmd + ex_cmd + tmp

        if shell_cmd is not None:
            if is_private(client, message):
                asyncio.create_task(cmd_answer(await get_iv_from_bot(url), client, msg=msg))
            if len(cmd) == 2:
#                url, new = savepagenow.capture_or_cache(url, user_agent=UA)
                try:
                    url, new = await asyncio.to_thread(savepagenow.capture_or_cache, url, UA)
                    if new:
                        info = url
                    else:
                        info = f"cache: {url}"
                except savepagenow.exceptions.WaybackRuntimeError as e:
                    info = f"{e=}"
            else:
                #  res = await my_popen(shell_cmd, max_time=300, client=client, msg=msg)
                info = await my_popen(shell_cmd, max_time=60)
        elif cmd[1] == "help":
            shell_cmd = an_cmd + ex_cmd
            #  await my_popen(shell_cmd, client=client, msg=msg)
            info = await my_popen(shell_cmd)
        else:
            #  await cmd_answer("E: no url", client=client, msg=msg)
            info = "E: no url"
            if chat_id == MY_ID:
                shell_cmd = an_cmd + ex_cmd + message.text.split(" ", 1)[1]
                await my_popen(shell_cmd, client=client, msg=msg)
        await cmd_answer(info, client, msg)



need = need & ~CMD.is_me

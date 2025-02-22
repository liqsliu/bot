#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info


from ..utils.tools import http, pastebin, ipfs_add

from ..utils.text2img import text2img

import io
from PIL import Image, ImageDraw, ImageFont
from ..utils.dwt import embed_DWT, extract_DWT




async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    if event.chat_id == MY_ID:
        pass


    client = event.client
    cmd = await get_cmd(event)
    if len(cmd) == 1:
        info = "wm [de] url url"
        info += "\nwm en|add url url"
        info += "\nwm wm text"
        await cmd_answer(info, event)
    elif cmd[1] == "get" or cmd[1] == "wm":
        # get wm pic
        file = io.BytesIO()
        text = cmd[2]
#        img = text2img(text, fill=1, width=1, fontsize=30)
        img = await asyncio.to_thread(text2img, text, 1, 1, 30)
        img.save(file, format="png")
        img=file.getvalue()
        file.close()
#        await event.client.upload_file(file)
#        await event.reply(file=file)
        link = await pastebin(img)
        await event.reply(link)
    elif cmd[1] == "en" or cmd[1] == "add":
        # add mark
        img = await http(cmd[2])
        wm = await http(cmd[3])
#        Image.frombytes("RGB", len(wm), wm)
        file_wm = io.BytesIO()
        file = io.BytesIO()
        out = io.BytesIO()
        try:
            file_wm.write(wm)
            file_wm.seek(0)
            file.write(img)
            file.seek(0)
            pic = Image.open(file)
            mark = Image.open(file_wm)
#            pic_marked = embed_DWT(pic, mark)
            pic_marked = await asyncio.to_thread(embed_DWT, pic, mark)
            pic_marked.save(out, format="png")
            img = out.getvalue()
            link = await pastebin(img)
            await event.reply(link)
        finally:
            file_wm.close()
            file.close()
            out.close()


    elif cmd[1] == "de":

#        ext_mark = extract_DWT(pic_marked, Image.open('temp/DWT_mark.png'))
        img = await http(cmd[2])
        wm = await http(cmd[3])
#        Image.frombytes("RGB", len(wm), wm)
        file_wm = io.BytesIO()
        file = io.BytesIO()
        out = io.BytesIO()
        try:
            file_wm.write(wm)
            file_wm.seek(0)
            file.write(img)
            file.seek(0)
            pic = Image.open(file)
            mark = Image.open(file_wm)
            pic_marked = await asyncio.to_thread(extract_DWT, pic, mark)
            pic_marked.save(out, format="png")
            img = out.getvalue()
            link = await pastebin(img)
            await event.reply(link)
        finally:
            file_wm.close()
            file.close()
            out.close()



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)

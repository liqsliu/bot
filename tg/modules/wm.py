from . import *

logger = logging.getLogger(__name__)


from ..utils.tools import http, pastebin, ipfs_add

from ..utils.text2img import text2img

import io
from PIL import Image, ImageDraw, ImageFont
from ..utils.dwt import embed_DWT, extract_DWT


async def _(client, message):
    "water mark"
    cmd = await get_cmd(client, message)
    if len(cmd) == 1:
        info = "wm [de] url url"
        info += "\nwm en|add url url"
        info += "\nwm wm text"
        await cmd_answer(info, client, message)
    elif cmd[1] == "get" or cmd[1] == "wm":
        # get wm pic
        file = io.BytesIO()
        text = cmd[2]
#        img = text2img(text, fill=1, width=1, fontsize=30)
        img = await asyncio.to_thread(text2img, text, 1, 1, 30)
        img.save(file, format="png")
        img=file.getvalue()
        file.close()
        link = await pastebin(img)
        await message.reply(link)
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
            await message.reply(link)
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
            await message.reply(link)
        finally:
            file_wm.close()
            file.close()
            out.close()


from . import *

logger = logging.getLogger(__name__)

from ..utils.tools import get_from_url, url_only_re, ipfs_add, pastebin, http, save_to_telegraph, rgb_re, url_re, catbox, my_jaccard, chr_list
from ..telegram import set_bot_cmd, get_chat_id, download_media, download_in_bash, get_name_for_mt, get_msg, media2link, is_reply, get_msg_link, get_msg_from_url, is_me

from ..config import cid_disk, SH_PATH, cid_wtfipfs
from ..utils import db
from time import time

from urllib.parse import urlsplit, unquote




cmd="""
select * from note
where tag is not "test" or tag is null
;"""

import aiofiles
path = SH_PATH + "/group_note.txt"

async def import_txt():
    #  from ..utils.tools import file_read
    #  s = await file_read(path)
    print(await list_tag())
    import os
    os.remove(path)
    path2 = PARENT_DIR / "group_note.txt"
    async with aiofiles.open(path2, "r") as file:
        async for line in file:
            tag = line.split(" ", 1)[0][1:]
            name = line.split(" ", 1)[1].split(": ",1)[0].rstrip("".join(chr_list))
            text = line.split(" ", 1)[1].split(": ",1)[1]
            text = text.replace("\\n", "\n")
            text = text.replace("\\\"", "\"")
            text = text.replace("\\\\", "\\")
            print(await save(text, name, tag))
    print(await list_tag())
    await NB.send_message(MY_ID, "ok")
    return


async def add_txt(line):
    tag = line["tag"]
    user = line["user"]
    text = line["text"]




async def note(text, tag=None, user=None, id=None, note_type=0, ps=None, date=None):
    if not id:
        msg = f"#{tag} {user}: {text}"
        if len(msg) > 4096:
            return "error: text is too long"
        r  = db.search(None, None, table="note")
        if r:
            id = r[0]["id"]-1
        else:
            id = 20000
        if id < 1:
            res = await NB.send_message(cid_disk, msg)
            id = res.id
    if tag is None:
        pass
    elif tag == "default":
        tag = None
    elif tag.startswith("#"):
        tag.lstrip("#")
    if date is None:
        date = int(time())
    v = {
        "id": id,
        "tag": tag,
        "user": user,
        "date": date,
        "type": note_type,
        "ps": ps,
        "text": text
        }
    if db.save(v, "note") == 0:
        info = "existed"
    else:
        #  await add_txt(v)
        if tag != "test":
            if tag is None:
                tag = "default"
            text = text.replace("\\","\\\\")
            text = text.replace("\"","\\\"")
            text = text.replace("\n","\\n")
            msg = f"#{tag} {user}: {text}\n"
            async with aiofiles.open(path, "a") as file:
                await file.write(msg)
        info = f"saved"
    res = db.get(id, "note")
    info += await pp(res, True)
    return info



async def send(url, caption, mode=1):
    info = ""
    try:
        note_type = mode
        ps = None
        res = None
        document = None
        client = UB
        if mode == 1:
            info += f"\nupload via url: "
            #  print(repr(url))
            #  https://core.telegram.org/bots/api#sending-files
            if url.endswith(".pdf"):
                document = url
            elif url.endswith(".gif"):
                document = url
            elif url.endswith(".zip"):
                document = url
            else:
                info += f"not supported.\nonly: pdf gif zip.\nbut let me try\n"
                document = url
        elif mode == 2:
            info += f"\nupload via catbox: "
            document = await catbox(url)
            if not document:
                info += f"catbot is not avilable"
        elif mode == 3:
            info += f"\nupload via local: "
            r, res, err = await download_in_bash(url, "200000000")
            if r == 0:
                document = res.strip()
            else:
                info += f"\nfail to download {url}: {res}\nE: {err}"
                ps = -1
        elif mode == 4:
            info += f"\nupload via bot api: "
            client = NB
            r, res, err = await download_in_bash(url, "200000000")
            if r == 0:
                document = res.strip()
            else:
                info += f"\nfail to download {url}: {res}\nE: {err}"
                ps = -1
        elif mode == 4:
            ps = -1
            # need fix
            info += f"\nupload via mem: "
        else:
            ps = -1

        if document:
            res = await client.send_document(cid_disk, caption=caption, document=document, force_document=True)
            info += f"send {document} ok"
            ps = url
            #  info = f"saved to {res.link}"
            #  text = text.replace(url, "")
        else:
            pass
            #  info += await note(text, tag, user, note_type=6)

    except Exception as e:
        info += f"fail to send {document}: {e=}"
        logger.error(info)
    info += "\n"
    return ps, info, res


#  async def check_add(text=None, tag="default", user=None, ps=None):
async def check(text=None, tag="default", ps=None):

    info = ""
    if text:

        if tag == "default":
            _tag = None
        else:
            _tag = tag
        #  if db.existed("note", text=text):
            #  res = db.get({"text":text}, "note")
            #  if text == res["text"] and _tag == res["tag"]:
            #      pass
            #  else:
            #      #  info += await note(text, tag, user, note_type=res["type"], ps=res["id"])
            #      return
        target = None
        #  if tag == "faq":
        #      res = await faq_get(text, return_res=True)
        #      if res:
        #          print(res)
        #          target = res[0]
        c = db.run("""select * from note
            where tag is ? and text like ?
        ;""", (_tag, f"%{text}%",))
        res = []
        for i in c:
            res.append(dict(i))
        print(res)
        for i in res:
            if i["text"].split("\n--\n")[0] == text:
                target = i
                break

        if target:
            res = target
            info = "existed\n"
        else:
            return
    elif ps and db.existed("note", ps=ps):
        info = "existed url\n"
        res = db.get({"ps":ps}, "note")
    else:
        return
    if res:
        info += await pp(res, True, True)
        if res["type"] is None:
            info += "\n"
            info += "\n"
            info += await rec(text)
    else:
        info = "\nfixme"
    return info


async def save_tg(text, user, tag, msg=None):
    tmp = url_re.search(text)
    url = tmp.group("url")


    info = ""
    if not msg:
        msg = await get_msg_from_url(url, UB)
    if not msg:
        info += "can't get the msg"
        return info
    if msg.media:
        if msg.media in ["audio","document","photo","sticker","video","animation","voice","video_note"]:
            file = getattr(msg, msg.media)
            size = file.file_size
            saved = await msg.copy(cid_disk)
            mode = 512
            ps = url
            #  if text == url:
            text += f"\n--\nfile: {file.file_name}\ntype: {file.mime_type}\nsize: {file.file_size//1024}KB"
            if msg.caption:
                text += f"\n--\n{msg.caption}"
            info += await note(text, tag, user, saved.id, note_type=mode, ps=ps)
        else:
            info += "E: need fix"
    elif msg.text:
        #  text = text.replace(url, "") + f"\n--\n{msg.text}"
        if text != url:
            text = msg.text + f"\n--\nps:" + text.replace(url, "")
        else:
            text = msg.text
        res = await check(text, tag=tag)
        if res:
            info += res
        else:
            if "https://t.me/" not in text:
                info += await save(text, user, tag)
            else:
                info += await note(text, tag, user)
    else:
        info += "E: empty content"
    return info



async def save(url, user, tag, msg=None):

    url = url.strip()
    text = url

    info = ""
    logger.warning(repr(text))
    res = await check(text, tag=tag)
    if res:
        return res
    logger.warning("not existed")

    if not text:
        logger.error("empty text")
        return "empty text"
    if tag is None:
        #  tag = "default"
        pass
    else:
        if " " in tag:
            return "can't contain sapce"
        elif " " in tag:
            return "can't contain ."
        if len(tag) > 64:
            return "tag is too long"
    #  if url_only_re.match(url):
    tmp = url_re.search(url)
    if tmp:
        url = tmp.group("url")
        #  if db.existed("note", text=text, ps=url):
        #      return "existed"
    else:
        return await note(text, tag, user)

    res = await check(ps=url)
    if res:
        info += res+"\n\n"
        res = db.get({"ps":url}, "note")
        info += await note(text, tag, user, note_type=res["type"], ps=res["id"])
        return info

    elif url.startswith("https://t.me/"):
        return await save_tg(text, user, tag, msg)

    else:

        info = f"save file and text\n\n====\nurl: {url}\n"
        #  info +="\n==\n"
        #  caption = "#test"
        #  caption = None
        caption = f"#{tag}"
        mode = 1
        while True:
            ps, res, msg = await send(url, caption, mode=mode)
            info += res
            info +="==\n"
            if ps is None:
                mode += 1
            elif ps == -1:
                ps = None
                break
            else:
                break

        info +="\n\n===="
    info += "\nsave text:"
    if ps:
        if ps.isnumeric():
            info += await note(text, tag, user, ps=ps)
        else:
            info += await note(text, tag, user, msg.id, note_type=mode, ps=ps)
    else:
        info += await note(text, tag, user, note_type=mode)
    return info



async def list_tag():
    cmd = """select tag,count(id) from note group by tag order by tag"""
    c = db.run(cmd)
    if not c:
        info = "db error"
        logger.error(info)
    else:
        info = "tag num\n=="
        for i in c:
            i = dict(i)
            if i["tag"] is None:
                i["tag"] = "default"
            info += "\n#{} {}".format(i["tag"], i["count(id)"])
            #  info.append(dict(i))
        #  info = list(x["tag"] if x["tag"] is not None else "default" for x in info)
        #  info = "\n".join(list(f"#{x}" for x in info))
    return info



#  async def search(*args, q=None, **kwargs):
async def search(value=None, /, *, q=None, qq=None, need=0.5, more=3,  **kwargs):
    tmp = []
    while True:
        #  res = db.search(*args, **kwargs, table="note")
        res = db.search(value, **kwargs, table="note")
        if not res:
            break
        for i in res.copy():
            if i["type"] is None:
                #  res.pop(i)
                res.remove(i)
            elif q is not None:
                #  if q in i["text"] or q in unquote(i["text"]):
                if q.lower() in i["text"].lower() or q.lower() in unquote(i["text"]).lower():
                    pass
                else:
                    res.remove(i)
            elif qq is not None:
                if my_jaccard(qq, i["text"], check_sub=True, need=need):
                    pass
                else:
                    res.remove(i)
            if i["tag"] == None:
                i["tag"] = "default"

        tmp += res
        if more:
            pass
        else:
            break
        if "limit" in kwargs:
            if len(tmp) >= kwargs["limit"]:
                break
        #  if not res:
        if len(tmp) < more:
            if "limit" not in kwargs:
                kwargs["limit"] = 64
            if "offset" not in kwargs:
                kwargs["offset"] = 0
            kwargs["offset"] += kwargs["limit"]
        else:
            break
    if tmp:
        res = tmp
        return res
    return tmp



async def list(tag=None, user=None, *, mode=None, **kwargs):
    if tag is not None:
        info = f"#{tag}\n=="
    else:
        info = ""
    if tag is None:
        res = await search(user, key="user", **kwargs)
    else:
        if tag == "default":
            tag = None
        key = "tag"
        q = None
        #  if mode:
        #      q = tag
        #      key = None
        #      tag = None

        if user:
            res = await search(tag, key=key, ex={"user":user}, q=q, **kwargs)
        else:
            res = await search(tag, key=key, q=q, **kwargs)

    if user is None:
        info += await pp(res, mode=mode)
    else:
        if info:
            info += await pp(res, mode=mode)
        else:
            info += await pp(res, True, mode=mode)
    return info




async def pp(res, print_tag=False, print_id=False, mode="note"):
    info = ""
    if res:
        if isinstance(res, dict):
            res = [res]
        for i in res:
            info += "\n"
            if i["type"] is None:
                if print_tag:
                    pass
                elif print_id:
                    pasw
                else:
                    continue
            tag = i["tag"]
            if tag is None:
                tag = "default"

            info += "\n"
            if i["type"] is None:
                info += f"[] "

            if print_tag:
                info += f"#{tag} "
            if print_id:
                info += f"{i['id']} "
            #  info += f"\n\n{i['id']}\n{i['user']}: {i['text']}"
            if i["ps"]:
                if i["ps"].isnumeric() and i["id"] != int(i["ps"]):
                    t = db.get(int(i["ps"]), "note")
                    url = t["ps"]
                else:
                    url = i["ps"]

                if mode == "book":
                    pass
                else:
                    info += f"{i['user']}: {i['text']}\n"
                    #  info += "\n--"
                if i["ps"].isnumeric():
                    info += f"®{i['ps']}\n"
                else:
                    info += f"®{i['id']}\n"
                #  info += "\n--\n"
                if url.startswith("https://t.me/"):
                    info += url
                elif url.startswith("https://"):
                    name = unquote(url.split("//")[-1])
                    if "/" in name:
                        name = name.split("/")[-1]
                        if "." in name:
                            if "=" in name:
                                name = name.split("=")[-1]
                            if name:
                                info += name
                else:
                    info += url
                if mode == "book":
                    if i["text"].replace(url, "").strip():

                        #  info += "\n--\n"
                        info += "\n"+i["text"].replace(url, "").strip()
            else:
                if mode == "book":
                    info += i["text"].strip()
                else:
                    info += f"{i['user']}: {i['text']}"
            #  info += "\n==\n"
        return info
    else:
        return ""



async def delete(id=None, text=None, user=None):
    info = ""
    pass
    if id:
        res = db.get(id, "note")
    else:
        res = db.get({"text":text, "user":user}, "note")

    if res and res["type"] is not None:
        if id and user is not None:
            info += "\nothers's? use delete"
            return
        info += "delete: " + await pp(res, True)
        #  res = db.delete(res["id"], key="id", table="note")

        # note_type: None => deleted
        #  res["type"] = None
        res.pop("type")
        res["note_type"] = None
        await note(**res)

        info += "\nok"
    else:
        info += "not found"
    return info



async def rec(text):
    if db.existed("note", text=text):
        info = "existed"
        #  res = db.get(id, "note")
        #  res = await search(text, key="text")
        res = db.get({"text":text}, "note")
        if res:
            #  res = res[0]
            if res["type"] is None:
                res.pop("type")
                info = "recovery...\n"
                info += await note(**res)
            else:
                info += "\nneed't recovery"

    else:
        info = "not found"
    return info



from ..telegram import faq_get


async def _(client, message):
    "note"
    chat_id = get_chat_id(message)
    info = ""
    cmd = await get_cmd(client, message)

    msg_r = None
    if is_reply(message):
        msg_r = message.reply_to_message
        link = await get_msg_link(msg_r)
        cmd.append(link)

    #  text = message.text
    text = " ".join(cmd[2:])
    #  tag = None
    if cmd[0] == "book":
        tag = "book"
        mode = tag
    else:
        tag = "default"
        mode = "note"
    limit = 64
    offset = 0
    more = 3
    name = await get_name_for_mt(message)

    if cmd[0] == 'faq':
        if len(cmd) == 1 or cmd[1] == "help":
            info = "自定义问答"
            info += "\n添加示例: .faq ping|pong"
            info += "\n使用(触发): ping"
            info += "\n"
            info += "\n其他操作请使用.note命令"
            info += "\nadd: .note #faq ping|pong"
            info += "\nlist: .note #faq"
            info += "\ndel: .note #faq del ping|pong"
            info += "\nhelp: .note help"
        elif cmd[1] == "add":
            tag = "faq"
            text = " ".join(cmd[2:])
            info = await save(text, name, tag, msg_r)
        else:
            text = " ".join(cmd[1:])
            if '|' in text:
                q = text.split('|', 1)[0]
                a = text.split('|', 1)[1]
                if q and a:
                    tag = "faq"
                    info = await save(text, name, tag, msg_r)
                else:
                    info = "格式有误"
            else:
                info = await faq_get(text)
        await cmd_answer(info, client, message)
        return

    elif len(cmd) == 1 or cmd[1] == "help":
        if mode == "book":
            info = "group disk"
        else:
            info = "group note"
        info += f"\n.{mode} [cmd] url/text"
        info += "\n=="
        info += f"\n查看: .{mode} [list|li] [-][0-9] #test"
        info += f"\n添加: .{mode} [add] [#test] text"
        info += f"\n关键词搜索: .{mode} search|se text"
        info += f"\n模糊搜索(s越多，结果越准确，但可能没结果): .{mode} sss... text"
        info += f"\n查看自己创建的记录: .{mode} my [#test]"
        info += f"\n删除自己的记录: .{mode} del id/text"
        info += f"\n删除记录: .{mode} delete id/(username: text)"
        info += f"\n撤回删除: .{mode} rec text"
        info += f"\n下载文件: .{mode} down|dd... id/url"
        info += "\n=="
        info += "\n®代表特殊的id：该id指向的是一个带文件的记录，下载文件时可以使用该id"
        info += "\n警告：删除不是真的删除，只是隐藏了。原因就是为了保护上面的下载id不会失效"
        info += "\n=="
        info += "\n备份： https://github.com/liqsliu/toxbot/blob/master/group_note.txt"

    elif cmd[1] == "add":
        if cmd[2].startswith("#"):
            tag = cmd[2].strip("#")
            text = " ".join(cmd[3:])
        info = await save(text, name, tag, msg_r)
    elif cmd[1] == "del":
        # delete mine
        if cmd[2].isnumeric():
            #  info = "E: need use delete"
            info += await delete(int(cmd[2]), user=name)
        else:
            info += await delete(text=text, user=name)


    elif cmd[1] == "delete":
        # delete others
        if cmd[2].isnumeric():
            info += await delete(int(cmd[2]))
        else:
            name = text.split(": ", 1)[0]
            text = text.split(": ", 1)[1]
            info += await delete(text=text, user=name)
    elif cmd[1] == "delf":
        # delete force, only for me
        if is_me(client, message):
            if cmd[2].isnumeric():
                #  res = db.get(int(cmd[2]), "note")
                #  res = db.get({"id": int(cmd[2])}, "note")
                info = db.delete(int(cmd[2]), table="note")
            else:
                info = db.delete(text, key='text', table="note")
    elif cmd[1].startswith("#"):
        tag = cmd[1].strip("#")
        if len(cmd) == 2:
            info = await list(tag, mode=mode)
        else:
            info = await save(text, name, tag, msg_r)
    #  elif cmd[1] == "search" or cmd[1] == "se" or cmd[1] == "ss":
    elif cmd[1] == "search" or cmd[1] == "se" or cmd[1].replace("s", "") == "":

        if len(cmd) > 2 and cmd[2].startswith("#"):
            tag = cmd[2].strip("#")
            #  cmd.remove(f"#{tag}")
            cmd.pop(2)
            key = "tag"
        else:
            tag = None
            key = None

        if len(cmd) == 2:
            info = "search|se [#tag] text"
        elif len(cmd) == 3:
            q = cmd[2].strip()
        elif cmd[2].isnumeric():
            limit = int(cmd[2])
            q = cmd[3:].strip()
        elif cmd[2].startswith("-"):
            offset = (int(cmd[2][1:])-1) * limit
            q = cmd[3:].strip()
        else:
            q = " ".join(cmd[2:])

        if not info and q:
            #  if cmd[1] == "ss":
            if not cmd[1].startswith("se"):
                # ssss... 模糊搜索
                # qq
                need = 0.1*len(cmd[1])
                if need > 1:
                    need = 1
                #  if tag:
                #      res = await search(tag, key="tag", qq=q, limit=limit, offset=offset, need=need)
                #  else:
                #      res = await search(None, key=None, qq=q, limit=limit, offset=offset, need=need)
                res = await search(tag, key=key, qq=q, limit=limit, offset=offset, need=need)
            else:
                res = await search(tag, key=key, q=q, limit=limit, offset=offset)
            info += await pp(res, True, print_id=True)
    elif cmd[1] == "list" or cmd[1] == "li":
        if len(cmd) == 2:
            pass
        elif len(cmd) == 3:
            tag = cmd[2].strip("#")
        elif cmd[2].isnumeric():
            #  limit = int(cmd[2])
            more = int(cmd[2])
            tag = cmd[3].strip("#")
        elif cmd[2].startswith("-"):
            offset = (int(cmd[2][1:])-1) * limit
            tag = cmd[3].strip("#")
        else:
            tag = cmd[2].strip("#")
        if offset < 0:
            offset = 0
        info = await list(tag, limit=limit, offset=offset, mode=mode, more=more)
    elif cmd[1] == "tag":
        info = await list_tag()
    elif cmd[1] == "my":
        if len(cmd) == 2:
            pass
        elif len(cmd) == 3:
            tag = cmd[2].strip("#")
        elif cmd[2].isnumeric():
            #  limit = int(cmd[2])
            more = int(cmd[2])
            tag = cmd[3].strip("#")
        elif cmd[2].startswith("-"):
            offset = (int(cmd[2][1:])-1) * limit
            tag = cmd[3].strip("#")
        else:
            tag = cmd[2].strip("#")
        if offset < 0:
            offset = 0
        #  info = await list(tag, name)
        #  info = await list(tag, name, limit=limit, offset=offset)
        info = await list(tag, name, limit=limit, offset=offset, mode=mode, more=more)
    elif cmd[1] == "import":
        if get_chat_id(message) == MY_ID:
            await import_txt()
        else:
            info += "need admin"
    elif cmd[1] == "check":
        if get_chat_id(message) == MY_ID:
            limit = limit*10
            while True:
                res = await search(None, key=None, offset=offset, limit=limit, more=False)
                if res:
                    for i in res:
                        if i["ps"]:
                            continue
                        if url_re.search(i["text"]):
                            url = url_re.search(i["text"]).group("url")
                            info += f"\nfind: {url}"
                            t = db.get({"ps":url}, "note")
                            if t and t["ps"] == url:
                                i["ps"] = str(t["id"])
                                i.pop("type")
                                i["note_type"] = t["type"]
                                info += await note(**i)
                                info += f"\nadded id: {i['ps']}"
                            else:
                                info += "\nskiped"

                    offset += limit
                else:
                    break
        else:
            info += "need admin"
    elif cmd[1] == "rec":
        info = await rec(text)
    elif cmd[1] == "down" or cmd[1] == "noup" or cmd[1].replace("d", "") == "":
        mid = None
        if len(cmd) == 2:
            info += "need a id or url"
            info += f"\n.{mode} down id/url"
            info += f"\njust download: .{mode} noup id/url"
            info += f"\nipfs: .{mode} d id/url"
            info += f"\nfars.ee: .{mode} dd id/url"
            info += f"\n0x0.st: .{mode} ddd id/url"
            info += "\ntransfer"
            info += "\nlitterbox"
            info += "\nfile_io"
            info += "\n..."
        elif cmd[2].isnumeric():
            mid = int(cmd[2])
            res = db.get(mid, "note")
            if res:
                url = res["ps"]
                info += f"\n原始链接: {url}"
            else:
                info += "\n没找到"
        else:
            url = cmd[2]
            res = db.get({"ps":url}, "note")
            if res:
                mid = res["id"]

            else:
                info += "\n没找到。建议先搜索，然后根据文件id下载"
        if mid:
            msg = await get_msg(cid_disk, mid, UB)
            if msg:
                #  await msg.forward(chat_id)
                await msg.copy(chat_id)
                #  info = await media2link(client, msg)
                if cmd[1] == "down":
                    link = await media2link(UB, msg, all=True, max_file_size=2000000000)
                elif cmd[1] == "noup":
                    link = await media2link(UB, msg, ex="just", max_file_size=2000000000)
                elif cmd[1] == "d":
                    link = await media2link(UB, msg, max_file_size=2000000000)
                else:
                    link = await media2link(UB, msg, ex=cmd[1], max_file_size=2000000000)
                if link:
                    info += "\n文件名: " + link[1]
                    info += "\n\n下载链接(每个链接指向的内容相同): "
                    link = link[0]
                    for i in link.split(" "):
                        info += f"\n\n{i}"
                else:
                    info += "\nfail to downlaod from telegram, need fix"
            else:
                info += "\nmsg not found, need fix"
    else:
        #  url = cmd[1]
        text = " ".join(cmd[1:])
        info = await save(text, name, tag)
    await cmd_answer(info, client, message)



need = need ^ CMD.is_me
need = need | CMD.is_my_group


CMD.add(_, "book", need, forbid)

CMD.add(_, "faq", need, forbid)


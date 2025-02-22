import logging
import asyncio




from telethon import events
from telethon import utils
from telethon.events import StopPropagation
from telethon.tl.types import PeerChannel, User

from .utils.config import cid_wtfipfs, cid_ipfsrss, cid_tw, TG_BOT_ID_FOR_MT
from .utils.tools import my_exceptions_handler as decorator
from .utils.tools import file_read
from .bot import *


logger = logging.getLogger(__name__)
mp = logger.warning


class Cmd(object):
    def __init__(self):
        self.cmds = {None: []}
        self.check = {}
        self.check_score = {}

    def add_check(self, fun):
        if fun in self.check.values():
            logger.error(f"check existed: {fun.__name__}")
            raise ValueError(f"check existed: {fun.__name__}")
            return
#        bit = 2**len(self.check)
        bit = 1 << len(self.check)
        if bit in self.check:
            logger.error(f"fail to add check: {fun.__name__}")
            raise ValueError(f"fail to add, bit existed, need fix: {bit=} in {self.check=}")
        if hasattr(self, fun.__name__):
            raise ValueError(f"fail to add, name existed, need fix: {bit=} in {self.check=}")
        exec(f"self.{fun.__name__} = bit")
#        self.check[bit] = fun
        self.check[bit] = decorator(fun)
        self.check_score[bit] = [0]*4

    def get_bit(self, need):
        bit = 0
        if need:
            for n in need:
                if not n:
                    raise ValueError(f"empty str in need: {cmd=}")
                    return
                tmp = bit
                for b in self.check:
                    if self.check[b].__name__ == n:
                        bit += b
                        break
                if tmp == bit:
                    raise ValueError(f"need is not found, need fix: {cmd=}")
                    return
        return bit


    def add(self, fun, cmd=None, need=None, forbid=None, *args, **kwargs):
        if cmd and cmd in self.cmds:
            raise ValueError(f"fail to add cmd: {cmd=} in {self.cmds=}")
            return
        k = []
        if cmd is None:
            self.cmds[cmd].append(k)
        else:
            self.cmds[cmd] = k
        k.append(decorator(fun))
#        k.append(self.get_bit(need))
        k.append(need)
        k.append(forbid)
        if k[1] & k[2] > 0:
            raise ValueError(f"need & forbid >0, need fix: {cmd=}")
            return
        if fun.__doc__ is not None:
            k.append(fun.__doc__.strip())

    async def get_cmd(self, event):
        " event to cmd, ignore some group msg"

#        if is_group(event) and not is_mentioned(event):
#            if is_admin(event) and is_out(event):
#                pass
#            else:
#                return
        cmd = []
        if not is_text(event):
            return
        client = event.client
        text = event.raw_text
#            if event.chat_id == cid_wtfipfs and ": " in text:
        if ": " in text:
            if event.sender_id:
                sender_id = event.sender_id
            else:
                logger.error("no sender_id, may ignore cmd")


                sender = await event.get_sender()
                sender_id = utils.get_peer_id(sender)
            if sender_id == 420415423 or sender_id == UB2_ID or sender_id == BOT_ID:
                text = text.split(": ", 1)[1]
        if text.strip() == "":
            return
        cmd = text.split(' ')
        if cmd[0].strip() == "":
            return
        if "\n" in cmd[0]:
            cmd = cmd[0].split('\n', 1) + cmd[1:]
            #      del cmd[2]
            # cmd.pop(2)
        if cmd[0].strip() == "":
            return
        key = cmd[0][0]
        if client == NB:
            if is_my_group(event):
                return
            if is_group(event):
#                    if cmd[0].endswith("@{}".format(BOT_NAME)):
                if "@" in cmd[0]:
                    cmd[0] = cmd[0].split("@", 1)[0]
            if key == "/":
                cmd[0] = cmd[0][1:]
        elif is_out(event):
            if key == "/" and "@" not in cmd[0]:
                cmd[0] = cmd[0][1:]
            elif key == ".":
                cmd[0] = cmd[0][1:]
            elif key == "$":
                cmd[0] = cmd[0][1:]
            elif key == "'":
                cmd[0] = cmd[0][1:]
            elif key == "_":
                cmd[0] = cmd[0][1:]
            else:
                return
        elif is_my_group(event):
            logger.warning(f"get a cmd in my group: {cmd=}")
            if key == ".":
                cmd[0] = cmd[0][1:]
            else:
                return

#        return cmd
        if cmd and cmd[0] and cmd[0] in self.cmds:
            return cmd
        else:
            return None

    async def _run(self, event, fun):
        if asyncio.iscoroutinefunction(fun):
            return await fun(event)
        else:
            return fun(event)

    def score(self, k, i):
        b = 1
        while True:
            if b & k != 0:
                self.check_score[b][i] += 1
            elif b > k:
                break

            b = b << 1

    def _check(self, b, event):
        self.score(b, 1)
        s = self.check[b](event)
        if s is True:
#            self.score(b, 2)
            return True
        else:
#            self.score(b, 3)
            return False

    def _checks(self, k, event):
        v = 0
        b = 1
        while True:
            if b & k != 0:
                s = self._check(b, event)
                if s is True:
                    v = v | b

            else:
                if b > k:
                    break
                self.score(b, 0)
            b = b << 1
        return v

    def _is_ok(self, i, v):
        "check v is ok"
        if (i[1] | i[2]) & v == i[1]:
            self.score((i[1] | i[2]) & (~(v ^ i[1])), 2)
            return True
        else:
            self.score((i[1] | i[2]) & (v ^ i[1]), 3)
        return False

    def _is_ok(self, n, f, v):
        "check n f is ok"
        if (n | f) & v == n:
            self.score((n | f) & ~(v ^ n), 2)
            return True
        else:
            self.score((n | f) & (v ^ n), 3)
        return False

    async def _check_and_run(self, event):
        "check all, one time"
        funs = self.cmds[None].copy()
        cmd = await self.get_cmd(event)
        if cmd:
            cmd = cmd[0]
            funs.append(self.cmds[cmd])
            cmd = True
        else:
            cmd = False
        k = 0
        for i in funs:
            k = k | i[1] | i[2]
#        v = self._checks(k, event)
        b = 1
        while True:
            if b & k != 0:
                if self._check(b, event) is True:
                    v = b
                else:
                    v = 0
                k = 0
                for i in funs.copy():
                    n = b & i[1]
                    f = b & i[2]
                    if n | f != 0 and self._is_ok(n, f, v) is not True:
                        if cmd and funs[-1] == i:
                            cmd = False
                        funs.remove(i)
                    else:
                        k = k | i[1] | i[2]
            elif b > k:
                break
            else:
                self.score(b, 0)
            b = b << 1

        if len(funs) == 0:
            return False
#        if is_admin(event) and event.client == NB:
#            i = funs[-1]
#            logger.warning(f"check: {i[0].__name__}\ncheck result k n f v:\n{bin(k)}\n{bin(i[1])}\n{bin(i[2])}\n{bin(v)}\nok: {(i[1] | i[2]) & v == i[1]}\nlog False: {(i[1] | i[2]) & (v ^ i[1])}\nlog True: {(i[1] | i[2]) & (~(v ^ i[1]))}")
#        logger.info(f"result: {bin(v)}")

        b = 1
        for i in funs:
#            if self._is_ok(i[1], i[2], v):
            await self._run(event, i[0])
        return cmd

    async def check_cmd(self, event, run=False, cmd=None):
        "check whether the event will start a cmd, warning: not check init"
#        if is_out(event) and is_my_group(event):
#            return False
        if cmd is None:
            cmd = await self.get_cmd(event)
            if cmd:
                cmd = cmd[0]
                logger.warning(f"check {cmd=}")
            else:
                return False
        i = self.cmds[cmd]
        v = self._checks(i[1] | i[2], event)
#            if self._is_ok(i, v):
        if self._is_ok(i[1], i[2], v):
#            logger.warning(f"will run: {cmd=}")
            if run:
                await self._run(event, i[0])
            return True
        return False

    async def run(self, event):
        try:
            return await self._check_and_run(event)
        except events.StopPropagation as e:
            return
            from .utils.tools import get_traceback
            info = get_traceback(e)
            if event.raw_text == "ping":
                print(info)
                logger.warning("stop event")
            return False

    async def print_cmd(self):
        "just for me"
        info = f"None: {len(self.cmds[None])}"
        for c in self.cmds:
            if c is None:
                o = self.cmds[c]
                for k in o:
                    info += f"\n{k[1]}-{k[2]}={k[0].__name__}"
                    if len(k) > 3:
                        info += f": {k[3]}"
                info += "\n"
                continue
            k = self.cmds[c]
            info += f"\n{c}: {k[1]}-{k[2]}={k[0].__name__}"
            if len(k) > 3:
                info += f": {k[3]}"
        info += "\n"
        info += "\n"
        for c in self.check:
            info += f"\n{c}: {self.check[c].__name__}"

        info += "\n\n: skip check ok bad"
        info += "\n"
#        import json
#        info += json.dumps(self.check_score,indent=2)
        info += "\n".join(f"{self.check[x].__name__}: {self.check_score[x]}" for x in self.check if x in self.check_score)
        if len(info.encode()) > 4096:
            info = info[:2048]
        return info

    async def list_cmd(self, event):
        "for others"
        if is_admin(event):
            name = "my master"
        else:
            if hasattr(event.sender, "first_name"):
                name = event.sender.first_name
            else:
                name = event.sender_id
        info = None
        if event.raw_text.endswith("help"):
            if is_my_group(event):
                info = await file_read(PARENT_DIR / "group_help.txt", "r")
                info += "\n"
            else:
                info = ""
            info += f"cmds for: {name}"
            for i in self.cmds:
                if i is None:
                    continue
                if is_admin(event):
                    info += f"\n{i}:"
                elif await self.check_cmd(event, cmd=i):
                    info += f"\n{i}:"
                else:
                    continue
                if len(self.cmds[i]) > 3:
                    info += f" {self.cmds[i][3]}"
            if is_my_group(event):
                info += "\n"
                info += "\ncmd menu 2(old):"
                info += "\n"
                info += await file_read(PARENT_DIR / "group_cmd.txt", "r")
        elif event.raw_text.endswith("help xmpp"):
            if is_my_group(event):
                info = await file_read(PARENT_DIR / "group_help_xmpp.txt", "r")
        elif event.raw_text.endswith("help tox"):
            if is_my_group(event):
                info = await file_read(PARENT_DIR / "group_help_tox.txt", "r")
        else:
            info = "E: need fix"
        return info

CMD = Cmd()




def is_text(event):
    "has text for cmd"
#    if event.raw_text is not None:
    if event.raw_text.strip() != "":
        # default ""
        return True
    return False
CMD.add_check(is_text)

def is_bot(event):
    if hasattr(event, "via_bot_id"):
        if event.via_bot_id is not None:
            return True
    if event.is_private is True and event.chat is not None:
        if event.chat.bot is True:
            return True
    elif event.sender is not None and type(event.sender) == User:
        if event.sender.bot is True:
            return True
    return False

CMD.add_check(is_bot)


def is_not_mentioned_in_group(event):
    "for cmd"
    if is_group(event):
        if is_out(event):
            return False
        elif is_my_group(event) and is_UB(event):
            return False
        elif not is_mentioned(event):
            return True
    return False
CMD.add_check(is_not_mentioned_in_group)

def is_my_group(event):
    if event.chat_id == cid_wtfipfs:
        return True
    return False
CMD.add_check(is_my_group)


def is_admin(event):
    if event.sender_id == MY_ID:
        return True
    return False
CMD.add_check(is_admin)

def is_UB(event):
    if event.client == UB:
        return True
    return False
CMD.add_check(is_UB)

def is_all(event):
    if is_new(event):
        if not is_grouped(event):
            return True
    elif is_edit(event):
        if not is_grouped(event):
            return True
    elif is_album(event):
        return True
    else:
        pass
#        return True
    return False
CMD.add_check(is_all)

def is_NB(event):
    if event.client == NB:
        return True
    return False
CMD.add_check(is_NB)

def is_UB2(event):
    if event.client == UB2:
        return True
    return False
CMD.add_check(is_UB2)

def is_edit(event):
    if type(event) == events.messageedited.MessageEdited.Event:
        return True
    return False
CMD.add_check(is_edit)

def is_channel(event):
    if event.is_channel is True and event.chat.broadcast is True:
        return True
    return False
CMD.add_check(is_channel)



def is_album(event):
    if type(event) == events.album.Album.Event:
        return True
    return False
CMD.add_check(is_album)



def is_out(event):
    "is out"
    if hasattr(event, "out"):
        if event.out is True:
            return True
        else:
            return False
    else:
        pass
#        from .utils.telegram import put
#        put(str(type(event)))
#        put(str(event))
    if hasattr(event, "message"):
        msg = event.message
        if hasattr(msg, "out"):
            if msg.out is True:
                return True
            else:
                return False
    if event.is_private is True:
        if event.chat_id != event.sender_id:
            return True
    elif is_group(event):
        if event.client == UB:
            if event.sender_id == MY_ID:
                return True
        elif event.client == UB2:
            if event.sender_id == UB2_ID:
                return True
    return False
CMD.add_check(is_out)



def is_new(event):
    if type(event) == events.newmessage.NewMessage.Event:
        return True
    return False
CMD.add_check(is_new)


def is_grouped(event):
    if event.grouped_id is not None:
        return True
    return False
CMD.add_check(is_grouped)


def is_anon_msg(event):
    if event.sender_id is not None and event.sender_id < 0:
        return True
    elif type(event.sender) == PeerChannel:
        return True
    elif hasattr(event, "from_id") and type(event.from_id) == PeerChannel:
        return True
    return False

CMD.add_check(is_anon_msg)




def is_private(event):
    "need private"
    if event.is_private is True:
        return True
    return False

CMD.add_check(is_private)

def is_group(event):
    "need group"
    if event.is_group and not is_channel(event):
        return True
    return False

CMD.add_check(is_group)



def is_mentioned(event):
    if hasattr(event, "mentioned"):
        if event.mentioned is True:
            return True
    return False

CMD.add_check(is_mentioned)

def is_reply(event):
    "is reply"
    if event.is_reply is True:
        return True
    return False

CMD.add_check(is_reply)


def is_forward(event):
    "is forward"
    if event.forward is not None:
        return True
    return False

CMD.add_check(is_forward)



@NB.on(events.NewMessage)
@NB.on(events.MessageEdited)
@NB.on(events.Album)
@UB.on(events.NewMessage)
@UB.on(events.MessageEdited)
@UB.on(events.Album)
@UB2.on(events.NewMessage)
@UB2.on(events.MessageEdited)
@UB2.on(events.MessageEdited)
async def _(event):
    if await CMD.run(event) is True:
        raise StopPropagation



if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))

    def fun():
        pass

    CMD.add_check(is_admin)

    CMD.add("test", fun, need=["is_admin"])
    CMD.add("test error need", fun, need=["is_adminhhh"])

    print(cmds)
    print(check)
    #print(dir(flag))

    #print(flag.need_admin)


else:
    print('{} 运行'.format(__file__))



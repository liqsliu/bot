import logging

logger = logging.getLogger(__name__)
mp = logging.error


class A():
    a = 5

    def __init__(self):
        self.a = 1

    def f(self, a=None):
        if not a:
            a = self.a
        print("f")
        print(a)

    @staticmethod
    def f_waibu():
        print("in ok")

    @staticmethod
    def f_nei():
        print("in ok")

    def ff(self):
        f_waibu()
        f_nei()
        print("ff")



def f_waibu():
    mp(locals())
    mp(globals())
    mp(test_a)

    print(locals())

    print(globals())


from . import *

from pyrogram import Client, filters


# @NB.on_message(filters.command("ping"))
# async def echo(client, message):
    # await message.reply("pong")


# @UB.on_message(filters.text & filters.private)
# @NB.on_message(filters.private)
# @NB.on_message()
# @NB.on_message(filters.all)
# async def echo(client, message):
    # # if message.from_user.id == MY_ID:
    # # if message.chat.id == MY_ID:
    # if message.from_user and message.from_user.id == MY_ID:
        # await message.reply(str(message))
    # if message.text == MY_NAME:
        # await message.reply(str(message))


async def run():
    from .utils import db
    db.init("mytask.db")
    from .config import load_config
    await load_config()
    global CMD
    from .cmd import CMD
    info = await CMD.print_cmd()
    await NB.send_message(MY_ID, info)
    # async def _(client, message):
        # "pong"
        # await message.reply("pong")

    # need = CMD.is_private
    # forbid = CMD.is_bot
    # cmd = "ping"
    # CMD.add(_, cmd=cmd, need=need, forbid=forbid)
    from . import mytask
    from . import ping
    return

    if "UB" in globals():
        await UB.send_message(MY_ID, "ptg is ok")
        from pyrogram import idle
        await idle()
        return

        await LOOP.run_until_disconnected()
        await UB.run_until_disconnected()
        return
        await LOOP.run_forever()
    return

    import asyncio
    await asyncio.sleep(8)
    return
    from .telegram import put
    put("test put")
    return

    info = await my_popen("echo popen ok", shell=True)

    print(info)

    #  info, err =await my_popen("ok error", shell=True, return_err=True)
    info = await my_popen("ok error", shell=True, combine=False)
    print(info)
    print(repr(info))

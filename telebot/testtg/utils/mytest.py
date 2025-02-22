import logging

logger = logging.getLogger(__name__)
mp = logging.error

#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

#logger.error("config: {}".format(CONFIG))
#CONFIG.append("test")
#logger.error("config: {}".format(CONFIG))


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


test_a = 1
#mp(locals())
#mp(globals())
mp(test_a)


def f_waibu():
    mp(locals())
    mp(globals())
    mp(test_a)

    print(locals())

    print(globals())


from ..bot import *

async def fun(event):
    print(event.raw_text)
    if event.raw_text == "ping":
        await event.reply("pong")


from ..cmd import CMD

need = CMD.is_NB+CMD.is_new
need += CMD.is_private
forbid = CMD.is_out
CMD.add(fun, need=need, forbid=forbid)




async def run():
    if "UB" in globals():
        await UB.run_until_disconnected()
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

#!/usr/bin/python3

import sys
import logging
import asyncio

from . import LOGGER, OUT, ERR, debug, UB, NB, MY_ID, BOT_ID, UB2, WORK_DIR, PARENT_DIR


logger = logging.getLogger(__name__)

LOOP = asyncio.get_event_loop()


if LOOP.is_closed():
    LOGGER.error("loop closed, this may be a error")


async def mytest():
    from .utils import mytest
    await mytest.run()

    print("test finished")
    return


from .utils.config import CONFIG, save_config


async def run():

    if "UB" in globals():
        #  me = client.get_me()
        me = await UB.get_me()
        print(me.id)
        global MY_NAME
        # if me.username:
        MY_NAME = me.username

    # https://docs.telethon.dev/en/latest/concepts/updates.html
#    if NB != UB:
    if "NB" in globals():
        global BOT_NAME
        bot = await NB.get_me()
        print(bot.id)
        BOT_NAME = bot.username

    if "UB2" in globals():
        global UB2_ID
        bot = await UB2.get_me()
        print(bot.id)
        UB2_ID = bot.id

    global CMD
    from .cmd import CMD

    # default 1
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            pass
            print("argv: ", end="")
            print(sys.argv)
            await mytest()
            return True

    # import os
    # if os.path.isfile("mytask.py"):
    if MY_NAME == "liqsliu":
        from .utils import db
        db.init("mytask.db")
        from .utils.config import load_config
        await load_config()
        from . import mytask
        from .utils.loader import load_modules
        from .modules import ALL_MODULES
        load_modules(ALL_MODULES, __package__)
        await mytask.ok()
    else:
        async def _(event):
            "pong"
            cmd = "ping"
            mp("cmd {}: {}: {}".format(cmd, event.sender_id, event.raw_text))
            await event.reply("pong")

        need = CMD.is_private
        forbid = CMD.is_bot
        CMD.add(_, cmd=cmd, need=need, forbid=forbid)

    logger.warning("init ok, loop...")
    if "UB" in globals():
        await UB.run_until_disconnected()
    elif "UB2" in globals():
        await UB2.run_until_disconnected()
    elif "NB" in globals():
        await NB.run_until_disconnected()

    return True
    await UB.disconnected


def main():
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warn")
    logger.error("test err")

    #  with UB:
    #    UB.loop.run_until_complete(run())
    #    loop.run_until_complete(run())
    try:
        with UB:
            try:
                if "UB2" in globals():
                    with UB2:
                        LOOP.run_until_complete(run())
                else:
                    LOOP.run_until_complete(run())
            except KeyboardInterrupt:
                if MY_NAME == "liqsliu":
                    logger.warning("save config...")
                    LOOP.run_until_complete(save_config())
                    logger.info("save config ok")
                    from .utils.tools import session
                    if session:
                        LOOP.run_until_complete(session.close())
                        logger.info("session closed")
                    from .utils import db
                    if db.conn:
                        db.cur.close()
                        db.conn.close()
                raise
            except Exception as e:
                # logger.exception("error: stop...")
                logger.warning("error: stop...", exc_info=True, stack_info=True)
                raise
    except KeyboardInterrupt:
        logger.warn("exit")
    except Exception as e:
        logger.error("wtf", exc_info=True)
    return
    LOOP.run_until_complete(LOOP.shutdown_asyncgens())
    logger.warn("main loop finished")
    LOOP.stop()
    logger.warn("loop close...")
    LOOP.close()
    if LOOP.is_closed():
        logger.warn("loop closed, exit....")
    else:
        logger.warn("loop is not closed, ???")
    return









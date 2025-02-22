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
        if me.username:
            MY_NAME = me.username
        else:
            MY_NAME = "liqsliu"

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

    # default 1
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            pass
            print("argv: ", end="")
            print(sys.argv)
            await mytest()
            return True

    global CMD
    from .cmd import CMD
    t = await UB.get_entity(MY_ID)
    m = await UB.send_message(MY_ID, "test")

    # from .utils.config import load_config
    # await load_config()
    # from . import mytask

    # from .utils.loader import load_modules
    # from .modules import ALL_MODULES
    # load_modules(ALL_MODULES, __package__)

    # await mytask.ok()

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
                logger.warning("save config...")
                LOOP.run_until_complete(save_config())
                logger.info("save config ok")
                from .utils.tools import session
                if session:
                    LOOP.run_until_complete(session.close())
                    logger.info("session closed")
                raise
            except:
                # logger.exception("error: stop...")
                logger.warning("error: stop...", exc_info=True, stack_info=True)
                raise
    except KeyboardInterrupt:
        logger.warn("exit")
    except:
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









#!/usr/bin/python
# -*- coding: UTF-8 -*-
from . import *  # noqa: F403


logger = logging.getLogger(__name__)



async def run():
    #fuck telegram

    from . import _init
    await _init()

    from .utils import db
    db.init(WORK_DIR / "mytask.db")
    from .config import load_config
    await load_config()

    # import os
    # if os.path.isfile("mytask.py"):
    from . import mytask

    from . import modules
    from .utils.loader import load_modules
    load_modules(modules.ALL_MODULES, __package__)
    from .telegram import CMD
    for m in modules.ALL_MODULES:
        # if hasattr(getattr(modules, m), "handler"):
        if hasattr(getattr(modules, m), "_"):
            handler = getattr(modules, m)._
        elif hasattr(getattr(modules, m), "handler"):
            handler = getattr(modules, m).handler
        else:
            continue
        need = getattr(modules, m).need
        forbid = getattr(modules, m).forbid
        CMD.add(handler, cmd=m, need=need, forbid=forbid)


    logger.warning("init ok, loop...")
    from pyrogram import idle
    if "idle" in locals():
        await idle()


#  async def run():
#      from importlib import import_module
#      from pathlib import Path
#      #  import_module(f"{directory}.modules.{module_name}")
#      directory = Path(__file__).parents
#      logger.warning(f"{directory=}")
#      module_name = "push_twitter_to_tg"
#      return
#      import_module(f"{directory}.modules.{module_name}")
#      while true:
#          pass
#          await asyncio.sleep(5)
#          logger.warning("ok")
        

def main():
    try:
        # with UB:
        LOOP.run_until_complete(run())
    except KeyboardInterrupt as e:
        raise
    except SystemExit as e:
        raise
    except Exception as e:
        # logger.exception("error: stop...")
        # logger.warning("error: stop...", exc_info=True, stack_info=True)
        logger.error("wtf", exc_info=True)
        raise
    finally:
        if "NB" in globals():
            NB.stop()
        if "NB2" in globals():
            NB2.stop()
        if "UB2" in globals():
            UB2.stop()
        if "UB" in globals():
            UB.stop()
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





if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warn")
    logger.error("test err")
    main()
else:
    print('{} 运行'.format(__file__))

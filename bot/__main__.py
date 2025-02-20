#!/usr/bin/python
# -*- coding: UTF-8 -*-
from . import *  # noqa: F403
#  import sys
#  import asyncio
#  loop = asyncio.get_event_loop()

#  async def _init():

#loop.run_until_complete(init())
#  if loop.is_running():
#    LOGGER.error("loop running...")
#  else:
#    LOGGER.error("loop stoped...")
#
#  if loop.is_closed():
#    LOGGER.error("loop closed, this may be a error")

logger = logging.getLogger(__name__)

if __name__ == '__main__':
  print('{} 作为主程序运行'.format(__file__))
  logger.debug("test debug")
  logger.info("test info")
  logger.warning("test warn")
  logger.error("test err")
  #  main()
  from . import m
  #  await bot.run()
  m.main()

elif __package__ == "":
  print('{} 运行, empty package'.format(__file__))
else:
  print('{} 运行, package: {}'.format(__file__, __package__))

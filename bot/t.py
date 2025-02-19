
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
logger = logging.getLogger(__name__)

from functools import wraps
import asyncio

def exceptions_handler(func):

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                return _exceptions_handler(e)

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
               return  _exceptions_handler(e)
    return wrapper



def _exceptions_handler(e, *args, **kwargs):
  try:
    res = f'{e=} line: {e.__traceback__.tb_next.tb_lineno}'
    raise e
  except KeyboardInterrupt:
    logger.info("W: 用户手动终止")
    raise
  except SystemExit as e:
    logger.warning(f"W: systemexit: {e=}")
    raise
  except RuntimeError as e:
    logger.warning(f"W: {e=} line: {e.__traceback__.tb_lineno}")
    raise
  except AttributeError as e:
    logger.warning(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    return f"{e=}"
  except Exception as e:
    print(res)
    print(f"W: {repr(e)} line: {e.__traceback__.tb_next.tb_next.tb_lineno}")
    logger.error(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    return f"{e=}"


def pprint(e):
  print('---')
  print("||%s: %s" % (type(e), e))
  print('---')
  for i in dir(e):
    print("  %s: %s: %s" % (i, type(getattr(e, i)), getattr(e, i)))
  print('===')



@exceptions_handler
def t():
  raise ValueError

import time

async def t():
  a = 1
  b=[0]
  def f():
    #  print(a)
    b[0] += 1
    print(b[0])
  f()
  await asyncio.sleep(3)
  a = time.time()
  f()

#  t()
#  t()
async def main():
  t1 = asyncio.create_task(t())
  t2 = asyncio.create_task(t())
  await t1
  await t2



def get_lineno(tb):
  lineno = "%s" % tb.f_lineno
  while tb.f_back is not None:
    lineno += " %s" % tb.f_back.f_lineno
    tb = tb.f_back
  return lineno


async def main():
  import sys
  tb = sys._getframe()
  lineno = get_lineno(tb)
  pprint(tb.f_code)
  print(lineno)

asyncio.run(main())
print(__file__)

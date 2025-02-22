#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .. import *  # noqa: F403


async def __test():
    from . import mytest
    await mytest.run()
    print("test finished")
    return


async def test():
    from .. import _init
    await _init()
    import sys
    # default 1
    if len(sys.argv) > 1:
        print("argv: ", end="")
        print(sys.argv)
        if sys.argv[1] == "test":
            pass
    await __test()
    print("test ok")



if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
elif __package__ != "":
    print('{} 运行 in package: {}'.format(__file__, __package__))
    asyncio.run(test())
else:
    print('{} 运行'.format(__file__))


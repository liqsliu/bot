



def f():

    print(id([]))
    print(id([]))
    print(id([]))
    print(id([]))


    print()

    print(id(1))
    print(id(1))
    print(id(1))
    print(id(1))

async def f2():

    print(id([]))
    print(id([]))
    print(id([]))
    print(id([]))


    print()

    print(id(1))
    print(id(1))
    print(id(1))
    print(id(1))

import asyncio

f()
asyncio.run(f2())



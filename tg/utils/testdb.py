import logging


# from .. import *

# from .tools import SH_PATH, tw_re, pic_re, url_only_re, my_host_re

import aiosqlite

logger = logging.getLogger(__name__)
mp = logger.warning

_path = "test.db"


async def init(path=_path):
    pass
    global conn, cur, db
    conn = await aiosqlite.connect(path)
    cur = await conn.cursor()
    db = cur


async def commit():
    await conn.commit()


async def close():
    await cur.close()
    await conn.close()


async def execute(sql, *args):
    return await cur.execute(sql, *args)


def _existed_table(name):
    c = cur.execute(f"""PRAGMA table_info({name});""")
    print(c.rowcount)
    if c.fetchone() != []:
        return True
    return False
    # print(c.fetchall())
    print(c.fetchone())
    print(c.arraysize)
    print(dir(c))


async def existed_table(name):
    c = await cur.execute(f"""PRAGMA table_info({name});""")
    print(c.rowcount)
    if await c.fetchone() != []:
        return True
    return False


async def _test():
    pass
    await init()
    await existed_table("users")
    # await execute("""insert into users (id, first_name) values(1, 'test');""")
    c = await execute("""select * from users""")
    print(await c.fetchall())
    await close()



def test():

    import asyncio
    asyncio.run(_test())
    return
    import sqlite3
    conn = sqlite3.connect(_path)
    cur = conn.cursor()
    db = cur

    print(existed_table("users"))
    print(existed_table("usejdnddnrs"))
    exit()
    existed_table("userS")
    existed_table("userdjdjdS")
    print(db.execute("""PRAGMA table_info(users);""").fetchall())
    print(db.execute("""PRAGMA table_info(userjdjdjdjs);""").fetchall())

    exit()
    p()

    db.execute("""insert into users (id, first_name) values(1, 'test');""")
    db.execute("""insert into users (id, first_name) values(2, 'test');""")
    conn.commit()

    p()


def p():
    c = db.execute("""select * from users""")
    print(c.fetchall())


def c():
    db.execute("""
            create table users
            (id int primary key not null,
            first_name text not null,
            last_name char(64),
            username char(32),
            raw blob,
            tag text
            );
    """)


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    test()

else:
    print('{} 运行'.format(__file__))

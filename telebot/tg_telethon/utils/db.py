import logging


# from .. import *

# from .tools import SH_PATH, tw_re, pic_re, url_only_re, my_host_re

# import aiosqlite
import asyncio
import sqlite3
import threading
_conns = threading.local()

logger = logging.getLogger(__name__)
mp = logger.warning

_path = "test.db"
conn = None


def init(path=_path):
    global conn, cur, db
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    db = cur
    # if not hasattr(_conns, 'lock'):
    _conns.lock = asyncio.Lock()
    table ="config"
    if not existed(table):
        create(table)
    table ="users"
    if not existed(table):
        create(table)
    table ="groups"
    if not existed(table):
        create(table)
    table ="channels"
    if not existed(table):
        create(table)
    table ="messages"
    if not existed(table):
        create(table)


def get_conn():
    global conn
    if conn is None:
        init()
    return conn


def commit():
    conn.commit()


def close():
    cur.close()
    conn.close()


def execute(sql, *args):
    # print(sql)
    # with tx() as cur:
    with conn:
        return cur.execute(sql, *args)


def get_column(table):
    # need fix
    tmp = []
    # tmp.append("id int primary key not null")
    if table == "users":
        tmp.append("""
            id integer primary key not null,
            first_name char(64),
            last_name char(64),
            username char(32),
            groups blob,
            ps text""")
    elif table == "groups":
        # type int default 0,
        tmp.append("""id integer not null,
            id2 integer primary key AUTOINCREMENT,
            title varchar(255),
            username char(32),
            ps text""")
    elif table == "channels":
        tmp.append("""id integer primary key not null,
            title varchar(255),
            username char(32),
            ps text""")
    elif table == "messages":
        tmp.append("""id integer not null,
            chat_id integer,
            sender_id integer,
            text varchar(4096),
            date int,
            ps text,
            primary key (chat_id, id)
            """)
    elif table == "rss":
        tmp.append("""id integer primary key AUTOINCREMENT not null,
            status int,
            url text not null,
            etag text,
            date text,
            update int,
            group int
            ps text""")
    else:
        # if table == "config":
        tmp.append("id integer primary key AUTOINCREMENT not null")
        tmp.append("text text")
    return tmp
    tmp = ["id integer primary key AUTOINCREMENT not null"]
    if type(table) == dict:
        for i in table:
            tmp.append("{i} text")






def create(table):
    column = get_column(table)
    # cur.execute(f"""create table {table}
    execute(f"""create table if not exists {table}
            ( {",".join(column)});""")
    # conn.commit()


def save(text, table="config", index=1):
    if text:
        pass
    else:
        logger.error(f"wtf: {text}")
        return
    if not existed(table):
        create(table)
    if type(text) == str or type(text) == int:
        # cur = execute(f"""select id from {table}
            # where id = {index}
        # """)
        # if cur.fetchone():
        if existed(table, index):
            cur = execute(f"""update {table}
                set text = ?
                where id = ?;
            """, (text, index))
        else:
            cur = execute(f"""insert into {table}
                (id, text) values (?,?);
            """, (index, text))
    elif type(text) == list:
        execute(f"""delete from {table};""")
        for i in range(len(text)):
            if type(text[i]) is str:
                save(text[i], table, i+1)
            elif type(text[i]) is int:
                save(text[i], table, i+1)
            else:
                logger.warning(f"may be wrong: {text[i]}\ntype: {type(text[i])}")
                # save(text[i], table, i+1)
                save(str(text[i]), table, i+1)
    elif type(text) == tuple:
        cs = columns(table)
        if len(cs) == len(text) + 1:
            cur = execute(f"""insert into {table}
                ({",".join(repr(x) for x in cs[1:])})
                values ({",".join(repr(x) for x in text)});
            """)
            return
        elif len(cs) == len(text):
            # cur = execute(f"""select * from {table}
                # where id = {text[0]};
            # """)
            # if cur.fetchone():
            if existed(table, text[0]):
                # cur = execute(f"""delete from {table}
                    # where {cs[0]} = {text[0]};
                # """)
                cur = execute("""update {}
                    set {}
                    where id = {};
                """.format(table, ",".join(f"{x}=?" for x in cs), text[0]), text)
            else:
                cur = execute(f"""insert into {table}
                    values ({",".join(repr(x) for x in text)});
                """)
        else:
            logger.error("need fix")
            raise ValueError(f"num is error: f{text} f{cs}")

    elif type(text) == dict:
        # cur = execute(f"""select * from {table}
            # where id = {text["id"]};
        # """)
        # if cur.fetchone():
        pid = {
                "id": text["id"]
                }
        if table == "messages":
            pid.update({"chat_id": text["chat_id"]})
        if existed(table, **pid):
            cur = execute("""update {}
                set {}
                where {};
            """.format(table, ",".join(f"{x}=?" for x in text.keys()), " and ".join(f"{x}=?" for x in pid.keys())), tuple(text.values())+tuple(pid.values()))
        else:
            cur = execute(f"""insert into {table}
                ({",".join(x for x in text.keys())})
                values ({",".join("?" for x in text.values())});
            """, tuple(text.values()))
    else:
        cs = columns(table)
        logger.error("need fix")
        raise ValueError(f"type is error: f{text} f{cs}")




def get(id, table="users"):
    c = execute(f"""select * from {table}
        where id={id};
    """)
    # for r in c:
        # print(r)
    r = c.fetchone()
    if r is not None:
        r = dict(r)
    return r

def search(text, key="text", offset=1, limit=5, table="messages"):
    # c = execute(f"""select id, chat_id, sender_id, text from {table}
    c = execute(f"""select * from {table}
        where {key} like ?
        order by date desc
        limit ?
        offset ?
    ;""", (f"%{text}%", limit, offset))
    # ;""", (repr(f"%{text}%"), limit, offset))
    info = []
    for i in c:
        info.append(dict(i))
    print(text)
    print(info)
    if info:
        return info



def pp(table="config"):
    c = db.execute(f"""select * from {table};""")
    cs = c.description
    print(list(i[0] for i in cs))
    for i in c:
        # print(tuple(i), end="")
        print(dict(i).values(), end="")
    print()


def columns(table):
    c = execute(f"""PRAGMA table_info({table});""")
    c = c.fetchall()
    return [x[1] for x in c]
    c = cur.execute(f"""select * from {table} limit 1;""")
    cs = c.description
    return list(i[0] for i in cs)


def existed(table, id=None, chat_id=None):
    if id is None:
        c = execute(f"""PRAGMA table_info({table});""")
        if c.fetchone():
            return True
        return False
    else:
        if chat_id is not None:
            c = execute(f"""select count(*) from {table} where id={id} and chat_id={chat_id} limit 1;""")
        else:
            c = execute(f"""select count(*) from {table} where id={id} limit 1;""")
        r = c.fetchone()
        n = tuple(r)[0]
        if n > 0:
            return True
        return False
        print(type(r))
        print(dict(r))
        print(tuple(r))



def cc():
            # (id int primary key not null,
    db.execute("""
            create table users
            (id integer primary key AUTOINCREMENT not null,
            first_name text not null,
            last_name char(64),
            username char(32),
            raw blob,
            tag text
            );
    """)




async def _test():
    init()
    save({"id":1, "first_name":"user", "groups": b"1"}, "users")
    pp("users")



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



class LocalTxContextManager:
    """
    Context manager that begins a transaction (with BEGIN IMMEDIATE, by default) and yields a cursor
    on entry, commits on normal exit, and rolls back on exit via exception.
    Internally this supports nesting via named savepoints with unique names on nested construction
    within a thread.
    Intended use is with a context to wrap code in a transaction (using the `tx` alias):
        with db.tx() as cur:
            ...
    Transactions are IMMEDIATE by default because SQLite's default DEFERRED transactions are a
    recipe for concurrency failure (see SQLITE_BUSY_SNAPSHOT description in
    https://www.sqlite.org/isolation.html).  If, however, you need transactional isolation for a
    read-only transaction (i.e. because you need multiple SELECTs that depend on a consistent
    snapshot of the data) then you can construct the transaction with the `read_only=True` kwarg to
    use a DEFERRED transaction.  (It is technically not read-only, but if you try to use
    modification on it you will probably end up crying at some future point).
    """

    def __init__(self, *, read_only=False):
        self.conn = get_conn()
        self.immediate = not read_only

    def __enter__(self):
        if not hasattr(_conns, 'sp_num'):
            _conns.sp_num = 0

        self.sp_num = _conns.sp_num + 1
        if self.sp_num == 1:
            self.conn.execute("BEGIN IMMEDIATE" if self.immediate else "BEGIN")
        else:
            self.conn.execute(f"SAVEPOINT sogs_sp_{self.sp_num}")

        cur = self.conn.cursor()

        # We do this down here so in case something above throws we won't leave it incremented.
        _conns.sp_num += 1

        return cur

    async def __aenter__(self):
        print("aenter ok")
        await _conns.lock.acquire()
        self.__enter__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        print("aexit ok")
        self.__exit__(exc_type, exc_value, traceback)
        _conns.lock.release()

    def __exit__(self, exc_type, exc_value, traceback):
        _conns.sp_num -= 1
        if exc_type is None:
            # This can throw, which we want to propagate
            if self.sp_num == 1:
                self.conn.execute("COMMIT")
            else:
                self.conn.execute(f"RELEASE SAVEPOINT sogs_sp_{self.sp_num}")
        else:
            # We're exiting the context by exception, so try to rollback but if this also fails then
            # we want the original exception to propagate, not this one.
            try:
                if self.sp_num == 1:
                    self.conn.execute("ROLLBACK")
                else:
                    self.conn.execute(f"ROLLBACK TO SAVEPOINT sogs_sp_{self.sp_num}")
            except Exception as e:
                logging.warn(f"Failed to rollback database transaction: {e}")


# Shorter alias for convenience
tx = LocalTxContextManager

if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    test()

else:
    print('{} 运行'.format(__file__))

import logging
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
    global conn, cur

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    close()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # if not hasattr(_conns, 'lock'):
    _conns.lock = asyncio.Lock()
    table ="config"
    if not existed(table):
        create(table)
    table ="user"
    if not existed(table):
        create(table)
    table ="chat"
    if not existed(table):
        create(table)
    table ="channel"
    if not existed(table):
        create(table)
    table ="message"
    if not existed(table):
        create(table)
    table ="note"
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


def run(sql, *args):
    #  if "like" in sql:
    #      print(sql)
    # with tx() as cur:
    with conn:
        return conn.execute(sql, *args)


def get_column(table):
    # need fix
    tmp = []
    # tmp.append("id int primary key not null")
    if table == "user":
        tmp.append("""
            id integer primary key not null,
            username char(32),
            first_name char(64),
            last_name char(64),
            groups blob,
            ps text""")
    elif table == "chat":
        # type int default 0,
        tmp.append("""id integer not null,
            id2 integer primary key AUTOINCREMENT,
            username char(32),
            title varchar(255),
            ps text""")
    elif table == "channel":
        tmp.append("""id integer primary key not null,
            username char(32),
            title varchar(255),
            ps text""")
    elif table == "message":
        tmp.append("""id integer not null,
            chat integer,
            sender integer,
            text varchar(4096),
            date int,
            reply_to_message_id int,
            ps text,
            primary key (chat, id)
            """)
    elif table == "note":
        tmp.append("""id integer primary key not null,
            tag varchar(64),
            text text not null,
            user text,
            date int,
            type int,
            ps text""")
    elif table == "rss":
        tmp.append("""id integer primary key AUTOINCREMENT not null,
            url text not null,
            status int,
            etag text,
            last text,
            update int,
            send blob,
            ps text""")
    elif table == "forwarder":
        tmp.append("""id integer primary key AUTOINCREMENT not null,
            send blob,
            ps text""")
    elif table == "data":
        tmp.append("""id integer primary key AUTOINCREMENT not null,
            data blob""")
    elif table == "config":
        tmp.append("id integer primary key AUTOINCREMENT not null")
        tmp.append("text text")
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
    run(f"""create table if not exists {table}
            ( {",".join(column)});""")
    # conn.commit()




def save(text, table="config", index=1):
    if text:
        pass
    else:
        logger.error(f"wtf: {text}")
        return
    cur = None
    if not existed(table):
        create(table)
    #  if type(text) == str or type(text) == int:
    if isinstance(text, str) or isinstance(text, int):
        # cur = run(f"""select id from {table}
            # where id = {index}
        # """)
        # if cur.fetchone():
        if existed(table, index):
            cur = run(f"""update {table}
                set text = ?
                where id is ?;
            """, (text, index))
        else:
            cur = run(f"""insert into {table}
                (id, text) values (?,?);
            """, (index, text))
    elif isinstance(text, list):
        #  run(f"""delete from {table};""")
        for i in range(len(text)):
            if type(text[i]) is str:
                save(text[i], table, i+1)
            elif type(text[i]) is int:
                save(text[i], table, i+1)
            else:
                logger.warning(f"may be wrong: {text[i]}\ntype: {type(text[i])}")
                # save(text[i], table, i+1)
                save(str(text[i]), table, i+1)
    elif isinstance(text, tuple):
        cs = columns(table)
        if len(cs) == len(text) + 1:
            cur = run(f"""insert into {table}
                ({",".join(repr(x) for x in cs[1:])})
                values ({",".join(repr(x) for x in text)});
            """)
        elif len(cs) == len(text):
            # cur = run(f"""select * from {table}
                # where id = {text[0]};
            # """)
            # if cur.fetchone():
            if existed(table, text[0]):
                # cur = run(f"""delete from {table}
                    # where {cs[0]} = {text[0]};
                # """)
                cur = run("""update {}
                    set {}
                    where id = {};
                """.format(table, ",".join(f"{x}=?" for x in cs), text[0]), text)
            else:
                cur = run(f"""insert into {table}
                    values ({",".join(repr(x) for x in text)});
                """)
        else:
            logger.error("need fix")
            raise ValueError(f"num is error: f{text} f{cs}")

    elif isinstance(text, dict):
        # cur = run(f"""select * from {table}
            # where id = {text["id"]};
        # """)
        # if cur.fetchone():
        pid = {
                "id": text["id"]
                }
        if table == "message":
            pid.update({"chat": text["chat"]})
        if existed(table, **pid):
            text.pop("id")
            if table == "message":
                text.pop("chat")
            cur = run("""select * from {}
                where {}
                limit 1
                ;
            """.format(table, " and ".join(f"{x} is ?" for x in pid.keys())), tuple(pid.values()))
            r = cur.fetchone()
            if r is not None:
                r = dict(r)
                same = True
                for i in r:
                    if i in text:
                        if text[i] != r[i]:
                            same = False
                            break
                if same:
                    logger.info(f"ignore same item: {text} == {i}")
                    return 0
            cur = run("""update {}
                set {}
                where {};
            """.format(table, ",".join(f"{x}=?" for x in text.keys()), " and ".join(f"{x} is ?" for x in pid.keys())), tuple(text.values())+tuple(pid.values()))
        else:
            cur = run(f"""insert into {table}
                ({",".join(x for x in text.keys())})
                values ({",".join("?" for x in text.values())});
            """, tuple(text.values()))
    else:
        cs = columns(table)
        logger.error("need fix")
        raise ValueError(f"type is error: f{text} f{cs}")
    if cur:
        return cur.lastrowid




def get(id, table="user"):
    #  c = run(f"""select * from {table}
    #      where id={id};
    #  """)
    if isinstance(id, int):
        id = {"id":id}
    c = run("""select * from {}
        where {}
        limit 1
        ;
    """.format(table, " and ".join(f"{x} is ?" for x in id.keys())), tuple(id.values()))
    # for r in c:
        # print(r)
    r = c.fetchone()
    if r is not None:
        r = dict(r)
    return r

def search(text, key="text", ex={}, offset=0, limit=5, table="message"):

    m = "="
    m = "is"
    if text is None:
        m = "is"
    elif isinstance(text, str):
        #  if len(text.split(" ")) > 1 and "only" in text:
        if text.startswith("like "):
            m = "like"
            text = text.split(" ", 1)[1]
        elif text.startswith("glob "):
            m = "glob"
            text = text.split(" ", 1)[1]
        else:
            m = "is"
            #  if len(text.split(" ")) > 1:
            #      if "like" in text:
            #          text = text.split(" ", 1)[1]
            #      elif "glob" in text:
            #          m = "glob"
            #          text = text.split(" ", 1)[1]
            #  if m == "glob":
            #      if "*" not in text:
            #          text = f"*{text}*"
            #  else:
            #      if "%" not in text:
            #          text = f"%{text}%"
        text = text.replace("'", "''")
        #  text = f"'{text}'"

    if table == "message":
        order = "order by date desc"
        #  exclude =[]
        #  exclude.append(684649913)
    elif table == "note":
        order = "order by id asc"
    else:
        order = "order by id"
    if ex:
        if key:
            ex[key] = text
        c = run("""select * from {}
            where {}
            {}
            limit ?
            offset ?
            """.format(table, " and ".join(f"{x} {m} ?" for x in ex.keys()), order), tuple(ex.values())+(limit, offset))
    elif text is None and key is None:
        c = run(f"""select * from {table}
            {order}
            limit ?
            offset ?
        ;""", (limit, offset))
    else:
        c = run(f"""select * from {table}
            where {key} {m} ?
            {order}
            limit ?
            offset ?
        ;""", (text, limit, offset))
    info = []
    for i in c:
        info.append(dict(i))
    print(info)
    if info:
        return info


def delete(text, key="id", table="message"):

    if text is None:
        m = "is"
    elif isinstance(text, str):
        m = "like"
        m = "="
    else:
        m = "="
    c = run(f"""delete from {table}
        where {key} {m} ?
    ;""", (text,))
    info = []
    for i in c:
        info.append(dict(i))
    print(info)
    if info:
        return info


def pp(table="config"):
    c = run(f"""select * from {table};""")
    cs = c.description
    print(list(i[0] for i in cs))
    for i in c:
        # print(tuple(i), end="")
        print(dict(i).values(), end="")
    print()


def columns(table):
    c = run(f"""PRAGMA table_info({table});""")
    c = c.fetchall()
    return [x[1] for x in c]
    c = cur.execute(f"""select * from {table} limit 1;""")
    cs = c.description
    return list(i[0] for i in cs)


def existed(table, id=None, **pid):
    if id is None:
        if not pid:
            c = run(f"""PRAGMA table_info({table});""")
            if c.fetchone():
                return True
            return False
    # c = run(f"""select count(*) from {table} where id={id} and chat={chat} limit 1;""")
    if id is not None:
        pid["id"] = id
    c = run("""select count(*) from {} where {} limit 1;""".format(table, " and ".join(f"{x} is ?" for x in pid.keys())), tuple(pid.values()))
    #  if pid:
    #      pid["id"] = id
    #  else:
    #      c = run(f"""select count(*) from {table} where id={id} limit 1;""")
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
    run("""
            create table user
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
    save({"id":1, "first_name":"user", "chat": b"1"}, "user")
    pp("user")



def test():

    import asyncio
    asyncio.run(_test())
    return
    import sqlite3
    conn = sqlite3.connect(_path)
    cur = conn.cursor()

    print(existed_table("user"))
    print(existed_table("usejdnddnrs"))
    exit()
    existed_table("userS")
    existed_table("userdjdjdS")
    print(cur.execute("""PRAGMA table_info(user);""").fetchall())
    print(cur.execute("""PRAGMA table_info(userjdjdjdjs);""").fetchall())

    exit()
    p()

    cur.execute("""insert into user (id, first_name) values(1, 'test');""")
    cur.execute("""insert into user (id, first_name) values(2, 'test');""")
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
            self.conn.execute(f"SAVEPOINT dbtx_sp_{self.sp_num}")

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
                self.conn.execute(f"RELEASE SAVEPOINT dbtx_sp_{self.sp_num}")
        else:
            # We're exiting the context by exception, so try to rollback but if this also fails then
            # we want the original exception to propagate, not this one.
            try:
                if self.sp_num == 1:
                    self.conn.execute("ROLLBACK")
                else:
                    self.conn.execute(f"ROLLBACK TO SAVEPOINT dbtx_sp_{self.sp_num}")
            except Exception as e:
                logging.warn(f"Failed to rollback database transaction: {e=}")


# Shorter alias for convenience
tx = LocalTxContextManager

if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    test()
else:
    print('{} 运行'.format(__file__))

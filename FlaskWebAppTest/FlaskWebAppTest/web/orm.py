import asyncio
import aiomysql
import logging

def log(sql,args=()):
    logging.info("SQL:%s" % sql)

async def crate_pool(**kw):
    logging.info("creat database connection pool...")
    global __pool
    __pool = await aiomysql.create_pool(host =kw.get("host","localhost"),
                                       port =kw.get("port",3306),
                                       user =kw["user"],
                                       password =kw["password"],
                                       db =kw["db"],
                                       charset =kw.get("charsetr","utf-8"),
                                       autocommit =kw.get("autocommit",True),
                                       maxsize=kw.get("maxsize",10),
                                       minsize=kw.get("minsize",1),
                                       loop=loop)

async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace("?","%s"),args or())
            if size:
                rs=await cur .fetchmany(size)
            else:
                rs=await cur .fetchall()
        logging.info("rows returned:%s"% len(rs))
        return rs;

async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace("?", "%s"), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

def create_args_string(num):
    L = []
    for n in range(num):
        L.append("?")
    return ", ".join(L)




class Field(object):
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)()
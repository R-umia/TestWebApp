import asyncio
import aiomysql

async def crate_pool(**kw):
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
    global __pool
    with (await __pool)as conn:
        cur=await conn.cursor(aiomysql.DictCursor)

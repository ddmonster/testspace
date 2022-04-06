from typing import Any
from fastapi import FastAPI
import aioredis
from aioredis import Redis
from testspace.utils.ContextVarsWapper import ContextWarpper
import weakref
class RedisWarpper():
    def __init__(self) -> None:
        self.init = False
        self.app:weakref.ReferenceType = None
    def __getattr__(self,__name:str):
        if not self.init:
            raise Exception("not init redis please register in app!!!")
        return getattr(self.app().state.redis,__name)
    
    async def init_from_url(self,url, app:FastAPI):
        app.state.redis  =  await aioredis.from_url(url)
        self.app = weakref.ref(app)
        self.init = True
        
redis:Redis = RedisWarpper()            
    
def register_redis(app:FastAPI):
    @app.on_event("startup")
    async def on_startup():
        await redis.init_from_url("redis://127.0.0.1",app)
    @app.on_event("shutdown")
    async def on_shutdown():
        await redis.close()
from typing import Optional, Union, cast
from fastapi import FastAPI
import aioredis
from aioredis import Redis
from testspace.utils.TypeWeakref import TypeWeakRef
from testspace.config import tomlconfig
from testspace.log import logger

__all__ = [
    'redis',
    "register_redis"
    ]
class RedisWarpper():
    def __init__(self) -> None:
        self.app:Optional[TypeWeakRef[FastAPI]] = None
        
    def __getattr__(self,__name:str):
        if not self.app:
            raise Exception("not setup  please register redis in app!!!")
        return getattr(cast(FastAPI,self.app.get()).state.redis,__name)
    
    async def init_from_url(self,url, app:FastAPI):
        app.state.redis  =  await aioredis.from_url(url)
        self.app = TypeWeakRef[FastAPI](app)
        
redis:Union[Redis,RedisWarpper] = RedisWarpper()            
    
def register_redis(app:FastAPI):
    
    @app.on_event("startup")
    async def on_startup():
        await redis.init_from_url(tomlconfig.database.REDIS_URL,app)
        logger.info(f"redis set up {tomlconfig.database.REDIS_URL}")
        
    @app.on_event("shutdown")
    async def on_shutdown():
        await redis.close()
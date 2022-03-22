from testspace.components.pubsub import endpoint
from fastapi import APIRouter, Path

router = APIRouter(tags=["websocket pub sub"])

@router.post("/{pub:path}")
async def publish(pub:str,data:str):
    rs = await endpoint.publish(pub,data)
    return rs

    
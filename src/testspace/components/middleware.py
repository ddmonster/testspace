
from testspace.log import logger
from fastapi import FastAPI
import time
from testspace.exceptions import AntdErrorResponse,ShowType
from fastapi import HTTPException,Request, Response


def error_handler(app:FastAPI):
    @app.middleware("http")
    async def exception_middleware(request:Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except HTTPException as e:
            response = Response(content= AntdErrorResponse(
                success=False,
                data= repr(e),
                errorCode=str(e.status_code),
                errorMessage=e.detail,
                showType=ShowType.error,
                traceId="",
                host=str(request.url.hostname)
                ).json())
            logger.error(f"{request.method} {request.url.path} {response.status_code} {response.body} {str(e)}")
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
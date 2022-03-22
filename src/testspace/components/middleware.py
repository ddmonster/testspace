
from testspace.log import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time
def error_handler(app:FastAPI):
    @app.middleware("http")
    async def exception_middleware(request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            response =  JSONResponse(status_code=500, content={"message": repr(e)})
            logger.error(f"{request.method} {request.url.path} {response.status_code} {response.body} {str(e)}")
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
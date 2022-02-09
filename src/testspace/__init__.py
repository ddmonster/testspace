from typing import Optional
from fastapi import FastAPI
from testspace.routers import find_routers

def create_app(config_path: Optional[str] = None) -> FastAPI:
    """
    Create the FastAPI application.
    """
    app = FastAPI()


    # register routers 
    for route in find_routers():
        app.include_router(route)


    return app



from fastapi import FastAPI,APIRouter   
from testspace.log import logger
def register_routers(app: FastAPI):
        router = APIRouter(prefix="/api")
        import testspace
        from testspace.utils.libautoimport import Module
        # get all modules in the routers package
        have_router = lambda module: isinstance(module.router, APIRouter) if hasattr(module,'router') else False
        root = Module(testspace)["api"]
        for m in root.iter_children():
            if have_router(m.module):
                router.include_router(m.router,prefix="/"+m.name)   
                logger.debug(f"add router [bold red]{m.module_path}[/bold red]") 
        app.include_router(router)
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from testspace.log import logger
from testspace.config import INDEX_PATH
from fastapi.responses import JSONResponse
from pathlib import Path

def register_routers(app: FastAPI):
    import importlib
    cur_path = Path(__file__).parent.joinpath("api")
    # get all modules in the routers package
    have_router = lambda module: isinstance(module.router, APIRouter) if hasattr(module,'router') else False
    for mod in cur_path.iterdir():
        if mod.is_dir():
            mod_name = mod.name
        elif mod.is_file() and mod.name.endswith('.py'):
            mod_name = mod.name.strip(".py")
        elif mod.name != '__pycache__' or mod.name != '__init__.py':
            continue
        module = importlib.import_module(f'.api.{mod_name}', package='testspace')
        if have_router(module):
            app.include_router(module.router,prefix=f"/{mod_name}")



app = FastAPI()


app.mount("/static",StaticFiles(directory=INDEX_PATH),"static")

@app.get("/index", response_class=HTMLResponse)
def index():
    index = INDEX_PATH.joinpath("index.html")
    if index.exists():
        return index.read_text()
    else:
        return ""

@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse("/index")
# @app.on_event("startup")
# async def startup_event():
#     logger = logging.getLogger("uvicorn.access")
#     handler = logging.StreamHandler()
#     handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#     logger.addHandler(handler)

# register routers 
register_routers(app)

@app.middleware("http")
async def exception_middleware(request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        response =  JSONResponse(status_code=500, content={"message": repr(e)})
        logger.error(f"{request.method} {request.url.path} {response.status_code} {response.body}")
    return response
import logging
from sys import prefix
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from testspace.config import ROOT_PATH
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from testspace.components.middleware import antd_adapter
from testspace.components.auth import set_auth,pwd_context
from testspace.components.cache import register_redis
from passlib.context import CryptContext
from testspace.models.user import User
from testspace.schemas.user import CreateUser
from loguru import logger
from testspace.crud.user import R_get_user_by_name, C_create_user
from testspace.schemas.user import CreateUser
from testspace.db.Session import openSession


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    with openSession() as s:
        from testspace.db.Base import create_schema
        create_schema()
        admin = R_get_user_by_name(s,'admin')
        if admin is None:
            user = CreateUser(username='admin',\
                accountname="Admin",\
                    email='', password=pwd_context.hash("123"),admin=True,avatar="icons/icons8-avatar-64.png")
            C_create_user(s,create_schema=user)
            
            
register_redis(app)
antd_adapter(app)
set_auth(app)

# router
def register_routers(app: FastAPI):
    import importlib
    router = APIRouter(prefix="/api")
    cur_path = Path(__file__).parent.joinpath("api")
    # get all modules in the routers package
    have_router = lambda module: isinstance(module.router, APIRouter) if hasattr(module,'router') else False
    for mod in cur_path.iterdir():
        if mod.is_dir():
            mod_name = mod.name
        elif mod.is_file() and mod.name.endswith('.py'):
            mod_name = mod.name.rstrip(".py")
        elif mod.name == '__pycache__' or mod.name == '__init__.py':
            continue
        module = importlib.import_module(f'testspace.api.{mod_name}')
        if have_router(module):
            router.include_router(module.router,prefix=f"/{mod_name}")
            
    app.include_router(router)
register_routers(app)


# task = endpoint.subscribe(ALL_TOPICS, call_back)
# asyncio.create_task(task)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


# CROS
origins = [
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Index
app.mount("/static",StaticFiles(directory=ROOT_PATH),"static")

@app.get("/index", response_class=HTMLResponse)
def index():
    index = ROOT_PATH.joinpath("index.html")
    if index.exists():
        return index.read_text()
    else:
        return ""

@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse("/index")




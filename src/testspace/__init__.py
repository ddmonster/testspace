import asyncio
import imp
import logging
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from testspace.config import INDEX_PATH
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from testspace.components.middleware import error_handler
from testspace.components.auth import set_auth
from passlib.context import CryptContext
from testspace.models.user import User
from testspace.schemas.user import CreateUser
from loguru import logger
from testspace.crud.user import R_get_user_by_name, C_create_user
from testspace.schemas.user import CreateUser
from testspace.db.session import openSession
# if User.get("admin") is None:
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     password = pwd_context.hash("123456")
#     user = User(**CreateUser(username="admin", accountname="Admin",email="aaa@aa.com",password=password, admin=True).dict())
#     user.flush()



app = FastAPI()
@app.on_event("startup")
async def startup_event():
    set_auth(app)
    with openSession() as s:
        admin = R_get_user_by_name(s,'admin')
        if admin is None:
            user = CreateUser(username='admin',\
                accountname="Admin",\
                    email='', password="123",admin=True)
            C_create_user(s,create_schema=user)

# error_handler(app)


# router
def register_routers(app: FastAPI):
    import importlib
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
            app.include_router(module.router,prefix=f"/{mod_name}")
register_routers(app)


# pubsub 
from fastapi_websocket_pubsub import PubSubEndpoint, ALL_TOPICS
import logging
from fastapi_websocket_rpc.logger import logging_config, LoggingModes
import asyncio
from testspace.components.pubsub import endpoint
async def call_back(data,topic):
    # print(">>>>>>>>>>>>>>>>>>>",data,topic)
    pass
logging_config.set_mode(LoggingModes.UVICORN,level=logging.DEBUG)

endpoint.register_route(app, "/pubsub")

# task = endpoint.subscribe(ALL_TOPICS, call_back)
# asyncio.create_task(task)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


# CROS
origins = [
    "http://localhost",
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




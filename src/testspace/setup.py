from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from testspace.components.middleware import antd_adapter
from testspace.components.swaggerui import setup_swagger_ui
from testspace.components.cache import register_redis
from testspace.components.auth import setup_auth_component
from testspace.db.Base import create_schema,drop_all_schema
from testspace.db.session import get_engine
from testspace.config import DATA_DIR,TomlConfig
from testspace.log import logger
from testspace.apimanager import register_routers
def create_app(tomlconfig:TomlConfig) -> FastAPI:
    app = FastAPI()
    app.state.config = tomlconfig
    SQLALCHEMY_DATABASE_URL  = tomlconfig.database.SQLALCHEMY_DATABASE_URL
    if tomlconfig.app.CHANNEL == 'dev':
        SQLALCHEMY_DATABASE_URL = tomlconfig.database.SQLALCHEMY_DATABASE_URL_dev
    elif tomlconfig.app.CHANNEL == "release":
        SQLALCHEMY_DATABASE_URL = tomlconfig.database.SQLALCHEMY_DATABASE_URL
    elif tomlconfig.app.CHANNEL == "test":
        SQLALCHEMY_DATABASE_URL = tomlconfig.database.SQLALCHEMY_DATABASE_URL_test
    engine = get_engine(SQLALCHEMY_DATABASE_URL)
    
    if tomlconfig.app.drop_all_table:
        drop_all_schema(engine)
    
    create_schema(engine)
    setup_auth_component(app,engine)
    register_redis(app)
    antd_adapter(app)
    register_routers(app)
    init_db_data(engine)
        
    # CROS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=tomlconfig.CROS.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static",StaticFiles(directory=DATA_DIR.joinpath("static")),"static")
    setup_swagger_ui(app)

        
    # set up swagger ui doc link in index
    @app.get("/apiUI", response_class=HTMLResponse,include_in_schema=False)
    def index():
        index = DATA_DIR.joinpath("static/html/index.html")
        logger.info(index)
        if index.exists():
            return index.read_text()
        else:
            return ""

    @app.get("/", response_class=RedirectResponse, include_in_schema=False)
    def root():
        return RedirectResponse("/apiUI")
    
    return app

    
def init_db_data(engine):
    from testspace.models.user import User, UserGroup
    from testspace.components.auth import get_password_hash
    from sqlmodel import select
    
    from sqlmodel import Session
    with Session(engine) as s:
        admin  = s.exec(select(User).where(User.username == "admin")).first()
        admin_group = s.exec(select(UserGroup).where(UserGroup.name == "admin")).first()
        if not admin and not admin_group:
            admin_group = UserGroup(**{"name":"admin","property":{}})
            admin_password = get_password_hash("123")
            admin = User(**{"username":"admin","password":admin_password,"admin":True,"groups":[admin_group]})
            
            s.add(admin_group)
            s.add(admin)
            s.commit()
            logger.info(f"admin")
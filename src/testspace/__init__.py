from . import api
from . import components
from . import crud
from . import db
from . import models
from . import schemas
from . import utils
from . import log, config,setup
from .setup import create_app

__all__=[
    "api",
    "components",
    "crud",
    "db",
    "models",
    "schemas",
    "log",
    "utils",
    "config",
    "setup",
    "app"
]

app = create_app()

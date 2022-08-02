import logging
from rich.logging import RichHandler
from testspace.config import tomlconfig

def get_log_level(name:str):
    log_level = ["INFO","DEBUG"]
    if name not in log_level:
        raise Exception(f"log level must be in {log_level}")
    return getattr(logging,name)

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
FORMAT_2 = ' %(asctime)s - %(threadName)s :%(thread)d  p:%(process)d - %(name)s [%(filename)s:%(lineno)d]  :  %(message)s'
from rich.logging import RichHandler
rich_handler = RichHandler(
    show_path=False,
    show_time=False,
    rich_tracebacks= False,
    tracebacks_show_locals= False,
    markup=True)

logging.basicConfig(
    level="NOTSET", format=FORMAT_2, datefmt="[%x %X]", handlers=[rich_handler], force=True
)

log_level =  get_log_level(tomlconfig.logconfig.level)
logger = logging.getLogger("testspace")

logger.setLevel(log_level)
sqlalchemy_engine_logger = logging.getLogger('sqlalchemy.engine')
# sqlalchemy_engine_logger.setLevel(log_level)
# sqlalchemy_engine_logger.addHandler(rich_handler)
# sqlalchemy_logger = logging.getLogger('sqlalchemy')
# uvicorn_logger = logging.getLogger("uvicorn")

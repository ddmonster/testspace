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
handler = RichHandler(show_path=False,show_time=False,rich_tracebacks=True,tracebacks_show_locals=True,markup=True)
logging.basicConfig(
    level="NOTSET", format=FORMAT_2, datefmt="[%x %X]", handlers=[handler]
)

log_level =  get_log_level(tomlconfig.logconfig.level)

logger = logging.getLogger("testspace")


# sqlalchemy_engine_logger = logging.getLogger('sqlalchemy.engine')
# sqlalchemy_engine_logger.setLevel(log_level)

sqlalchemy_logger = logging.getLogger('sqlalchemy')
sqlalchemy_logger.setLevel(log_level)
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.addHandler(handler)

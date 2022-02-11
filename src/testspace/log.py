from cmath import log
from fastapi.logger import logger
import logging

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s:  %(asctime)s - %(message)s"))
logger.addHandler(handler)


from sqlalchemy import true
import uvicorn
from testspace import config,setup
if __name__ == "__main__":
    if config.tomlconfig.development.level == "DEBUG":
        uvicorn.run("testspace.run:app", **config.tomlconfig.uvicorn)
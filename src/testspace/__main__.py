import uvicorn
from testspace import config
if __name__ == "__main__":
    # if config.tomlconfig.development.level == "DEBUG":
        uvicorn.run("testspace.instance:app", reload_includes=["*.py","*.toml"],**config.tomlconfig.uvicorn)
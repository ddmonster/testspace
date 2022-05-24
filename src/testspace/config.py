from environs import Env
from pathlib import Path
import toml
from testspace.log import logger
PACKAGE_PATH = Path(__file__).parent
env = Env()
env.read_env()

def set_data_dir(env):
    DATA_DIR:Path = env.path("DATA_DIR", default=PACKAGE_PATH)
    DATA_DIR = DATA_DIR.joinpath("data")
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR

DATA_DIR = set_data_dir(env)

PROJECT_DATA_DIR = PACKAGE_PATH.joinpath("data")

ROOT_PATH = PROJECT_DATA_DIR.joinpath("html")

config_toml = toml.load(PROJECT_DATA_DIR.joinpath("config.toml"))

class TomlConfig:
    def __init__(self, path):
        self.path = path
        self._dict = toml.load(path)
    def __getitem__(self, key):
        return self._dict.get(key)
    def __setitem__(self, key, value):
        self._dict[key] = value
    def __getattr__(self, __name: str):
        return self._dict[__name]
    def update(self):
        toml.dump(self._dict,self.path.open("w"))
    def __str__(self) -> str:
        return str(self._dict)

tomlconfig = TomlConfig(PROJECT_DATA_DIR.joinpath("config.toml"))

SECRET_KEY = "5aaca26c7bb7d1d8d2312498006db19cfe3953152a2541ab725ce8098c7d506c"

app_key = "asdasd"
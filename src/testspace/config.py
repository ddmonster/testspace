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

config_toml = toml.load(PROJECT_DATA_DIR.joinpath("config.toml"))

class TomlConfig:
    def __init__(self, path):
        self.path = path
        self._dict = toml.load(path)
    def __getitem__(self, key):
        return self._dict.get(key)
    def __setitem__(self, key, value):
        self._dict[key] = value
    def update(self):
        toml.dump(self._dict,self.path.open("w"))
    def __str__(self) -> str:
        return str(self._dict)

tomlconfig = TomlConfig(PROJECT_DATA_DIR.joinpath("config.toml"))
tomlconfig["database"]["SQLALCHEMY_DATABASE_URL"] = tomlconfig["database"]["SQLALCHEMY_DATABASE_URL"].format(data=PROJECT_DATA_DIR)


from environs import Env
from pathlib import Path
from dotmap import DotMap
import toml
PACKAGE_PATH = Path(__file__).parent
env = Env()
env.read_env()

def get_data_dir(env):
    DATA_DIR:Path = env.path("DATA_DIR", default=PACKAGE_PATH.joinpath("data"))
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR

DATA_DIR = get_data_dir(env)
ROOT_PATH = DATA_DIR
class TomlConfig:
    def __init__(self, path):
        self.path = path
        self._dict = toml.load(path)
    def __getitem__(self, key):
        return self._dict.get(key)
    def __getattr__(self, __name: str):
        return DotMap(self._dict[__name])
    def update(self):
        toml.dump(self._dict,self.path.open("w"))
    def __str__(self) -> str:
        return str(self._dict)

tomlconfig = TomlConfig(DATA_DIR.joinpath("config.toml"))

SECRET_KEY = "5aaca26c7bb7d1d8d2312498006db19cfe3953152a2541ab725ce8098c7d506c"

app_key = "asdasd"
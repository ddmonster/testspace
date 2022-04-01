from testspace.db.base_class import Base
from pathlib import Path
import importlib

cur_path = Path(__file__).parent.parent.joinpath("models")
# get all modules in the routers package
have_base = lambda module: True if hasattr(module,'Base') else False

for mod in cur_path.iterdir():
    if mod.is_dir():
        mod_name = mod.name
    elif mod.is_file() and mod.name.endswith('.py'):
        mod_name = mod.name.strip(".py")
    elif mod.name != '__pycache__' or mod.name != '__init__.py':
        continue
    importlib.import_module(f'testspace.models.{mod_name}')
    
def create_schema():
    from testspace.db.session import engine
    Base.metadata.create_all(bind = engine, checkfirst=True)
if __name__ == "__main__":
    from testspace.db.session import engine
    Base.metadata.create_all(bind = engine, checkfirst=True)
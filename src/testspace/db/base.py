from testspace.db.base_class import Base

from pathlib import Path
import importlib

print("-----------------sdsad",__name__)
cur_path = Path(__file__).parent.parent.joinpath("models")
# get all modules in the routers package
have_base = lambda module: True if hasattr(module,'Base') else False

for mod in cur_path.iterdir():
    if mod.is_file() and mod.name.endswith('.py'):
        mod_name = mod.name.strip(".py")
    elif mod.name != '__pycache__' or mod.name != '__init__.py':
        continue
    
    importlib.import_module(f'testspace.models.{mod_name}')
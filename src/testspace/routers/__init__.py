import importlib
from pathlib import Path
from fastapi import APIRouter

def find_routers():
    cur_path = Path(__file__).parent
    # get all modules in the routers package
    routers = []
    have_router = lambda module: isinstance(module.router, APIRouter) if hasattr(module,'router') else False
    for mod in cur_path.iterdir():
        if mod.is_dir() :
            mod_name = mod.name
        elif mod.is_file() and mod.name.endswith('.py'):
            mod_name = mod.name.strip(".py")
        elif mod.name != '__pycache__' or mod.name != '__init__.py':
            continue
        module = importlib.import_module(f'{__name__}.{mod_name}')
        if have_router(module):
            module.router.prefix = f'/{mod_name}'
            routers.append(module.router)
    return routers
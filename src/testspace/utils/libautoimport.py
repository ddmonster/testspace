
import pathlib
import importlib
import importlib.machinery
import re
from typing import Callable, Iterable, Optional,cast
from types import ModuleType
from functools import cache
__all__ = ["Module"]
class Module:
    
    def __init__(self,package:pathlib.Path | ModuleType , parent:Optional["Module"] = None) -> None:
        self.mark = package
        self.parent = parent
    
    def is_package(self):
        if self.path.is_dir(): 
            return True
        return False

    @property
    def path(self) -> pathlib.Path:
        if type(self.mark) is ModuleType:
            return pathlib.Path(self.mark.__path__[0])
        return cast(pathlib.Path,self.mark)
    
    @property
    @cache
    def module(self):
        return importlib.import_module(self.module_path)
    @cache
    def import_module(self):
        return importlib.import_module(self.module_path)
    @property
    def module_path(self):
        _path = self.name
        parent = cast(Module,self.parent)
        while parent:
            _path = parent.name + "." + _path
            parent = parent.parent
        return _path
    @property # ignore
    def name(self):
        if self.path.is_dir():
            return self.path.name
        
        return re.sub(".py$","",self.path.name)
        
    def __getitem__(self, __name) -> "Module":
        for i in self.iter_children():
            if i.name == __name:
                return i
        raise KeyError(f"{__name} not Found")
    def iter_children(self, filter_call: Optional[Callable[[pathlib.Path], bool]] = None)-> Iterable["Module"]:
        if filter_call:
            yield from self._find_packages(filter_call)
        else:
            yield from self._find_packages(lambda p: False if re.match("^__.*__(.?py)$",p.name) or p.name == "__pycache__" else True)
        
    def glob(self,filter_call: Optional[Callable[[pathlib.Path], bool]] = None):
        yield from self._iter(self,filter_call)
            
    def _iter(self,sub_package:"Module", filter_call: Optional[Callable[[pathlib.Path], bool]] = None):
        for m in sub_package.iter_children(filter_call):
            if m.is_package():
                yield from self._iter(m)
            yield m
            
    def __str__(self):
        return f"{self.path, self.parent}"
        
    def _find_packages(self,filter_call:Callable[[pathlib.Path], bool]):
        if not self.is_package():
            raise Exception(f"{self.path} not a package")
        package_path = self.path
        for p in filter(filter_call,package_path.iterdir()):
                yield Module(p,self)

        
    def __getattr__(self, __name):
        return getattr(self.module,__name)        
        
if __name__ == "__main__":
    pass
    # m =  Module(testspace,None)
    # print(m["utils"]["gen"].curtime())
            
        
    
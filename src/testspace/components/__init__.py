
from typing import Callable, Generic, TypeVar
from testspace.schemas.user import UserProps
from testspace.utils.ContextVarsWapper import ContextWarpper


current_user = ContextWarpper[UserProps]("current access user",None)
'''UserProps'''


T = TypeVar("T")
class LazyLoad(Generic[T]):
    def __init__(self , create: Callable[[],T]) -> None:
        self._inner:T
        self.create = create
    def __getattr__(self,__name:str):
        if not self._inner:
            self._inner = self.create()
        return getattr(self._inner,__name)
            
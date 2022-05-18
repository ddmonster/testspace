import weakref

from typing import Generic, Optional, TypeVar


T = TypeVar("T")

class TypeWeakRef(Generic[T]):
    def __init__(self, ref:T) -> None:
        self.__ref = weakref.ref(ref)
    def get(self) -> Optional[T]:
        return self.__ref()
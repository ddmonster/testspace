from typing import Union
from testspace.schemas.user import UserProps

from testspace.utils.ContextVarsWapper import ContextWarpper


current_user:Union[UserProps,None] = ContextWarpper("current access user",None)
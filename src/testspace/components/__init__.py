
from testspace.schemas.user import UserProps
from testspace.utils.ContextVarsWapper import ContextWarpper


current_user = ContextWarpper[UserProps]("current access user",None)
'''UserProps'''
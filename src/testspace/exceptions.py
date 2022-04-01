


from pydantic import BaseModel
from typing import Any
from enum import IntEnum

class ShowType(IntEnum):
    silent = 0
    warn =1
    error =2
    notification = 4
    page = 9
class AntdErrorResponse(BaseModel):
    success: bool; # if request is success
    data: Any; # response data
    errorCode: str; # code for errorType
    errorMessage: str; # message display to user
    showType: ShowType; #error display type： 0 silent; 1 message.warn; 2 message.error; 4 notification; 9 page
    traceId: str; #Convenient for back-end Troubleshooting: unique request ID
    host: str;# onvenient for backend Troubleshooting: host of current access server





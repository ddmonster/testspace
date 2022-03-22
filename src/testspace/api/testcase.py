from tkinter.filedialog import Open
from fastapi import APIRouter, Depends, Header, Path
from testspace.models.testcase import Testcase,TestSuite
from testspace.models.user import User
from testspace.schemas.testcase import *
from testspace.crud.testcase import C_create_testcase
from .import set_page_enable_api

from testspace.db.session import get_db, Session
router  = APIRouter(tags=["testcase management"])



set_page_enable_api(router,Testcase,TestcaseProps)


@router.post("/", response_model=TestcaseProps)
def create_case(case:TestcaseCreate, session:Session = Depends(get_db)):
    return C_create_testcase(session,case)
    





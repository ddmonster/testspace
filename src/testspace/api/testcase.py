
from fastapi import APIRouter, Depends, Header, Path
from testspace.models.testcase import Testcase,TestSuite
from testspace.schemas.testcase import *
from .import set_page_enable_api
from testspace.db.Session import session
from testspace.crud.testcase import C_create_testcase, \
                                    R_get_testcases_by_uuid, \
                                    U_update_testcase_by_uuid,\
                                    D_delete_testcase_by_uuid

router  = APIRouter(tags=["Testcase Management"])

set_page_enable_api(router,Testcase,TestcaseProps)


@router.post("/", response_model=TestcaseProps)
def create_testcase(case:TestcaseCreate):
    return C_create_testcase(session,case)

@router.get("/{uuid}",response_model=TestcaseProps)
def get_testcase(uuid:UUID):
    return R_get_testcases_by_uuid(session,uuid)

@router.patch("/{uuid}", response_model=TestcaseProps)
def update_case(uuid:UUID,case:TestcaseUpdate):
    return U_update_testcase_by_uuid(session,uuid,case)
    
@router.delete("/{uuid}")
def delete_testcase(uuid:UUID):
    D_delete_testcase_by_uuid(session,uuid)





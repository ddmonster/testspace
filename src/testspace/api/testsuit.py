
from fastapi import APIRouter, Depends, Header, Path
from testspace.models.testcase import TestSuite
from testspace.schemas.testcase import *
from .import set_page_enable_api
from testspace.db.Session import session
from testspace.crud.testcase import C_create_testsuit, D_delete_testsuit_by_uuid,R_get_testsuit_by_uuid, U_update_testsuit_by_uuid,U_update_testsuit_by_uuid
router  = APIRouter(tags=["testsuit management"])



set_page_enable_api(router,TestSuite,TestSuitProps)


@router.post("/", response_model=TestSuitProps)
def create_testsuit(suit:TestSuitCreate):
    return C_create_testsuit(session,suit)

@router.get("/{uuid}",response_model=TestSuitProps)
def get_testsuit(uuid:UUID, ):
    return R_get_testsuit_by_uuid(session,uuid)

@router.patch("/{uuid}",response_model=TestSuitProps)
def update_testsuit(uuid:UUID,case:TestSuitUpdate):
    return U_update_testsuit_by_uuid(session,uuid,case)

@router.delete("/{uuid}")
def delete_testsuit(uuid:UUID):
    D_delete_testsuit_by_uuid(session,uuid)
    return True
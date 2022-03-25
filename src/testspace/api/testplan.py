
from fastapi import APIRouter, Depends, Header, Path
from testspace.models.testcase import TestPlan
from testspace.schemas.testcase import *
from .import set_page_enable_api
from testspace.db.session import get_db, Session
from testspace.crud.testcase import *
router  = APIRouter(tags=["Testplan management"])



set_page_enable_api(router,TestPlan,TestPlanProps)


@router.post("/", response_model=TestPlanProps)
def create_testplan(plan:TestPlanCreate, session:Session = Depends(get_db)):
    return C_create_testplan(session,plan)

@router.get("/{uuid}",response_model=TestPlanProps)
def get_testplan(uuid:UUID,session:Session = Depends(get_db)):
    return R_get_testplan_by_uuid(session,uuid)

@router.patch("/{uuid}", response_model=TestPlanProps)
def update_testplan(uuid:UUID,plan:TestPlanUpdate,session:Session = Depends(get_db)):
    return U_update_testplan_by_uuid(session,uuid,plan)

@router.delete("/{uuid}")
def delete_testplan(uuid:UUID, session:Session = Depends(get_db)):
    D_delete_testplan_by_uuid(session,uuid)
    return True
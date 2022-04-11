
from fastapi import APIRouter, Depends, Header, Path, Query
from testspace.models.testcase import TestPlan
from testspace.schemas.testcase import *
from .import set_page_enable_api
from testspace.db.Session import session
from testspace.crud.testcase import *
from testspace.components.cache import redis
router  = APIRouter(tags=["Testplan management"])



set_page_enable_api(router,TestPlan,TestPlanProps)


@router.post("/", response_model=TestPlanProps)
def create_testplan(plan:TestPlanCreate):
    return C_create_testplan(session,plan)



@router.get("/{uuid}", response_model=TestPlanProps)
def get_testplan(uuid:UUID, details:bool = False):
    testplan =  R_get_testplan_by_uuid(session,uuid)
    testplan_props = TestPlanProps.from_orm(testplan)
    if details:
        testplan_props.testsuits = R_get_testsuits_by_testplan_uuid(session,uuid)
    
    return testplan_props

@router.patch("/{uuid}", response_model=TestPlanProps)
def update_testplan(uuid:UUID,plan:TestPlanUpdate):
    return U_update_testplan_by_uuid(session,uuid,plan)

@router.delete("/{uuid}")
def delete_testplan(uuid:UUID):
    D_delete_testplan_by_uuid(session,uuid)
    return True

@router.get("/cache/{key}")
async def get_cache(key:str):
    return await redis.get(key)

@router.post("/cache/{key}")
async def create_key(key:str,value:str):
    await redis.set(key,value)
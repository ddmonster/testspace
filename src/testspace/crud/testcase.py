from typing import Any, List, Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from testspace.models.testcase import TestPlan, Testcase,TestSuite
from testspace.models.user import User
from .common.exception import NotFoundException
from testspace.schemas.testcase import \
    TestcaseCreate,TestcaseProps, TestcaseUpdate,\
    TestSuitCreate,TestSuitProps,TestSuitUpdate,\
    TestPlanCreate,TestPlanProps,TestPlanUpdate

# testcase 
def C_create_testcase(s:Session, case:TestcaseCreate)->TestcaseProps:
    ts = Testcase(**case.dict())
    s.add(ts)
    s.commit()
    return ts

def R_get_testcases_by_uuid(s:Session,uuid:UUID) -> Union[TestcaseProps, None]:
    return s.query(Testcase).filter_by(uuid = uuid).first()
        
def U_update_testcase_by_uuid(s:Session,uuid:UUID, case:TestcaseUpdate):
    q = s.query(Testcase).filter_by(uuid=uuid)
    c= q.first()
    if c is None:
        raise NotFoundException(case, f"<uuid= {uuid}> not  found in table {Testcase.name}")
    q.update(case.dict(exclude={'uuid'},exclude_none=True),synchronize_session="fetch")
    s.refresh(c)
    return c

def D_delete_testcase_by_uuid(s:Session, uuid:UUID):
    s.query(Testcase).filter_by(uuid=uuid).delete()

# testsuit
def C_create_testsuit(s:Session, suit:TestSuitCreate) -> TestSuitProps:
    ts = TestSuite(**suit.dict(exclude_none=True))
    s.add(ts)
    s.commit()
    return ts

def R_get_testsuit_by_uuid(s:Session,uuid:UUID) -> Union[TestSuitProps, None]:
    return s.query(TestSuite).filter_by(uuid = uuid).first()
def R_get_testsuits_by_testplan_uuid(s:Session,uuid:UUID)-> List[TestSuitProps]:
    return s.query(TestSuite).filter(TestSuite.testplans.contains([uuid])).order_by(TestSuite.created_at).all()
def U_update_testsuit_by_uuid(s:Session,uuid:UUID, su:TestSuitUpdate):
    q = s.query(TestSuite).filter_by(uuid=uuid)
    suit = q.first()
    if suit is None:
        raise NotFoundException(su, f"<uuid= {uuid}> not  found in table {TestSuite.name}")
    q.update(su.dict(exclude={'uuid'},exclude_none=True),synchronize_session="fetch")
    s.commit()
    s.refresh(suit)
    return suit
def D_delete_testsuit_by_uuid(s:Session, uuid:UUID):
    s.query(TestSuite).filter_by(uuid=uuid).delete()
        
        
# testplan
def C_create_testplan(s:Session, plan:TestPlanCreate) -> TestPlanProps:
    ts = TestPlan(**plan.dict(exclude_none=True))
    s.add(ts)
    s.commit()
    return ts

def R_get_testplan_by_uuid(s:Session,uuid:UUID) -> Union[TestPlanProps, None]:
    return s.query(TestPlan).filter_by(uuid = uuid).first()

def U_update_testplan_by_uuid(s:Session,uuid:UUID, p:TestPlanUpdate):
    q = s.query(TestPlan).filter_by(uuid=uuid)
    plan = q.first()
    if plan is None:
        raise NotFoundException(p, f"<uuid= {uuid}> not  found in table {TestPlan.name}")
    q.update(p.dict(exclude={'uuid'},exclude_none=True),synchronize_session="fetch")
    s.commit()
    s.refresh(plan)
    return plan

def D_delete_testplan_by_uuid(s:Session, uuid:UUID):
    s.query(TestPlan).filter_by(uuid=uuid).delete()
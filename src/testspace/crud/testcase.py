from sqlalchemy.orm import Session
from testspace.models.testcase import Testcase,TestSuite

from testspace.schemas.testcase import TestcaseCreate,TestcaseProps


def C_create_testcase(s:Session, case:TestcaseCreate):
    ts = Testcase(**case.dict())
    with s.begin():
        ts = Testcase(**case.dict())
        s.add(ts)
        s.commit()
    return ts
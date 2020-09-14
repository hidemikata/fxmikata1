import Model.sqlbase as sqlbase
import datetime
from sqlalchemy import Column, String, DateTime


class FxDataUsdJpy1M(sqlbase.Base):
    __tablename__ = 'usd_jpy_1m'
    time = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True, nullable=False)
    name = Column(String)


def testadd():
    d = FxDataUsdJpy1M()
    d.name = 'cde'
    with sqlbase.get_session() as session:
        session.add(d)


def testget():
    r = FxDataUsdJpy1M.query.all()
    for c in r:
        print(c.time)
        print(c.name)

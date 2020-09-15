import Model.sqlbase as sqlbase
import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer


class FxDataUsdJpy1M(sqlbase.Base):
    __tablename__ = 'usd_jpy_1m'
    time = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


def add_price(self, time, open, high, low, close):
    d = FxDataUsdJpy1M()
    d.time = time
    d.open = open
    d.hight = high
    d.low = low
    with sqlbase.get_session() as session:
        session.add(d)


def testget():
    r = FxDataUsdJpy1M.query.all()
    #for c in r:
    #    print(c.time)
    #    print(c.name)

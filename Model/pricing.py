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

    @classmethod
    def get_latest(cls):
        r = FxDataUsdJpy1M.query.limit(1).all()
        r = r[0]
        return [r.open, r.high, r.low, r.close]

    @classmethod
    def get(cls, limit=1):
        r = FxDataUsdJpy1M.query.limit(limit).all()
        return r

    @classmethod
    def add_price(cls, time, open, high, low, close):
        #instansをわたすらしい
        d = FxDataUsdJpy1M()
        d.time = time
        d.open = open
        d.high = high
        d.low = low
        d.close = close
        with sqlbase.get_session() as session:
            session.add(d)

#定義の後でテーブル生成
sqlbase.create_all()



import Model.sqlbase as sqlbase
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, desc


class FxDataUsdJpy1M(sqlbase.Base):
    __tablename__ = 'usd_jpy_1m'
    time = Column(DateTime, default=datetime.utcnow, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    @classmethod
    def get_latest(cls):
        r = FxDataUsdJpy1M.query.order_by(desc(FxDataUsdJpy1M.time)).limit(1).all()
        return r[0]


    @classmethod
    def get(cls, limit=1):
        r = FxDataUsdJpy1M.query.limit(limit).all()
        return r

    @classmethod
    def add_price(cls, time, open, high, low, close):
        #クラスをそのまま渡したいけどinstansをわたすらしい
        d = FxDataUsdJpy1M()
        d.time = time
        d.open = open
        d.high = high
        d.low = low
        d.close = close
        with sqlbase.get_session() as session:
            session.add(d)

    @classmethod
    def save_data(cls, data):
        with sqlbase.get_session() as session:
            session.add(data)

    @classmethod
    def truncate_time(self, time):
        time_format = '%Y-%m-%d %H:%M'
        str_date = datetime.strftime(time, time_format)
        return datetime.strptime(str_date, time_format)

    @classmethod
    def update(cls, time, price):
        time = cls.truncate_time(time)
        latest = cls.get_latest()
        #getfortimeをつくってtimeを指定して取ってくるやつをつくる。あれば更新する。
        #なければnewしてつくる。
        latest.close = price
        cls.save_data(latest)



#定義の後でテーブル生成
sqlbase.create_all()



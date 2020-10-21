import Model.sqlbase as sqlbase
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, desc, asc, or_


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
        return r[0] if r else None


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
    def truncate_time(cls, time):
        time_format = '%Y-%m-%d %H:%M'
        str_date = datetime.strftime(time, time_format)
        return datetime.strptime(str_date, time_format)

    @classmethod
    def update(cls, time, price):
        #timeはdatetime型
        time = cls.truncate_time(time)
        latest = cls.get_latest()
        is_create = False
        if latest and latest.time == time:
            #更新
            latest.close = price
            if latest.high < price:
                latest.high = price
            elif latest.low > price:
                latest.low = price
            cls.save_data(latest)
        else:
            #新規
            d = FxDataUsdJpy1M()
            d.time = time
            d.open = price
            d.high = price
            d.low = price
            d.close = price
            cls.save_data(d)
            is_create = True

        return is_create

    @classmethod
    def get_count(cls, filter_time='%'):
        return FxDataUsdJpy1M.query.filter(or_(i for i in filter_time)).count()

    @classmethod
    def get_close_test(cls, limit=100, past_offset=0, filter_time='%'):
        r = FxDataUsdJpy1M.query.filter(or_(i for i in [FxDataUsdJpy1M.time.like('%-%-% '+'01'+':%:%'), FxDataUsdJpy1M.time.like('%-%-% '+'02'+':%:%')])).all()
        rlist = [i.time for i in r]
        for i in rlist:
            print(i)
        exit()
#        r =
        return r

    @classmethod
    def get_close_past_date(cls, limit=100, past_offset=0, filter_time=None):
        r = FxDataUsdJpy1M.query.filter(or_(i for i in filter_time)).order_by(desc(FxDataUsdJpy1M.time)).limit(limit).offset(past_offset).all()
        r = sorted(r, key=lambda t: t.time, reverse=False)
        return r

    @classmethod
    def get_close_data(cls, limit=100, chomp_num=1):
        r = FxDataUsdJpy1M.query.order_by(desc(FxDataUsdJpy1M.time)).limit(limit).all()
        #offsetでかきなおしたい。
        for i in range(chomp_num):
            r.pop(0)

        r = sorted(r, key=lambda t: t.time, reverse=False)

        return [i.close for i in r]

#定義の後でテーブル生成
sqlbase.create_all()



import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///fxdatabase.sql', echo=True)

Base = declarative_base()


class FxDataUsdJpy1M(Base):
    __tablename__ = 'usd_jpy_1m'

    time = Column(DateTime,default=datetime.datetime.utcnow, primary_key=True, nullable=False)
    name = Column(String)


Base.metadata.create_all(engine)


def test():
    print('test')
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(FxDataUsdJpy1M(name='abc'))
    session.commit()
    session.close()

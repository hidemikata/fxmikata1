import datetime
import threading
from contextlib import contextmanager
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

logger = logging.getLogger(__name__)  # ???

lock = threading.Lock()

engine = create_engine('sqlite:///fxdatabase.sql', echo=True)

Base = declarative_base()

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine))

Base.metadata.create_all(engine)
Base.query = Session.query_property()

@contextmanager
def get_session():
    session = Session()
    session.expire_on_commit = False
    try:
        lock.acquire()
        yield session
        session.commit()
    except Exception as e:
        logger.error(f'sqlbase error 1{e}')
        session.rollback()
        raise
    finally:
        session.expire_oncommit = True
        lock.release()



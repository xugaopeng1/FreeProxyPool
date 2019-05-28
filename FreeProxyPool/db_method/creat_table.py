"""
创建表
"""

from setting import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, create_engine, TIMESTAMP, Float

Base = declarative_base()


class ItemInfo(Base):
    """define louzhu item"""

    __tablename__ = "proxy"

    id = Column(Integer, primary_key=True)
    ip_info = Column(String(255))
    ip_type = Column(String(255))
    res_time = Column(Float)
    score = Column(String(255))
    flag = Column(String(10))
    date_time = Column(String(255))


def create_table():
    if passwd:
        db_engine = """mysql+mysqlconnector://{user}:{passwd}@{host}:3306/db_proxy""".format(
            user=user, passwd=passwd, host=host
        )
    else:
        db_engine = """mysql+mysqlconnector://{user}@{host}:3306/db_proxy""".format(
            user=user, host=host
        )
    engine = create_engine(db_engine, echo=False)
    DBSession = sessionmaker(engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    session.commit()


if __name__ == "__main__":
    create_table()

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text, UUID, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import AccessRights

engine_1 = create_engine("mysql+pymysql://user:password@mariadb-node1/database?charset=utf8mb4")
engine_2 = create_engine("mysql+pymysql://user:password@mariadb-node2/database?charset=utf8mb4")

Session_1 = sessionmaker(bind=engine_1)
Session_2 = sessionmaker(bind=engine_2)


def get_session_1() -> Session_1:
    session = Session_1()
    try:
        yield session
    finally:
        session.close()


def get_session_2() -> Session_2:
    session = Session_2()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'user'

    uuid = Column(UUID, primary_key=True)
    email = Column(String(64), nullable=False, unique=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    patronymic = Column(String(64))
    access_rights = Column(Enum(AccessRights), nullable=False)


class ReportTable(Base):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    annotation = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_date = Column(DateTime(timezone=True))
    moderation_flag = Column(Boolean, default=False, nullable=False)
    user_uuid = Column(UUID, nullable=False)
    conference_id = Column(Integer)


class ConferenceTable(Base):
    __tablename__ = 'conference'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)


if __name__ == '__main__':
    engine_1_localhost = create_engine(
        "mysql+pymysql://user:password@localhost:3306/database?charset=utf8mb4",
        echo=True,
    )
    Base.metadata.create_all(bind=engine_1_localhost)
    engine_2_localhost = create_engine(
        "mysql+pymysql://user:password@localhost:3316/database?charset=utf8mb4",
        echo=True,
    )
    Base.metadata.create_all(bind=engine_2_localhost)

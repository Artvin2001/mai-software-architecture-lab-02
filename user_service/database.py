from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, UUID, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import AccessRights

engine = create_engine("mysql+pymysql://user:password@mariadb/database?charset=utf8mb4")

Session = sessionmaker(bind=engine)


def get_session() -> Session:
    session = Session()
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
    user_id = Column(UUID, ForeignKey('user.uuid', ondelete="CASCADE"), nullable=False)
    conference_id = Column(Integer, ForeignKey('conference.id', ondelete="CASCADE"))


class ConferenceTable(Base):
    __tablename__ = 'conference'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)


if __name__ == '__main__':
    engine_localhost = create_engine("mysql+pymysql://user:password@localhost/database?charset=utf8mb4", echo=True)
    Base.metadata.create_all(bind=engine_localhost)

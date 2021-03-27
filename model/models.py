from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import settings


engine = create_engine('sqlite:///{}'.format(settings.database_address))
Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('chats_id', Integer, ForeignKey('chats.chat_id')),
                          Column('tags_id', Integer, ForeignKey('tags.id'))
                          )


class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True, autoincrement=False)
    first_name = Column(String(65), default='', nullable=False)
    last_name = Column(String(65), default='', nullable=False)
    username = Column(String(65), default='', nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_bot = Column(Boolean, default=False, nullable=False)
    state = Column(String(10000), default='', nullable=False)


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(BigInteger, primary_key=True, autoincrement=False)
    title = Column(String(65), default='', nullable=False)
    type = Column(String(65), default='', nullable=False)
    tags = relationship("Tag",
                        secondary=association_table,
                        back_populates="chats")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), default='', nullable=False)
    chats = relationship("Chat",
                         secondary=association_table,
                         back_populates="tags")


Base.metadata.create_all(engine)

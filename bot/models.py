from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    telegram_id = Column(Integer)
    registration_date = Column(Date)


class ItemType(Base):
    __tablename__ = 'item_types'
    type_id = Column(Integer, primary_key=True)
    data_type = Column(String)
    description = Column(String)
    children = relationship("ToSeeItem")


class ToSeeItem(Base):
    __tablename__ = 'to_see_items'
    record_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    message_id = Column(Integer)
    date_received =Column(Date)
    type_id = Column(Integer, ForeignKey("item_types.type_id"))
    raw_data = Column(String)

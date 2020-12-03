"""
Module with Database scheme and tables initializations.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class User(base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    telegram_id = Column(Integer)
    registration_date = Column(DateTime)


class ItemType(base):
    __tablename__ = "item_types"
    type_id = Column(Integer, primary_key=True)
    data_type = Column(String)
    description = Column(String)
    children = relationship("ToSeeItem")


class ToSeeItem(base):
    __tablename__ = "to_see_items"
    record_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    message_id = Column(Integer)
    date_received = Column(DateTime)
    type_id = Column(Integer, ForeignKey("item_types.type_id"))
    raw_data = Column(String)
    showed = Column(Boolean, default=False)

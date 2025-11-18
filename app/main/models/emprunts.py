from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base


class EmpruntStatus(str, Enum):

    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    closed = "closed"



class Emprunt(Base):
    __tablename__ = "emprunts"


    uuid = Column(String(36), primary_key=True,index=True)

    added_by: str = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=True)
    user = relationship("User", foreign_keys=[added_by])

    user_uuid: str = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=True)
    customer = relationship("User", foreign_keys=[user_uuid])

    book_uuid: str = Column(String, ForeignKey('books.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=True)
    book = relationship("Book", foreign_keys=[book_uuid])

    note : str = Column(Text, nullable=True)
    status : str = Column(String, nullable=False,default=EmpruntStatus.pending)

    is_deleted: bool = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp


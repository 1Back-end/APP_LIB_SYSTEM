from datetime import datetime

from cloudinary.utils import unique
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func,Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class Book(Base):

    __tablename__ = 'books'


    uuid : str = Column(String, primary_key=True,index=True)
    name : str = Column(String,index=True,unique=True)
    category_book_uuid: str = Column(String, ForeignKey('category_books.uuid', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    category = relationship("CategoryBooks", foreign_keys=[category_book_uuid])
    gender : str = Column(String,index=True,nullable=False)
    currency : str = Column(String,index=True,nullable=False)
    price : str = Column(String,index=True,nullable=False)
    full_price : str = Column(String,index=True,nullable=False)
    author : str = Column(String,index=True,nullable=False)
    year : str = Column(String,index=True,nullable=False)
    isbn : str = Column(String,index=True,unique=True,nullable=False)
    description : str = Column(String,index=True,nullable=False)
    publisher_date : datetime = Column(DateTime,index=True,nullable=False)
    image_uuid: str = Column(String, ForeignKey('storages.uuid', ondelete="CASCADE", onupdate="CASCADE"),
                              nullable=True)
    image = relationship("Storage", foreign_keys=[image_uuid])

    added_by: str = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"),
                           nullable=True)
    user = relationship("User", foreign_keys=[added_by])

    is_active : bool = Column(Boolean,nullable=False)
    is_deleted : bool = Column(Boolean,nullable=False)
    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp
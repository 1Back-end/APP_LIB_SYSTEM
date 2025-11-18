from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base


class CategoryBooks(Base):
    __tablename__ = "category_books"


    uuid : str = Column(String, primary_key=True,index=True)
    name : str = Column(String,nullable=False,unique=True)
    description : str = Column(String,nullable=True)
    is_active : bool = Column(Boolean,nullable=False,default=True)
    is_deleted : bool = Column(Boolean,nullable=False,default=False)
    added_by: str = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"),
                              nullable=True)
    user = relationship("User", foreign_keys=[added_by])
    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp
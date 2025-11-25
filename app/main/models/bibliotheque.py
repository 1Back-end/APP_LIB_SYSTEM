from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base


class BibliothequeStatus(str, Enum):

    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    closed = "closed"


class Bibliotheque(Base):
    __tablename__ = "bibliotheques"

    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True)
    phone_number_2 = Column(String, nullable=True)
    email = Column(String, nullable=True)
    web_site = Column(String, nullable=True)
    id_number = Column(String, nullable=True, unique=True)

    description = Column(Text, nullable=True)

    added_by: str = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=False)
    user = relationship("User", foreign_keys=[added_by])


    address_uuid: str = Column(String, ForeignKey('addresses.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=False)
    address = relationship("Address", foreign_keys=[address_uuid])

    country_uuid: str = Column(String, ForeignKey('country.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=False)
    country = relationship("Country", foreign_keys=[country_uuid])

    city_uuid: str = Column(String, ForeignKey('cities.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=False)
    city = relationship("City", foreign_keys=[city_uuid])

    manager_uuid: str = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"),nullable=False)
    nmanager = relationship("User", foreign_keys=[manager_uuid])

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

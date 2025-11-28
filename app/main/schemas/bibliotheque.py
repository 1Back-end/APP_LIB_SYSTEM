from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.contry_with_city import CitySlim, CountrySlim
from app.main.schemas.user import AddedBySlim
from app.main.schemas.address import AddressSlim


class Bibliotheque(BaseModel):
    name: str
    phone_number: str
    phone_number_2: Optional[str]
    email: str
    web_site: str
    id_number: str
    description: Optional[str]
    address_uuid: str
    country_uuid: str
    city_uuid: str
    street: str
    city: str
    state: Optional[str] = None
    zipcode: str
    country: str


class BibliothequeCreate(Bibliotheque):
    pass


class BibliothequeUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    phone_number: Optional[str]
    phone_number_2: Optional[str]
    email: Optional[str]
    web_site: Optional[str]
    id_number: Optional[str]
    description: Optional[str]
    address_uuid: Optional[str]
    country_uuid: Optional[str]
    city_uuid: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str] 
    zipcode: Optional[str]
    country: Optional[str]


class BibliothequeUpdateStatus(BaseModel):
    uuid: str
    status: str


class BibliothequeDelete(BaseModel):
    uuid: str


class BibliothequeResponse(BaseModel):
    uuid: str
    name: Optional[str]
    phone_number: Optional[str]
    phone_number_2: Optional[str]
    email: Optional[str]
    web_site: Optional[str]
    id_number: Optional[str]
    description: Optional[str]
    address: AddressSlim
    country: CountrySlim
    city: CitySlim
    nmanager: AddedBySlim
    user: AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class BibliothequeResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[BibliothequeResponse]

    model_config = ConfigDict(from_attributes=True)
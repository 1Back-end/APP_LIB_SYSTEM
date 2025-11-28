import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session

from app.main.core.security import generate_password, get_password_hash
from app.main.crud.base import CRUDBase
from app.main import models,schemas


class CRUD_BIBLIOTHEQUE(CRUDBase[models.Bibliotheque,schemas.BibliothequeUpdate,schemas.BibliothequeCreate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str)->Optional[schemas.Bibliotheque]:
        return db.query(models.Bibliotheque).filter(models.Bibliotheque.uuid == uuid,models.Bibliotheque.is_deleted==False).first()

    @classmethod
    def get_by_email(cls,db:Session,email:str)->Optional[schemas.Bibliotheque]:
        return db.query(models.Bibliotheque).filter(models.Bibliotheque.email==email,models.Bibliotheque.is_deleted==False).first()

    @classmethod
    def get_by_id_number(cls,db:Session,id_number:str)->Optional[schemas.Bibliotheque]:
        return db.query(models.Bibliotheque).filter(models.Bibliotheque.id_number==id_number,models.Bibliotheque.is_deleted==False).first()

    @classmethod
    def create(cls,db:Session,obj_in:schemas.BibliothequeCreate) -> schemas.BibliothequeCreate:
        password: str = generate_password(8, 8)
        print(f"User password: {password}")  # Pour debug ou logs, attention à ne pas le faire en prod !

        commond_user_uuid = str(uuid.uuid4())
        new_user = models.User(
            uuid = commond_user_uuid,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            role = models.UserRole.MANAGER,
            password_hash=get_password_hash(password)
        )
        db.add(new_user)
        db.commit()

        commond_address_uuid = str(uuid.uuid4())

        new_address = models.Address(
            uuid = commond_address_uuid,
            street = obj_in.street,
            city = obj_in.city,
            state = obj_in.state,
            zipcode = obj_in.zipcode,
            country = obj_in.country,
        )
        db.add(new_address)
        db.commit()


        new_bibliotheque = models.Bibliotheque(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            phone_number = obj_in.phone_number,
            phone_number_2 = obj_in.phone_number_2,
            email = obj_in.email,
            web_site = obj_in.web_site,
            id_number = obj_in.id_number,
            description = obj_in.description,
            address_uuid = commond_address_uuid,
            country_uuid = obj_in.country_uuid,
            city_uuid = obj_in.city_uuid,
            manager_uuid = commond_user_uuid,
            added_by = commond_user_uuid,
            logo_uuid = obj_in.logo_uuid
        )
        db.add(new_bibliotheque)
        db.commit()
        db.refresh(new_bibliotheque)
        return new_bibliotheque
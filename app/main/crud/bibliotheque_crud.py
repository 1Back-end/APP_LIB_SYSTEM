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
    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.BibliothequeUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="bibliotheque-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.phone_number = obj_in.phone_number if obj_in.phone_number else db_obj.phone_number
        db_obj.phone_number_2 = obj_in.phone_number_2 if obj_in.phone_number_2 else db_obj.phone_number_2
        db_obj.email = obj_in.email if obj_in.email else db_obj.email
        db_obj.id_number = obj_in.id_number if obj_in.id_number else db_obj
        db_obj.web_site = obj_in.web_site if obj_in.web_site else db_obj.web_site
        db_obj.description = obj_in.description if obj_in.description else db_obj.description
        db_obj.street = obj_in.street if obj_in.street else db_obj.street
        db_obj.state = obj_in.state if obj_in.state else db_obj.state
        db_obj.zipcode = obj_in.zipcode if obj_in.zipcode else db_obj.zipcode
        db_obj.city = obj_in.city if obj_in.city else db_obj.city
        db_obj.country = obj_in.country if obj_in.country else db_obj.country

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
        db_obj.country_uuid = obj_in.country_uuid if obj_in.country_uuid else db_obj.country_uuid,
        db_obj.city_uuid = obj_in.city_uuid if obj_in.city_uuid else db_obj.city_uuid,
        db_obj.manager_uuid = added_by,
        db_obj.added_by = added_by


    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="bibliotheque-not-found"))
        db.status = status
        db.commit()


    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="bibliotheque-not-found"))
        db.delete(db_obj)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="bibliotheque-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def get_all_data(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status : Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Bibliotheque).filter(models.Bibliotheque.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Bibliotheque.note.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Bibliotheque, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Bibliotheque, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Bibliotheque, order_field).desc())

        if status:
            record_query = record_query.filter(models.Bibliotheque.status == status)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.BibliothequeResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
import math
from datetime import datetime

import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_, false
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas


class CRUD_EMPRUNT(CRUDBase[models.Emprunt,schemas.EmpruntCreate,schemas.EmpruntUpdate]):

    @classmethod
    def get_by_uuid(cls,db: Session, uuid: str) -> Optional[models.Emprunt]:
        db.query(models.Emprunt).filter(models.Emprunt.uuid == uuid, models.Emprunt.is_deleted==False).first()


    @classmethod
    def create(cls, db:Session, obj_in: schemas.EmpruntCreate,added_by:str,user_uuid:str):
        db_obj = models.Emprunt(
            uuid=str(uuid.uuid4()),
            book_uuid=obj_in.book_uuid,
            note=obj_in.note,
            added_by=added_by,
            user_uuid=user_uuid,
            date_return = datetime.date.today() + datetime.timedelta(days=15)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    @classmethod
    def update(cls,db:Session,obj_in:schemas.EmpruntUpdate,added_by:str,user_uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="emprunt-not-found"))
        db_obj.book_uuid = obj_in.book_uuid if obj_in.book_uuid else db_obj.book_uuid
        db_obj.note = obj_in.note if obj_in.note else obj_in.note
        db_obj.added_by = added_by
        db_obj.user_uuid = user_uuid
        db_obj.date_return = datetime.date.today() + datetime.timedelta(days=15)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def delete(cls, db:Session, uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="emprunt-not-found"))
        db.delete(db_obj)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="emprunt-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="emprunt-not-found"))
        db_obj.status = status
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

        record_query = db.query(models.Emprunt).filter(models.Emprunt.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Emprunt.note.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Emprunt, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Emprunt, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Emprunt, order_field).desc())

        if status:
            record_query = record_query.filter(models.Emprunt.status == status)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.EmpruntResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )

    @classmethod
    def get_my_emprunts(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status: Optional[str] = None,
            user_uuid: Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Emprunt).filter(models.Emprunt.is_deleted == False,models.Emprunt.user_uuid==user_uuid)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Emprunt.note.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Emprunt, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Emprunt, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Emprunt, order_field).desc())

        if status:
            record_query = record_query.filter(models.Emprunt.status == status)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.EmpruntResponseListSlim(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


emprunt = CRUD_EMPRUNT(models.Emprunt)
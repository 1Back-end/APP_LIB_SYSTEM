import math
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


class CRUD_EMPRUNTS(CRUDBase[models.Emprunt,schemas.EmpruntCreate,schemas.EmpruntUpdate]):

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
    def update_status(cls,db:Session,uuid:str,status:bool):
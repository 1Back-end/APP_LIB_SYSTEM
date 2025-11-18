import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas


class CATEGORY_BOOK_CRUD(CRUDBase[models.CategoryBooks,schemas.CategoryBookSlim,schemas.CategoryBookCreate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str)->Optional[models.CategoryBooks]:
        return db.query(models.CategoryBooks).filter(models.CategoryBooks.uuid == uuid,models.CategoryBooks.is_deleted==False).first()


    @classmethod
    def get_by_name(cls,db:Session,name:str)->Optional[models.CategoryBooks]:
        return db.query(models.CategoryBooks).filter(models.CategoryBooks.name == name,models.CategoryBooks.is_deleted==False).first()

    @classmethod
    def delete(cls,db:Session,uuid:str)->Optional[models.CategoryBooks]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="category-book-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str)->Optional[models.CategoryBooks]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="category-book-not-found"))
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool)->Optional[models.CategoryBooks]:
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="category-book-not-found"))
        db_obj.is_active = is_active
        db.commit()

    @classmethod
    def create(cls,db:Session,obj_in:schemas.CategoryBookCreate,added_by:str)->Optional[models.CategoryBooks]:
        db_obj = models.CategoryBooks(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            description = obj_in.description,
            added_by = added_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(cls,db:Session,obj_in:schemas.CategoryBookUpdate,added_by:str)->Optional[models.CategoryBooks]:
        db_obj = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="category-book-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.description = obj_in.description if obj_in.description else db_obj.description
        db_obj.added_by = added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj

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

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.CategoryBooks).filter(models.CategoryBooks.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.CategoryBooks.name.ilike(f'%{keyword}%'),
                    models.CategoryBooks.description.ilike(f'%{keyword}%')
                )
            )


        if order and order_field and hasattr(models.CategoryBooks, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.CategoryBooks, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.CategoryBooks, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CategoryBookResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )



category_books = CATEGORY_BOOK_CRUD(models.CategoryBooks)
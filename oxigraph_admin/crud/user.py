import json
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from oxigraph_admin import schemas
from oxigraph_admin import models
from oxigraph_admin.crud.security import get_password_hash


class UserExistsError(HTTPException):
    @classmethod
    def message(cls, value: str) -> str:
        return f'The user "{value}" already exists.'


class UserNotFoundError(HTTPException):
    @classmethod
    def message(cls, value: str) -> str:
        return f'The user "{value}" was not found.'


def get_all(db: Session) -> List[models.User]:
    return db.query(models.User).all()


def create(user: schemas.UserCreate, db: Session) -> models.User:
    if get(user.username, db):
        raise UserExistsError(status_code=422, detail=UserExistsError.message(user.username))

    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, permissions=json.dumps(user.permissions))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get(username: str, db: Session) -> models.User:
    return db.query(models.User).filter_by(username=username).first()


def update(username: str, user: schemas.UserUpdate, db: Session) -> models.User:
    db_user = get(username, db)
    if not db_user:
        raise UserNotFoundError(status_code=404, detail=UserNotFoundError.message(username))

    updates = user.dict()
    if user.password:
        hashed_password = get_password_hash(user.password)
        updates['hashed_password'] = hashed_password
    updates.pop('password')
    for k, v in dict(updates).items():
        if v is None:
            updates.pop(k)

    db.query(models.User).update(updates)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete(username: str, db: Session):
    user = get(username, db)
    if not user:
        raise UserNotFoundError(status_code=404, detail=UserNotFoundError.message(username))
    db.delete(user)
    db.commit()

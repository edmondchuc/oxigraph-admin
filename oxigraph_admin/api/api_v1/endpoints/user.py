from http import HTTPStatus
from typing import List

from fastapi import Depends, Security
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from oxigraph_admin import schemas
from oxigraph_admin import models
from oxigraph_admin import crud
from oxigraph_admin.database import get_db

router = APIRouter()


@router.get('/users', response_model=List[schemas.UserRead])
def get_users(db: Session = Depends(get_db), user: models.User = Security(crud.auth.get_current_active_user, scopes=['user_management'])):
    return crud.user.get_all(db)


@router.get('/user/{username}', response_model=schemas.UserRead)
def get_user(username: str, db: Session = Depends(get_db)):
    user = crud.user.get(username, db)
    if user:
        return user
    return JSONResponse({'detail': f'User "{username}" not found.'}, status_code=404)


@router.post('/user', response_model=schemas.UserRead, status_code=HTTPStatus.CREATED)
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.user.create(user, db)


@router.put('/user/{username}', response_model=schemas.UserRead)
def put_user(user: schemas.UserUpdate, username: str, db: Session = Depends(get_db)):
    return crud.user.update(username, user, db)


@router.delete('/user/{username}')
def delete_user(username: str, db: Session = Depends(get_db)):
    crud.user.delete(username, db)
    return JSONResponse({'detail': f'User "{username}" has been deleted.'}, status_code=200)


@router.get('/user', response_model=schemas.UserRead)
def get(user: models.User = Security(crud.auth.get_current_active_user)):
    return user

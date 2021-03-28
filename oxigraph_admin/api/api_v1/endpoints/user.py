from http import HTTPStatus
from typing import List

from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse, Response

from oxigraph_admin.schemas.user import UserOut, UserIn, UserUpdate, UsersOut
from oxigraph_admin import crud

router = APIRouter()


@router.get('/users', response_model=UsersOut)
def get_users():
    users = crud.user.get_all()
    if users:
        return users
    else:
        return Response(status_code=HTTPStatus.NO_CONTENT)


@router.get('/user/{username}', response_model=UserOut)
def get_user(username: str):
    return crud.user.get_user(username)


@router.post('/user', response_model=UserOut, status_code=HTTPStatus.CREATED)
def post_user(user: UserIn):
    return crud.user.create_user(user)


@router.put('/user', response_model=UserOut)
def put_user(user: UserUpdate):
    return crud.user.update_user(user)


@router.delete('/user/{username}')
def delete_user(username: str):
    return crud.user.delete_user(username)

from http import HTTPStatus

from fastapi import HTTPException

from oxigraph_admin.schemas.user import UserIn, UserUpdate, UsersOut, UserRaw
from oxigraph_admin.crud.security import get_password_hash
from oxigraph_admin.store import store


def is_username_exist(username: str):
    for user in store.users:
        if user['username'] == username:
            return True
    return False


class UserExistsError(HTTPException):
    @classmethod
    def message(cls, value: str) -> str:
        return f'The user "{value}" already exists.'


class UserNotFoundError(HTTPException):
    @classmethod
    def message(cls, value: str) -> str:
        return f'The user "{value}" was not found.'


def get_all() -> UsersOut:
    users = [{'username': user['username'], 'permissions': user['permissions']} for user in store.users]
    return UsersOut(users=users)


def get_user(username: str) -> UserRaw:
    for user_ in store.users:
        if user_['username'] == username:
            return UserRaw(**dict(user_))
    raise UserNotFoundError(status_code=HTTPStatus.NOT_FOUND, detail=UserNotFoundError.message(username))


def create_user(user: UserIn) -> UserIn:
    if is_username_exist(user.username):
        raise UserExistsError(status_code=HTTPStatus.CONFLICT, detail=UserExistsError.message(user.username))
    else:
        password = user.password
        user_data = user.dict()
        del user_data['password']
        user_data['password_hash'] = get_password_hash(password)
        store.users += [user_data]
        return user


def update_user(user: UserUpdate) -> UserRaw:
    for i, user_ in enumerate(store.users):
        if user_['username'] == user.username:
            if user.password:
                password_hash = get_password_hash(user.password)
                del store['users', i]
                user_data = user.dict()
                user_data['password_hash'] = password_hash
                store.users += [user.dict()]
                return get_user(user.username)
            else:
                password_hash = user_['password_hash']
                del store['users', i]
                user_data = user.dict()
                user_data['password_hash'] = password_hash
                store.users += [user_data]
                return get_user(user.username)
    raise UserNotFoundError(status_code=HTTPStatus.NOT_FOUND, detail=UserNotFoundError.message(user.username))


def delete_user(username: str):
    for i, user in enumerate(store.users):
        if user['username'] == username:
            del store['users', i]
            return {'detail': f'Successfully deleted user "{username}.'}
    raise UserNotFoundError(status_code=HTTPStatus.NOT_FOUND, detail=UserNotFoundError.message(username))

from fastapi import HTTPException
from passlib.context import CryptContext

from oxigraph_admin.schemas.security import SecuritySettings
from oxigraph_admin.store import store
from oxigraph_admin import crud


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class UnauthorizedError(HTTPException):
    pass


def is_security_enabled() -> bool:
    return store.security['enabled']


def verify_login(username: str, password: str):
    from oxigraph_admin.crud.user import get_user
    user = get_user(username)
    if user:
        if verify_password(password, user.password_hash):
            return True
    return False


def verify_permissions(username: str, path: str):
    user = crud.user.get_user(username)
    if path.startswith(tuple(user.permissions)):
        return True
    return False


def get_security_settings():
    return SecuritySettings(**dict(store.security))


def set_security(security_settings: SecuritySettings):
    del store['security']
    store['security'] = security_settings.dict()

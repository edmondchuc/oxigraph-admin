from fastapi import HTTPException

from oxigraph_admin.schemas.security import SecuritySettings
from oxigraph_admin.store import store
from oxigraph_admin import crud


class UnauthorizedError(HTTPException):
    pass


def is_security_enabled() -> bool:
    return store.security['enabled']


# def verify_login(username: str, password: str):
#     from oxigraph_admin.crud.user import get
#     user = get(username)
#     if user:
#         if verify_password(password, user.password_hash):
#             return True
#     return False


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

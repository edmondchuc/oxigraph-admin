from datetime import datetime
from datetime import timedelta
from typing import Union, Optional

from fastapi import Depends, status, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from oxigraph_admin import crud, schemas
from oxigraph_admin import models
from oxigraph_admin import settings
from oxigraph_admin.database import get_db


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={
        'me': 'Read information about the current user.',
        'user_management': 'Management of users.'
    }
)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session) -> Union[models.User, bool]:
    user = crud.user.get(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.OXIGRAPH_SECRET_KEY, algorithm=settings.OXIGRAPH_JWT_ALGORITHM)
    return encoded_jwt


def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )

    try:
        payload = jwt.decode(token, settings.OXIGRAPH_SECRET_KEY, algorithms=settings.OXIGRAPH_JWT_ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
        token_scopes = payload.get('scopes', [])
        token_data = schemas.AccessTokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        import traceback
        traceback.print_exc()
        raise credential_exception

    user = crud.user.get(username, db)
    if user is None:
        raise credential_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not enough permissions.',
                headers={'WWW-Authenticate': authenticate_value}
            )
    return user


def get_current_active_user(user: models.User = Security(get_current_user, scopes=['me'])):
    if not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user.')
    return user

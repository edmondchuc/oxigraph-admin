from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from oxigraph_admin import crud
from oxigraph_admin import schemas
from oxigraph_admin.database import get_db
from oxigraph_admin import settings

router = APIRouter()


@router.post('/token', response_model=schemas.AccessToken)
def access_token_get(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.OXIGRAPH_OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.auth.create_access_token(
        data={'sub': user.username, 'scopes': user.permissions},
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

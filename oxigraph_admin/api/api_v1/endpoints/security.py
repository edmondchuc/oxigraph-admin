from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from oxigraph_admin import crud
from oxigraph_admin.schemas.security import SecuritySettings

router = APIRouter()


@router.get('/security', response_model=SecuritySettings)
def security_get():
    response = crud.security.get_security_settings()
    return response


@router.post('/security')
def security_post(security_settings: SecuritySettings):
    crud.security.set_security(security_settings)
    return JSONResponse({'detail': f'Security set to {security_settings.enabled}'})

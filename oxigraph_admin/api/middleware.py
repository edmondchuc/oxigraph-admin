from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from basicauth import decode

from oxigraph_admin.crud.security import is_security_enabled, verify_login, verify_permissions
from oxigraph_admin.crud.user import UserNotFoundError

NO_SECURITY = ('/docs', '/redoc', '/openapi.json')


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path: str = request.scope.get('path')
        if is_security_enabled() and not path.startswith(NO_SECURITY):
            auth = request.headers.get('authorization')
            if auth:
                username, password = decode(auth)
                try:
                    if verify_login(username, password) and verify_permissions(username, path):
                        return await call_next(request)
                    else:
                        return JSONResponse(content={'detail': 'Unauthorized.'}, status_code=HTTPStatus.UNAUTHORIZED)
                except UserNotFoundError as e:
                    return JSONResponse(content={'detail': 'Unauthorized.'}, status_code=HTTPStatus.UNAUTHORIZED)
            else:
                return JSONResponse(content={'detail': 'No credentials supplied.'}, status_code=HTTPStatus.UNAUTHORIZED)
        else:
            return await call_next(request)

from fastapi import APIRouter


from oxigraph_admin.api.api_v1.endpoints import user, sparql_protocol_service, security, auth

api_router_v1 = APIRouter()
api_router_v1.include_router(user.router, tags=['Users'])
api_router_v1.include_router(sparql_protocol_service.router, tags=['SPARQL Protocol Service'])
api_router_v1.include_router(security.router, tags=['Security'])
api_router_v1.include_router(auth.router, tags=['Authentication'])

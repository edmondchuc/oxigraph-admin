from fastapi import FastAPI

from oxigraph_admin.api import middleware
from oxigraph_admin.api import api_v1
from oxigraph_admin import settings


tags_metadata = [
    {
        'name': 'Security',
        'description': 'Manage security settings.'
    },
    {
        'name': 'Users',
        'description': 'Manage authentication and authorization for users.'
    },
    {
        'name': 'SPARQL Protocol Service',
        'description': 'Proxy endpoints to interface directly with Oxigraph Server, protected by the Security middleware.'
    }
]


def create_app():
    app = FastAPI(title='Oxigraph Admin API', openapi_tags=tags_metadata)

    app.include_router(api_v1.api.api_router_v1, prefix=settings.API_V1_STR)

    app.add_middleware(middleware.SecurityMiddleware)

    return app

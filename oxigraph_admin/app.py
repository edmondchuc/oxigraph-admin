import random
import datetime

from fastapi import FastAPI

from oxigraph_admin.api import middleware
from oxigraph_admin.api import api_v1
from oxigraph_admin import settings
from oxigraph_admin.database import Base, engine


tags_metadata = [
    {
        'name': 'Security',
        'description': 'Manage security settings.'
    },
    {
        'name': 'Authentication',
        'description': 'User authentication'
    },
    {
        'name': 'Users',
        'description': 'Manage authorization for users.'
    },
    {
        'name': 'SPARQL Protocol Service',
        'description': 'Proxy endpoints to interface directly with Oxigraph Server, protected by the Security middleware.'
    }
]


def create_app():
    app = FastAPI(title='Oxigraph Admin API', openapi_tags=tags_metadata)

    app.include_router(api_v1.api.api_router_v1, prefix=settings.API_V1_STR)

    # Use SQLAlchemy to create SQLite database.
    Base.metadata.create_all(bind=engine)

    return app

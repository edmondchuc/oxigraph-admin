from os import environ

from dotenv import load_dotenv

load_dotenv()

# Oxigraph Admin
OXIGRAPH_STORE_FILE = environ.get('OXIGRAPH_STORE_FILE', 'data.json')
OXIGRAPH_SERVER_URL = environ.get('OXIGRAPH_SERVER_URL', 'http://localhost:7878')
API_V1_STR = environ.get('API_V1_STR', '/api/v1')

# SQLAlchemy
SQLALCHEMY_DATABASE_URL = environ.get('SQLALCHEMY_DATABASE_URL ', 'sqlite:///./store.db')

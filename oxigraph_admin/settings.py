from os import environ
from secrets import token_bytes
from base64 import b64encode

from dotenv import load_dotenv

load_dotenv()


# Oxigraph Admin
OXIGRAPH_STORE_FILE = environ.get('OXIGRAPH_STORE_FILE', 'data.json')
OXIGRAPH_SERVER_URL = environ.get('OXIGRAPH_SERVER_URL', 'http://localhost:7878')
API_V1_STR = environ.get('API_V1_STR', '/api/v1')


# Oxigraph Admin Security
# secret_key = b64encode((token_bytes(32))).decode('utf-8')
OXIGRAPH_SECRET_KEY = environ.get('OXIGRAPH_SECRET_KEY', 'bkng2zJttKirIGZHQTXXA1Xgaixpgz1l+XhWphfvs28=')
OXIGRAPH_JWT_ALGORITHM = environ.get('OXIGRAPH_JWT_ALGORITHM', 'HS256')
OXIGRAPH_OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES = environ.get('OXIGRAPH_OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES', 30)


# SQLAlchemy
SQLALCHEMY_DATABASE_URL = environ.get('SQLALCHEMY_DATABASE_URL ', 'sqlite:///./store.db')

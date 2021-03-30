from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from oxigraph_admin import settings

Base = declarative_base()

# check_same_thread = False only required for SQLite.
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

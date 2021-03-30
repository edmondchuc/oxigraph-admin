from sqlalchemy import Column, Integer, Text, Boolean

from oxigraph_admin.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, index=True)
    hashed_password = Column(Text)
    permissions = Column(Text)
    is_active = Column(Boolean, default=True)

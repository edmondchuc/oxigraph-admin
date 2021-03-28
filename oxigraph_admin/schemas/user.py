from typing import List, Sequence

from pydantic import BaseModel


class Permissions(BaseModel):
    permissions: Sequence[str]


class UserIn(Permissions):
    username: str
    password: str


class UserOut(Permissions):
    username: str


class UserUpdate(Permissions):
    username: str
    password: str = None


class UserRaw(Permissions):
    username: str
    password_hash: str


class UsersOut(BaseModel):
    users: List[UserOut]

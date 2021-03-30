from typing import List, Optional

from pydantic import BaseModel, Json


class UserBase(BaseModel):
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    permissions: List[str] = ['query']


class UserRead(UserBase):
    permissions: Json[List[str]]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    permissions: Optional[List[str]]
    is_active: Optional[bool]



# class Permissions(BaseModel):
#     permissions: Sequence[str]


# class UserIn(Permissions):
#     username: str
#     password: str
#
#
# class UserOut(Permissions):
#     username: str
#
#
# class UserUpdate(Permissions):
#     username: str
#     password: str = None
#
#
# class UserRaw(Permissions):
#     username: str
#     password_hash: str
#
#
# class UsersOut(BaseModel):
#     users: List[UserOut]

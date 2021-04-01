from typing import Optional, List

from pydantic import BaseModel, Json


class SecuritySettings(BaseModel):
    enabled: bool


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class AccessTokenData(BaseModel):
    username: Optional[str] = None
    scopes: Json[List[str]] = []

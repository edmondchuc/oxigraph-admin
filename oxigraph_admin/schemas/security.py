from pydantic import BaseModel


class SecuritySettings(BaseModel):
    enabled: bool

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str
    token_type: str
    jti: str | None = None


class TokenRefreshRequest(BaseModel):
    refresh_token: str

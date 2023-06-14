from pydantic import BaseModel


class AuthSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccountSchema(BaseModel):
    id: int
    username: str
    password: str
    role_id: str

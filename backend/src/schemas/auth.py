from pydantic import BaseModel


class AuthBase(BaseModel):
    username: str
    password: str


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str


class AccountBase(BaseModel):
    username: str
    password: str
    role_id: str

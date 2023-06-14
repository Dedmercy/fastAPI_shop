from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    username: str
    password: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr
    phone: str


class AccountCreateSchema(BaseModel):
    username: str
    password: str
    role_id: int


class PersonalDataCreateSchema(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr
    phone: str


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]


class AccountUpdateSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]


class PersonalDataUpdateSchema(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]



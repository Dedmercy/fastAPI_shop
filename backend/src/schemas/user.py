from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreateBase(BaseModel):
    username: str
    password: str
    role_id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr
    phone: str


class AccountCreateBase(BaseModel):
    username: str
    password: str
    role_id: int


class PersonalDataCreateBase(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr
    phone: str


class UserUpdateBase(BaseModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]


class AccountUpdateBase(BaseModel):
    username: Optional[str]
    password: Optional[str]


class PersonalDataUpdateBase(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]



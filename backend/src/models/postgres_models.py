from typing import List

from sqlalchemy import String, MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from typing_extensions import Annotated

str_50 = Annotated[str, 50]
str_25 = Annotated[str, 25]
phone = Annotated[str, 11]


class Base(DeclarativeBase):
    metadata = MetaData()
    type_annotation_map = {
        str_50: String().with_variant(String(50), "postgresql"),
        str_25: String().with_variant(String(25), "postgresql"),
        str: String().with_variant(String(255), "postgresql"),
        phone: String().with_variant(String(11), "postgresql")
    }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    accounts: Mapped[List["Account"]] = relationship(back_populates="role")


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str_25] = mapped_column(unique=True)
    password: Mapped[str]

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="accounts")
    personal_data: Mapped["PersonalData"] = relationship(back_populates="account")


class PersonalData(Base):
    __tablename__ = "personal_data"

    id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)
    account: Mapped["Account"] = relationship(back_populates="personal_data")

    first_name: Mapped[str_50]
    middle_name: Mapped[str_50 | None]
    last_name: Mapped[str_50]

    email: Mapped[str_50]
    phone: Mapped[phone]



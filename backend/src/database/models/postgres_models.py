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

    role_account: Mapped[List["Account"]] = relationship(back_populates="account_role")


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str_25] = mapped_column(unique=True)
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    account_role: Mapped["Role"] = relationship(back_populates="role_account")
    account_pd: Mapped["PersonalData"] = relationship(back_populates="pd_account")
    account_cart: Mapped["Cart"] = relationship(back_populates="cart_account")


class PersonalData(Base):
    __tablename__ = "personal_data"

    id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)

    first_name: Mapped[str_50]
    middle_name: Mapped[str_50 | None]
    last_name: Mapped[str_50]
    email: Mapped[str_50] = mapped_column(unique=True)
    phone: Mapped[phone]

    pd_account: Mapped["Account"] = relationship(back_populates="account_pd")


class Cart(Base):
    __tablename__ = 'cart'

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)
    product_id: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(default=1)

    cart_account: Mapped["Account"] = relationship(back_populates="account_cart")


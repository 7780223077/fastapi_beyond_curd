from enum import Enum
import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg


class RoleEnum(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        )
    ) 
    username: str
    email: str
    password: str = Field(exclude=True)
    first_name: str 
    last_name: str
    role: RoleEnum = Field(sa_column=Column(pg.ENUM(RoleEnum, name="RoleEnum", create_type=True), nullable=False, default=RoleEnum.USER, server_default=RoleEnum.USER.value))
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))

    def __repr__(self):
        return f"User(uid={self.uid}, username='{self.username}', email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}', is_verified={self.is_verified}, created_at={self.created_at}, updated_at={self.updated_at})"
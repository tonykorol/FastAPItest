from typing import List

from pydantic import BaseModel, Field, EmailStr
from app.schemas.events import EventSchema


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    email: EmailStr = Field(..., max_length=254)


class UserSchema(UserBaseSchema):
    id: int
    is_admin: bool
    events: List[EventSchema]


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=50)


class UserCredentialsSchema(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    password: str = Field(..., min_length=8, max_length=50)


class AllUsersSchema(BaseModel):
    users: list


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPairSchema(AccessTokenSchema, RefreshTokenSchema):
    pass

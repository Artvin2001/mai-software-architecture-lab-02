from enum import Enum

from pydantic import BaseModel, ConfigDict


class AccessRights(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    MODERATOR = 'MODERATOR'


class UserModel(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    patronymic: str
    access_rights: AccessRights

    model_config = ConfigDict(from_attributes=True)


class CreateUserModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    patronymic: str
    access_rights: AccessRights

    model_config = ConfigDict(from_attributes=True)

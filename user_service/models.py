from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AccessRights(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    MODERATOR = 'MODERATOR'


class UserModel(BaseModel):
    uuid: UUID
    email: str
    first_name: str
    last_name: str
    patronymic: str | None
    access_rights: AccessRights

    model_config = ConfigDict(from_attributes=True)


class CreateUserModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    patronymic: str
    access_rights: AccessRights

    model_config = ConfigDict(from_attributes=True)

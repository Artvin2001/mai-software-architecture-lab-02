from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class AccessRights(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    MODERATOR = 'MODERATOR'


class ConferenceModel(BaseModel):
    id: int
    title: str
    date: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateConferenceModel(BaseModel):
    title: str
    date: datetime

    model_config = ConfigDict(from_attributes=True)

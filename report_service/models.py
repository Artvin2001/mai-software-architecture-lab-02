from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class AccessRights(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    MODERATOR = 'MODERATOR'


class ReportModel(BaseModel):
    id: int
    title: str
    annotation: str
    text: str
    creation_date: datetime
    update_date: datetime | None
    moderation_flag: bool
    user_id: int
    conference_id: int | None

    model_config = ConfigDict(from_attributes=True)


class CreateReportModel(BaseModel):
    title: str
    annotation: str
    text: str
    moderation_flag: bool
    user_id: int
    conference_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

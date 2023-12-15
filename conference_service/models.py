from enum import Enum


class AccessRights(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    MODERATOR = 'MODERATOR'

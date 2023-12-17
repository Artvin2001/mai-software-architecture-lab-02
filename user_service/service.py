from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status

from database import Session_1, Session_2, UserTable, get_session_1, get_session_2
from models import CreateUserModel, UserModel


class Service:
    def __init__(self, session_1: Session_1 = Depends(get_session_1), session_2: Session_2 = Depends(get_session_2)):
        self.__session_1: Session_1 = session_1
        self.__session_2: Session_2 = session_2

    def create_user(self, model: CreateUserModel) -> UserModel:
        user = self.__session_1.query(UserTable).filter(UserTable.email == model.email).scalar()
        if user is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, f'User with email {model.email} already exists.')
        user = self.__session_2.query(UserTable).filter(UserTable.email == model.email).scalar()
        if user is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, f'User with email {model.email} already exists.')

        uuid = uuid4()
        session = self.__session_1 if int(uuid) % 2 else self.__session_2
        user = UserTable(
            uuid=uuid,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            access_rights=model.access_rights,
        )
        session.add(user)
        session.commit()
        return user

    def get_user_by_uuid(self, user_uuid: UUID) -> UserModel:
        session = self.__session_1 if int(user_uuid) % 2 else self.__session_2
        user = session.query(UserTable).get(user_uuid)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f'User with uuid {user_uuid} not found.')
        return user

    def get_user_by_email(self, email: str) -> UserModel:
        user = self.__session_1.query(UserTable).filter(UserTable.email == email).scalar()
        if user is None:
            user = self.__session_2.query(UserTable).filter(UserTable.email == email).scalar()
            if user is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f'User with email {email} not found.')
        return user

    def update_user(self, user_uuid: UUID, model: CreateUserModel) -> UserModel:
        user = self.get_user_by_uuid(user_uuid)

        if self.get_user_by_email(model.email) is not None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f'User with email {model.email} already exists.',
            )

        user.email = model.email
        user.first_name = model.first_name
        user.last_name = model.last_name
        user.patronymic = model.patronymic
        user.access_rights = model.access_rights

        session = self.__session_1 if int(user_uuid) % 2 else self.__session_2
        session.commit()
        return user

    def delete_user(self, user_uuid: UUID) -> None:
        user = self.get_user_by_uuid(user_uuid)
        session = self.__session_1 if int(user_uuid) % 2 else self.__session_2
        session.delete(user)
        session.commit()

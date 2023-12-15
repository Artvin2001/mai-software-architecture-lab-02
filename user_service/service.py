from fastapi import Depends, HTTPException, status

from models import CreateUserModel, UserModel
from database import Session, UserTable, get_session


class Service:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session: Session = session

    def create_user(self, model: CreateUserModel) -> UserModel:
        user = self.__session.query(UserTable).filter(UserTable.email == model.email).scalar()
        if user is not None:
            HTTPException(status.HTTP_409_CONFLICT, f"User with email {model.email} already exists.")
        user = UserTable(
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            access_rights=model.access_rights,
        )
        self.__session.add(user)
        self.__session.commit()
        return user

    def get_user_by_id(self, user_id: int) -> UserModel:
        user = self.__session.query(UserTable).get(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {user_id} not found.")
        return user

    def get_user_by_email(self, email: str) -> UserModel:
        user = self.__session.query(UserTable).filter(UserTable.email == email).scalar()
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with email {email} not found.")
        return user

    def update_user(self, user_id: int, model: CreateUserModel) -> UserModel:
        user = self.__session.query(UserTable).get(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {user_id} not found.")
        user.email = model.email
        user.first_name = model.first_name
        user.last_name = model.last_name
        user.patronymic = model.patronymic
        user.access_rights = model.access_rights
        self.__session.commit()
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.__session.query(UserTable).get(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {user_id} not found.")
        self.__session.delete(user)
        self.__session.commit()

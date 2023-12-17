from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from models import CreateUserModel, UserModel
from service import Service

router = APIRouter(
    prefix='/users',
    tags=['Пользователи'],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel,
    summary="Создание нового пользователя.",
)
def create_user_endpoint(model: CreateUserModel, service: Service = Depends()) -> UserModel:
    return service.create_user(model)


@router.get(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Получение пользователя по идентификатору.",
)
def get_user_by_id_endpoint(user_uuid: UUID, service: Service = Depends()) -> UserModel:
    return service.get_user_by_uuid(user_uuid)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Получение пользователя по электронной почте.",
)
def get_user_by_email_endpoint(email: str, service: Service = Depends()) -> UserModel:
    return service.get_user_by_email(email)


@router.put(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Редактирование пользователя.",
)
def update_user_endpoint(user_uuid: UUID, model: CreateUserModel, service: Service = Depends()) -> UserModel:
    return service.update_user(user_uuid, model)


@router.delete(
    "/{user_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Удаление пользователя.",
)
def delete_user_by_uuid_endpoint(user_uuid: UUID, service: Service = Depends()) -> None:
    return service.delete_user(user_uuid)

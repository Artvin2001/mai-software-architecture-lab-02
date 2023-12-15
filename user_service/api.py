from fastapi import APIRouter, Depends, status, Response

from models import CreateUserModel, UserModel
from service import Service

router = APIRouter(
    prefix='/user',
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
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Получение пользователя по идентификатору.",
)
def get_user_by_id_endpoint(user_id: int, service: Service = Depends()) -> UserModel:
    return service.get_user_by_id(user_id)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Получение пользователя по электронной почте.",
)
def get_user_by_email_endpoint(email: str, service: Service = Depends()) -> UserModel:
    return service.get_user_by_email(email)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Редактирование пользователя.",
)
def update_user_endpoint(user_id: int, model: CreateUserModel, service: Service = Depends()) -> UserModel:
    return service.update_user(user_id, model)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Удаление пользователя.",
)
def delete_user_by_id_endpoint(user_id: int, service: Service = Depends()) -> None:
    return service.delete_user(user_id)

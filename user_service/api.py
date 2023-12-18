import json
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from fastapi.requests import Request

from models import CreateUserModel, UserModel
from service import Service

router = APIRouter(
    prefix='/users',
    tags=['Пользователи'],
)

TTL = 60


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel,
    summary="Создание нового пользователя.",
)
def create_user_endpoint(
        request: Request,
        model: CreateUserModel,
        service: Service = Depends(),
) -> UserModel:
    data = service.create_user(model)
    request.app.state.redis.setex(str(data.uuid), TTL, UserModel(**data.__dict__).model_dump_json())
    return data


@router.get(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=UserModel,
    summary="Получение пользователя по идентификатору.",
)
def get_user_by_id_endpoint(request: Request, user_uuid: UUID, service: Service = Depends()) -> UserModel:
    cached = request.app.state.redis.get(str(user_uuid))
    if cached:
        return UserModel.model_validate(json.loads(cached.decode("utf8")))

    data = service.get_user_by_uuid(user_uuid)
    request.app.state.redis.setex(str(user_uuid), TTL, UserModel(**data.__dict__).model_dump_json())
    return data


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
def update_user_endpoint(
        request: Request,
        user_uuid: UUID,
        model: CreateUserModel,
        service: Service = Depends(),
) -> UserModel:
    data = service.update_user(user_uuid, model)
    request.app.state.redis.setex(
        str(user_uuid),
        TTL,
        UserModel(**model.model_dump(), uuid=user_uuid).model_dump_json(),
    )
    return data


@router.delete(
    "/{user_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Удаление пользователя.",
)
def delete_user_by_uuid_endpoint(
        request: Request,
        user_uuid: UUID,
        service: Service = Depends(),
) -> None:
    service.delete_user(user_uuid)
    request.app.state.redis.delete(str(user_uuid))


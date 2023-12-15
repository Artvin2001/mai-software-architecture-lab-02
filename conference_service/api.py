from fastapi import APIRouter, Depends, Response, status

from models import CreateConferenceModel, ConferenceModel
from service import Service

router = APIRouter(
    prefix='/conferences',
    tags=['Конференции'],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ConferenceModel,
    summary="Создание конференции.",
)
def create_conference_endpoint(model: CreateConferenceModel, service: Service = Depends()) -> ConferenceModel:
    return service.create_conference(model)


@router.get(
    "/{conference_id}",
    status_code=status.HTTP_200_OK,
    response_model=ConferenceModel,
    summary="Получение конференции по идентификатору.",
)
def get_conference_by_id_endpoint(conference_id: int, service: Service = Depends()) -> ConferenceModel:
    return service.get_conference_by_id(conference_id)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ConferenceModel],
    summary="Получение всех конференций.",
)
def get_all_conferences_endpoint(service: Service = Depends()) -> list[ConferenceModel]:
    return service.get_all_conferences()


@router.put(
    "/{conference_id}",
    status_code=status.HTTP_200_OK,
    response_model=ConferenceModel,
    summary="Редактирование конференции.",
)
def update_conference_endpoint(
        conference_id: int,
        model: CreateConferenceModel,
        service: Service = Depends(),
) -> ConferenceModel:
    return service.update_conference(conference_id, model)


@router.delete(
    "/{conference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Удаление конференции.",
)
def delete_conference_by_id_endpoint(conference_id: int, service: Service = Depends()) -> None:
    return service.delete_conference(conference_id)

from fastapi import APIRouter, Depends, status, Response

from models import CreateReportModel, ReportModel
from service import Service

router = APIRouter(
    prefix='/reports',
    tags=['Доклады'],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReportModel,
    summary="Создание доклада.",
)
def create_report_endpoint(model: CreateReportModel, service: Service = Depends()) -> ReportModel:
    return service.create_report(model)


@router.get(
    "/{report_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReportModel,
    summary="Получение доклада по идентификатору.",
)
def get_report_by_id_endpoint(report_id: int, service: Service = Depends()) -> ReportModel:
    return service.get_report_by_id(report_id)


# ВСТАВИТЬ ЕЩЕ ОДИН

@router.put(
    "/{report_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReportModel,
    summary="Редактирование доклада.",
)
def update_report_endpoint(report_id: int, model: CreateReportModel, service: Service = Depends()) -> ReportModel:
    return service.update_report(report_id, model)


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Удаление доклада.",
)
def delete_report_by_id_endpoint(report_id: int, service: Service = Depends()) -> None:
    return service.delete_report(report_id)

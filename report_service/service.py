from re import compile, error
from datetime import datetime

from fastapi import Depends, HTTPException, status

from database import ConferenceTable, ReportTable, Session_1, Session_2, UserTable, get_session_1, get_session_2
from models import CreateReportModel, ReportModel


class Service:
    def __init__(self, session_1: Session_1 = Depends(get_session_1), session_2: Session_2 = Depends(get_session_2)):
        self.__session_1: Session_1 = session_1
        self.__session_2: Session_2 = session_2

    def create_report(self, model: CreateReportModel) -> ReportModel:
        self.__check_user_and_conference(model)

        report = ReportTable(
            title=model.title,
            annotation=model.annotation,
            text=model.text,
            moderation_flag=model.moderation_flag,
            user_uuid=model.user_uuid,
            conference_id=model.conference_id,
        )
        self.__session_1.add(report)
        self.__session_1.commit()
        return report

    def get_report_by_id(self, report_id: int) -> ReportModel:
        user = self.__session_1.query(ReportTable).get(report_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f'Report with id {report_id} not found.')
        return user

    def get_report_by_title_regex(self, report_title_regex: str) -> list[ReportModel]:
        try:
            compile(report_title_regex)
        except error:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f'Regular expression `{report_title_regex}` is incorrect.',
            )

        return self.__session_1.query(ReportTable).filter(ReportTable.title.op('regexp')(report_title_regex))

    def update_report(self, report_id: int, model: CreateReportModel) -> ReportModel:
        report = self.get_report_by_id(report_id)

        self.__check_user_and_conference(model)

        report.title = model.title
        report.annotation = model.annotation
        report.text = model.text
        report.update_date = datetime.now()
        report.moderation_flag = model.moderation_flag
        report.user_uuid = model.user_uuid
        report.conference_id = model.conference_id

        self.__session_1.commit()
        return report

    def delete_report(self, report_id: int) -> None:
        report = self.get_report_by_id(report_id)
        self.__session_1.delete(report)
        self.__session_1.commit()

    def __check_user_and_conference(self, model: CreateReportModel) -> None:
        session = self.__session_1 if int(model.user_uuid) % 2 else self.__session_2
        if session.query(UserTable).get(model.user_uuid) is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'User with uuid {model.user_uuid} not found.')
        if model.conference_id is not None and self.__session_1.query(ConferenceTable).get(model.conference_id) is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f'Conference with id {model.conference_id} not found.',
            )

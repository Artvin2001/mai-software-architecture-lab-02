from re import compile, error
from datetime import datetime

from fastapi import Depends, HTTPException, status

from database import ConferenceTable, ReportTable, Session, UserTable, get_session
from models import CreateReportModel, ReportModel


class Service:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session: Session = session

    def create_report(self, model: CreateReportModel) -> ReportModel:
        self.__check_user_and_conference(model)

        report = ReportTable(
            title=model.title,
            annotation=model.annotation,
            text=model.text,
            moderation_flag=model.moderation_flag,
            user_id=model.user_id,
            conference_id=model.conference_id,
        )
        self.__session.add(report)
        self.__session.commit()
        return report

    def get_report_by_id(self, report_id: int) -> ReportModel:
        user = self.__session.query(ReportTable).get(report_id)
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

        return self.__session.query(ReportTable).filter(ReportTable.title.op('regexp')(report_title_regex))

    def update_report(self, report_id: int, model: CreateReportModel) -> ReportModel:
        report = self.get_report_by_id(report_id)

        self.__check_user_and_conference(model)

        report.title = model.title
        report.annotation = model.annotation
        report.text = model.text
        report.update_date = datetime.now()
        report.moderation_flag = model.moderation_flag
        report.user_id = model.user_id
        report.conference_id = model.conference_id

        self.__session.commit()
        return report

    def delete_report(self, report_id: int) -> None:
        report = self.get_report_by_id(report_id)
        self.__session.delete(report)
        self.__session.commit()

    def __check_user_and_conference(self, model: CreateReportModel) -> None:
        if self.__session.query(UserTable).get(model.user_id) is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'User with id {model.user_id} not found.')
        if model.conference_id is not None and self.__session.query(ConferenceTable).get(model.conference_id) is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f'Conference with id {model.conference_id} not found.',
            )

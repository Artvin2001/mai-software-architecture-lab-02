from fastapi import Depends, HTTPException, status

from database import ConferenceTable, Session, get_session
from models import CreateConferenceModel, ConferenceModel


class Service:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session: Session = session

    def create_conference(self, model: CreateConferenceModel) -> ConferenceModel:
        conference = ConferenceTable(
            title=model.title,
            date=model.date,
        )
        self.__session.add(conference)
        self.__session.commit()
        return conference

    def get_conference_by_id(self, conference_id: int) -> ConferenceModel:
        conference = self.__session.query(ConferenceTable).get(conference_id)
        if conference is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f'Conference with id {conference_id} not found.')
        return conference

    def get_all_conferences(self) -> list[ConferenceModel]:
        return self.__session.query(ConferenceTable).all()

    def update_conference(self, conference_id: int, model: CreateConferenceModel) -> ConferenceModel:
        conference = self.get_conference_by_id(conference_id)

        conference.title = model.title
        conference.date = model.date

        self.__session.commit()
        return conference

    def delete_conference(self, conference_id: int) -> None:
        conference = self.get_conference_by_id(conference_id)
        self.__session.delete(conference)
        self.__session.commit()

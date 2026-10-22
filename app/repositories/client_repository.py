from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:

    def get_all(
        self,
        db: Session,
        advisor_id: int
    ):
        return (
            db.query(Client)
            .filter(Client.advisor_id == advisor_id)
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        client_id: int
    ):
        return (
            db.query(Client)
            .filter(Client.id == client_id)
            .first()
        )

    def create(
        self,
        db: Session,
        client: Client
    ):
        try:
            db.add(client)
            db.commit()
            db.refresh(client)

            return client

        except IntegrityError:
            db.rollback()
            raise
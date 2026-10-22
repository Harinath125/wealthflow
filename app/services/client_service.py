from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.user import User
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate


class ClientService:

    def __init__(self):
        self.repository = ClientRepository()

    def get_clients(
        self,
        db: Session,
        advisor_id: int
    ):
        return self.repository.get_all(
            db,
            advisor_id
        )

    def create_client(
        self,
        db: Session,
        client_data: ClientCreate,
        current_user: User
    ):
        new_client = Client(
            advisor_id=current_user.id,
            name=client_data.name,
            email=client_data.email,
            phone=client_data.phone
        )

        return self.repository.create(
            db,
            new_client
        )
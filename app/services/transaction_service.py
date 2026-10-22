from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.client_repository import ClientRepository

from app.schemas.transaction import TransactionCreate

from app.exceptions.exceptions import (
    ResourceNotFoundException,
    ForbiddenException
)


class TransactionService:

    def __init__(self):
        self.repository = TransactionRepository()
        self.portfolio_repository = PortfolioRepository()
        self.client_repository = ClientRepository()

    def create_transaction(
        self,
        db: Session,
        transaction_data: TransactionCreate,
        current_user: User
    ):
        portfolio = self.portfolio_repository.get_by_id(
            db,
            transaction_data.portfolio_id
        )

        if portfolio is None:
            raise ResourceNotFoundException(
                "Portfolio not found"
            )

        client = self.client_repository.get_by_id(
            db,
            portfolio.client_id
        )

        if client is None:
            raise ResourceNotFoundException(
                "Client not found"
            )

        if client.advisor_id != current_user.id:
            raise ForbiddenException(
                "You do not have access to this portfolio"
            )

        new_transaction = Transaction(
            portfolio_id=transaction_data.portfolio_id,
            asset_symbol=transaction_data.asset_symbol,
            transaction_type=transaction_data.transaction_type,
            quantity=transaction_data.quantity,
            price=transaction_data.price
        )

        return self.repository.create(
            db,
            new_transaction
        )

    def get_transaction(
        self,
        db: Session,
        transaction_id: int,
        current_user: User
    ):
        transaction = self.repository.get_by_id(
            db,
            transaction_id
        )

        if transaction is None:
            raise ResourceNotFoundException(
                "Transaction not found"
            )

        portfolio = self.portfolio_repository.get_by_id(
            db,
            transaction.portfolio_id
        )

        if portfolio is None:
            raise ResourceNotFoundException(
                "Portfolio not found"
            )

        client = self.client_repository.get_by_id(
            db,
            portfolio.client_id
        )

        if client is None:
            raise ResourceNotFoundException(
                "Client not found"
            )

        if client.advisor_id != current_user.id:
            raise ForbiddenException(
                "You do not have access to this transaction"
            )

        return transaction
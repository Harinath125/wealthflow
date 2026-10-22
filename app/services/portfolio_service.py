import logging

from collections import defaultdict
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.models.user import User

from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.client_repository import ClientRepository
from app.repositories.transaction_repository import TransactionRepository

from app.schemas.portfolio import PortfolioCreate

from app.exceptions.exceptions import (
    ResourceNotFoundException,
    ForbiddenException
)


logger = logging.getLogger(__name__)

class PortfolioService:

    def __init__(self):
        self.repository = PortfolioRepository()
        self.client_repository = ClientRepository()
        self.transaction_repository = TransactionRepository()

    def get_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        current_user: User
    ):
        portfolio = self.repository.get_by_id(
            db,
            portfolio_id
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
            logger.warning(
        "Unauthorized portfolio access attempt: "
        "portfolio_id=%s advisor_id=%s owner_id=%s",
        portfolio_id,
        current_user.id,
        client.advisor_id
    )

            raise ForbiddenException(
        "You do not have access to this portfolio"
    )    

        return portfolio

    def create_portfolio(
        self,
        db: Session,
        portfolio_data: PortfolioCreate,
        current_user: User
    ):
        client = self.client_repository.get_by_id(
            db,
            portfolio_data.client_id
        )

        if client is None:
            raise ResourceNotFoundException(
        "Client not found"
    )

        if client.advisor_id != current_user.id:
            raise ForbiddenException(
    "You do not have access to this client"
)

        new_portfolio = Portfolio(
            client_id=portfolio_data.client_id,
            name=portfolio_data.name
        )

        portfolio = self.repository.create(
            db,
            new_portfolio
        )
        logger.info(
    "Portfolio created: portfolio_id=%s client_id=%s advisor_id=%s",
    portfolio.id,
    portfolio.client_id,
    current_user.id
)

        return portfolio

    def get_summary(
        self,
        db: Session,
        portfolio_id: int,
        current_user: User
    ):
        # --------------------------------
        # 1. Verify portfolio ownership
        # --------------------------------
        portfolio = self.get_portfolio(
            db,
            portfolio_id,
            current_user
        )

        # --------------------------------
        # 2. Get all transactions
        # --------------------------------
        transactions = (
            self.transaction_repository
            .get_by_portfolio_id(
                db,
                portfolio.id
            )
        )

        # --------------------------------
        # 3. Calculate holdings
        # --------------------------------
        holdings = defaultdict(
            lambda: {
                "quantity": Decimal("0"),
                "invested_amount": Decimal("0")
            }
        )

        for transaction in transactions:

            symbol = transaction.asset_symbol

            if transaction.transaction_type == "BUY":

                holdings[symbol]["quantity"] += (
                    transaction.quantity
                )

                holdings[symbol]["invested_amount"] += (
                    transaction.quantity
                    * transaction.price
                )

            elif transaction.transaction_type == "SELL":

                holdings[symbol]["quantity"] -= (
                    transaction.quantity
                )

                holdings[symbol]["invested_amount"] -= (
                    transaction.quantity
                    * transaction.price
                )

        # --------------------------------
        # 4. Remove fully sold holdings
        # --------------------------------
        holdings = {
            symbol: data
            for symbol, data in holdings.items()
            if data["quantity"] > 0
        }

        # --------------------------------
        # 5. Calculate total invested
        # --------------------------------
        total_invested = sum(
            data["invested_amount"]
            for data in holdings.values()
        )

        # --------------------------------
        # 6. Build response
        # --------------------------------
        holding_response = [
            {
                "asset_symbol": symbol,
                "quantity": data["quantity"],
                "invested_amount": data["invested_amount"]
            }
            for symbol, data in holdings.items()
        ]
        logger.info(
    "Generating portfolio summary: portfolio_id=%s advisor_id=%s",
    portfolio.id,
    current_user.id
)
        return {
            "portfolio_id": portfolio.id,
            "total_invested": total_invested,
            "holdings": holding_response
        }
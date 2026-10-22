from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio


class PortfolioRepository:

    def get_by_id(self, db: Session, portfolio_id: int):
        return (
            db.query(Portfolio)
            .filter(Portfolio.id == portfolio_id)
            .first()
        )

    def create(self, db: Session, portfolio: Portfolio):
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

        return portfolio
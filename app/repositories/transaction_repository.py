from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:

    def create(
        self,
        db: Session,
        transaction: Transaction
    ):
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    def get_by_id(
        self,
        db: Session,
        transaction_id: int
    ):
        return (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

    def get_by_portfolio_id(
        self,
        db: Session,
        portfolio_id: int
    ):
        return (
            db.query(Transaction)
            .filter(
                Transaction.portfolio_id == portfolio_id
            )
            .order_by(Transaction.transaction_time)
            .all()
        )
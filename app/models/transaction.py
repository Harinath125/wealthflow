from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False
    )

    asset_symbol = Column(String(20), nullable=False)
    transaction_type = Column(String(10), nullable=False)

    quantity = Column(Numeric(18, 4), nullable=False)
    price = Column(Numeric(18, 2), nullable=False)

    transaction_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    portfolio = relationship(
        "Portfolio",
        back_populates="transactions"
    )
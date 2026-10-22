from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    name = Column(String(150), nullable=False)

    client = relationship("Client", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio")
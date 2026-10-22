from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    portfolio_id: int
    asset_symbol: str
    transaction_type: Literal["BUY", "SELL"]
    quantity: Decimal = Field(gt=0)
    price: Decimal = Field(gt=0)


class TransactionResponse(BaseModel):
    id: int
    portfolio_id: int
    asset_symbol: str
    transaction_type: str
    quantity: Decimal
    price: Decimal
    transaction_time: datetime

    model_config = ConfigDict(from_attributes=True)
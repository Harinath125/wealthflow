from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PortfolioCreate(BaseModel):
    client_id: int
    name: str


class PortfolioResponse(BaseModel):
    id: int
    client_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class HoldingResponse(BaseModel):
    asset_symbol: str
    quantity: Decimal
    invested_amount: Decimal


class PortfolioSummaryResponse(BaseModel):
    portfolio_id: int
    total_invested: Decimal
    holdings: list[HoldingResponse]
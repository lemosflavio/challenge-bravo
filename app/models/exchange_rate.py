from datetime import datetime

from pydantic import BaseModel, Field


class ExchangeRateModel(BaseModel):
    exchange_from: str
    exchange_to: str
    exchange_tax: float
    last_update: datetime = Field(default_factory=datetime.now)

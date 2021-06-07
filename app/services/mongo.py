from typing import Optional

from motor.core import AgnosticCollection

from app.models.exchange_rate import ExchangeRateModel, ExchangeRatesModel


class ExchangeRateService:
    def __init__(self, exchange_rate_collection: AgnosticCollection):
        self.__collection = exchange_rate_collection

    async def find_one(self, exchange_from: str, exchange_to: str) -> Optional[ExchangeRateModel]:
        data = await self.__collection.find_one({
            'exchange_from': exchange_from,
            'exchange_to': exchange_to
        })
        return ExchangeRateModel(**data) if data else None

    async def find(self) -> ExchangeRatesModel:
        data = await self.__collection.find({}).to_list(None)
        return ExchangeRatesModel(exchange_rates=data)

    async def insert(self, exchange_rate: ExchangeRateModel):
        await self.__collection.insert_one(exchange_rate.dict())

    async def update(self, exchange_rate: ExchangeRateModel):
        search = {
            'exchange_from': exchange_rate.exchange_from,
            'exchange_to': exchange_rate.exchange_to
        }
        update = {
            "$set": exchange_rate.dict()
        }
        await self.__collection.update_one(search, update)

from typing import Dict

from aiohttp import web
from aiohttp_swagger import swagger_path
from webargs.aiohttpparser import use_args

from app.config import settings
from app.models.exchange_rate import ExchangeRateModel
from app.schemas.exchange_rate_schema import ExchangeRateRequestSchema
from app.services.mongo import ExchangeRateService


@swagger_path(f"{settings.SWAGGER_PATH}/exchange_rate.yaml")
class ExchangeRate(web.View):
    async def get(self) -> web.Response:
        service: ExchangeRateService = self.request.app["exchange_rate_service"]
        exchange_rates = await service.find()

        return web.json_response(text=exchange_rates.json())

    @use_args(ExchangeRateRequestSchema, location='json')
    async def post(self, args: Dict) -> web.Response:
        service: ExchangeRateService = self.request.app["exchange_rate_service"]
        exchange_rate = await service.find_one(args['exchange_from'], args['exchange_to'])

        if exchange_rate:
            raise web.HTTPConflict(
                reason=f"Already exists a exchange rate with current data {args['exchange_from']} > {args['exchange_to']}"
            )

        exchange_rate = ExchangeRateModel(**args)
        await service.insert(exchange_rate)
        response_data = {
            'message': "Exchange rate created",
        }

        return web.json_response(response_data, status=web.HTTPCreated.status_code)

    @use_args(ExchangeRateRequestSchema, location='json')
    async def put(self, args: Dict) -> web.Response:
        service: ExchangeRateService = self.request.app["exchange_rate_service"]
        exchange_rate = await service.find_one(args['exchange_from'], args['exchange_to'])

        if not exchange_rate:
            raise web.HTTPNotFound(
                reason="Could not find the requested exchange rate to update"
            )

        exchange_rate = ExchangeRateModel(**args)
        await service.update(exchange_rate)
        response_data = {
            'message': "Exchange rate updated",
        }

        return web.json_response(response_data, status=web.HTTPAccepted.status_code)

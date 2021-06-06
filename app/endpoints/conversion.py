from typing import Dict

from aiohttp import web
from aiohttp_swagger import swagger_path
from webargs.aiohttpparser import use_args

from app.config import settings
from app.schemas.conversion_schema import ConversionRequestSchema
from app.services.mongo import ExchangeRateService


@swagger_path(f"{settings.SWAGGER_PATH}/conversion.yaml")
class Conversion(web.View):
    @use_args(ConversionRequestSchema, location="querystring")
    async def get(self, args: Dict) -> web.Response:
        service: ExchangeRateService = self.request.app["exchange_rate_service"]
        exchange_rate = await service.find_one(args['from_'], args['to'])

        if not exchange_rate:
            raise web.HTTPNotFound(
                reason="Could not find the requested conversion"
            )

        response_data = {
            "from": exchange_rate.exchange_from,
            "to": exchange_rate.exchange_to,
            "amount": args['amount'],
            "converted_amount": args['amount'] / exchange_rate.exchange_tax,
        }

        return web.json_response(response_data)

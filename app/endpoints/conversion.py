from typing import Dict

from aiohttp import web
from aiohttp_swagger import swagger_path
from webargs.aiohttpparser import use_args

from app.schemas.conversion_schema import ConversionRequestSchema
from app.config import settings


@swagger_path(f"{settings.SWAGGER_PATH}/conversion.yaml")
class Conversion(web.View):
    @use_args(ConversionRequestSchema, location="querystring")
    async def get(self, args: Dict) -> web.Response:
        response_data = {
            "from": args['from_'],
            "to": args['to'],
            "amount": args['amount'],
            "converted_amount": args['amount'] / 5,
        }

        return web.json_response(response_data)

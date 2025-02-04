from http import HTTPStatus

from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app.models.exchange_rate import ExchangeRateModel
from app.routes import ROUTES_MAPPING
from tests.base_tests import AppBaseTest
from tests.config import LOCAL_SERVERS


class TestConversion(AppBaseTest):
    def setUp(self):
        super(TestConversion, self).setUp()
        self.route = ROUTES_MAPPING['get_conversion']

    @unittest_run_loop
    async def test_it_returns_200(self):
        await self.app["exchange_rate_service"].insert(ExchangeRateModel(**{
            "exchange_from": "BRL",
            "exchange_to": "USD",
            "exchange_tax": 5,
        }))

        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_GET,
                path=self.route.path,
                params={
                    "from": "BRL",
                    "to": "USD",
                    "amount": 5,
                }
            )

            content = await response.json()

        expected_content = {
            "from": "BRL",
            "to": "USD",
            "amount": 5,
            "converted_amount": 1
        }
        self.assertEqual(HTTPStatus.OK, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_404_if_exchange_rate_dont_exists(self):
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_GET,
                path=self.route.path,
                params={
                    "from": "BRL",
                    "to": "USD",
                    "amount": 5,
                }
            )

            content = await response.json()

        expected_content = {
            'message': '404: Could not find the requested conversion'
        }
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_422_if_send_invalid_params(self):
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_GET,
                path=self.route.path,
                params={
                    "from": "345",
                    "to": "USD",
                    "amount": "5asd",
                }
            )

            content = await response.json()

        expected_content = {"message": "{\"querystring\": {\"amount\": [\"Not a valid number.\"]}}"}
        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status)
        self.assertEqual(expected_content, content)

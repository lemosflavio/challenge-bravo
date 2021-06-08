from http import HTTPStatus
from unittest.mock import ANY

from aiohttp.hdrs import METH_GET, METH_POST, METH_PUT
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app.models.exchange_rate import ExchangeRateModel
from app.routes import ROUTES_MAPPING
from tests.base_tests import AppBaseTest
from tests.config import LOCAL_SERVERS


class TestExchangeRateGet(AppBaseTest):
    def setUp(self):
        super(TestExchangeRateGet, self).setUp()
        self.route = ROUTES_MAPPING['get_exchange_rates']

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
            )

            content = await response.json()

        expected_content = {
            'exchange_rates': [{
                "exchange_from": "BRL",
                "exchange_to": "USD",
                "exchange_tax": 5,
                "last_update": ANY
            }]
        }
        self.assertEqual(HTTPStatus.OK, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_empty_list_if_db_is_empty(self):
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_GET,
                path=self.route.path,
            )

            content = await response.json()

        expected_content = {
            'exchange_rates': []
        }
        self.assertEqual(HTTPStatus.OK, response.status)
        self.assertEqual(expected_content, content)


class TestExchangeRatePost(AppBaseTest):
    def setUp(self):
        super(TestExchangeRatePost, self).setUp()
        self.route = ROUTES_MAPPING['post_exchange_rate']

    @unittest_run_loop
    async def test_it_returns_201(self):
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_POST,
                path=self.route.path,
                json={
                    "exchange_from": "BRL",
                    "exchange_to": "USD",
                    "exchange_tax": 5,
                }
            )

            content = await response.json()

        expected_content = {
            'message': "Exchange rate created",
        }
        self.assertEqual(HTTPStatus.CREATED, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_400_if_exchange_rate_already_exists(self):
        await self.app["exchange_rate_service"].insert(ExchangeRateModel(**{
            "exchange_from": "BRL",
            "exchange_to": "USD",
            "exchange_tax": 5,
        }))

        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_POST,
                path=self.route.path,
                json={
                    "exchange_from": "BRL",
                    "exchange_to": "USD",
                    "exchange_tax": 5,
                }
            )

            content = await response.json()

        expected_content = {
            'message': "409: Already exists a exchange rate with current data BRL > USD",
        }
        self.assertEqual(HTTPStatus.CONFLICT, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_422_if_send_invalid_values(self):
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_POST,
                path=self.route.path,
                json={
                    "exchange_from": "345",
                    "exchange_to": "USD",
                    "exchange_tax": "5asd",
                }
            )

            content = await response.json()

        expected_content = {'message': '{"json": {"exchange_tax": ["Not a valid number."]}}'}
        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status)
        self.assertEqual(expected_content, content)


class TestExchangeRatePut(AppBaseTest):
    def setUp(self):
        super(TestExchangeRatePut, self).setUp()
        self.route = ROUTES_MAPPING['put_exchange_rate']

    @unittest_run_loop
    async def test_it_returns_201(self):
        await self.app["exchange_rate_service"].insert(ExchangeRateModel(**{
            "exchange_from": "BRL",
            "exchange_to": "USD",
            "exchange_tax": 10,
        }))
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_PUT,
                path=self.route.path,
                json={
                    "exchange_from": "BRL",
                    "exchange_to": "USD",
                    "exchange_tax": 5,
                }
            )

            content = await response.json()

        expected_content = {
            'message': "Exchange rate updated",
        }
        self.assertEqual(HTTPStatus.ACCEPTED, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_404_if_exchange_rate_dont_exists(self):

        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_PUT,
                path=self.route.path,
                json={
                    "exchange_from": "BRL",
                    "exchange_to": "USD",
                    "exchange_tax": 5,
                }
            )

            content = await response.json()

        expected_content = {
            'message': "404: Could not find the requested exchange rate to update",
        }
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status)
        self.assertEqual(expected_content, content)

    @unittest_run_loop
    async def test_it_returns_422_if_send_invalid_values(self):
        with aioresponses(passthrough=LOCAL_SERVERS):
            response = await self.client.request(
                method=METH_PUT,
                path=self.route.path,
                json={
                    "exchange_from": "345",
                    "exchange_to": "USD",
                    "exchange_tax": "5asd",
                }
            )

            content = await response.json()

        expected_content = {'message': '{"json": {"exchange_tax": ["Not a valid number."]}}'}
        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status)
        self.assertEqual(expected_content, content)

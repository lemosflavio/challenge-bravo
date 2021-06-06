from http import HTTPStatus
from unittest.mock import patch

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses
from asynctest import CoroutineMock
from pymongo.errors import ServerSelectionTimeoutError

from app.routes import ROUTES_MAPPING
from tests.base_tests import AppBaseTest
from tests.config import LOCAL_SERVERS


class HealthCheckViewTests(AppBaseTest):
    route = ROUTES_MAPPING['get_health_check']

    def setUp(self):
        super(HealthCheckViewTests, self).setUp()
        self.responses = aioresponses(passthrough=LOCAL_SERVERS)

    @unittest_run_loop
    async def test_everything_ok(self):
        mongo_server_info = CoroutineMock()

        with patch.object(
            self.app["mongo_db"].client, "server_info", side_effect=mongo_server_info
        ):
            with self.responses:
                response = await self.client.request("GET", self.route.path)

                mongo_server_info.assert_awaited_once()

        self.assertEqual(HTTPStatus.OK, response.status)
        self.assertEqual(
            await response.json(),
            {"validate_mongo_connection": True},
        )

    @unittest_run_loop
    async def test_when_mongodb_is_unhealthy_must_return_500(self):
        with patch.object(
            self.app["mongo_db"].client,
            "server_info",
            side_effect=ServerSelectionTimeoutError,
        ) as server_info_mock:
            with aioresponses(passthrough=LOCAL_SERVERS):
                response = await self.client.request("GET", self.route.path)

                resp_body = await response.json()
                self.assertFalse(resp_body["validate_mongo_connection"])
                server_info_mock.assert_called_once()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status)

import asyncio
import json
from http import HTTPStatus

from aiohttp import web
from aiologger import Logger
from asynctest import TestCase, Mock, CoroutineMock, MagicMock

from app.middlewares import middleware


class MiddlewareTests(TestCase):
    async def setUp(self):
        self.request = MagicMock(
            rel_url="https://www.conversion.com",
            loop=CoroutineMock(spec=asyncio.AbstractEventLoop),
            app={"logger": Mock(spec=Logger)},
        )

    async def test_404_responses_returns_json_responses_as_is(self):
        response = web.json_response(status=HTTPStatus.NOT_FOUND)
        handler = CoroutineMock(return_value=response)
        middleware_response = await middleware(self.request, handler)

        handler.assert_awaited_once_with(self.request)
        self.assertEqual(middleware_response, response)

    async def test_404_exceptions_returns_a_json_response_for_non_json_responses(
        self
    ):
        exc = web.HTTPNotFound()
        handler = CoroutineMock(side_effect=exc)
        middleware_response = await middleware(self.request, handler)

        handler.assert_called_once_with(self.request)

        self.assertEqual(middleware_response.content_type, "application/json")
        self.assertEqual(middleware_response.status, 404)
        self.assertEqual(middleware_response.reason, exc.reason)
        self.assertEqual(
            json.loads(middleware_response.text), {"message": "404: Not Found"}
        )

    async def test_500_exceptions_returns_a_valid_json_response(self):
        exc = web.HTTPInternalServerError()
        handler = CoroutineMock(side_effect=exc)
        middleware_response = await middleware(self.request, handler)

        handler.assert_called_once_with(self.request)

        self.assertEqual(middleware_response.content_type, "application/json")
        self.assertEqual(middleware_response.status, 500)
        self.assertEqual(
            json.loads(middleware_response.text),
            {"message": "500: Internal Server Error"},
        )

    async def test_422_exceptions_gets_logged_and_returns_a_valid_json_response(
        self
    ):
        exc = web.HTTPUnprocessableEntity(body=b"{'data': ['missing']}")
        handler = CoroutineMock(side_effect=exc)
        middleware_response = await middleware(self.request, handler)

        handler.assert_called_once_with(self.request)
        self.assertEqual(middleware_response.content_type, "application/json")
        self.assertEqual(middleware_response.status, 422)
        self.assertEqual(middleware_response.reason, exc.reason)

    async def test_other_exceptions_gets_raised(self):
        exc = web.HTTPBadGateway()
        handler = CoroutineMock(side_effect=exc)

        with self.assertRaises(web.HTTPBadGateway):
            await middleware(self.request, handler)

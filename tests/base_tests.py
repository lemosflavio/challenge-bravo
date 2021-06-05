from aiohttp.test_utils import AioHTTPTestCase
from aiologger.loggers.json import JsonLogger
from asynctest import patch, Mock

from app.api import Api


class AppBaseTest(AioHTTPTestCase):
    async def get_application(self):
        api = Api()
        return api.app

    def setUp(self):
        self.logger = Mock(spec=JsonLogger)
        patch(
            "app.api.JsonLogger.with_default_handlers", return_value=self.logger
        ).start()
        super().setUp()

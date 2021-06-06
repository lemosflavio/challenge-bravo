from aiohttp.test_utils import AioHTTPTestCase
from aiologger.loggers.json import JsonLogger
from asynctest import patch, Mock, MagicMock

from app.api import Api


class AppBaseTest(AioHTTPTestCase):
    async def get_application(self):
        api = Api()
        api.app["mongo_db"] = MagicMock()
        return api.app

    def setUp(self):
        self.logger = Mock(spec=JsonLogger)
        self.logger_patch = patch(
            "app.api.JsonLogger.with_default_handlers", return_value=self.logger
        )
        self.logger_patch.start()
        super().setUp()

    def tearDown(self):
        self.logger_patch.stop()
        self.loop.run_until_complete(self.clear_mongo())
        super().tearDown()

    async def clear_mongo(self):
        collections = await self.app["mongo_db"].list_collection_names()
        for collection in collections:
            await self.app["mongo_db"][collection].drop()

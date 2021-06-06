from aiohttp import web
from aiohttp_swagger import swagger_path
from healthchecker import check
from healthchecker.async_checker import AsyncCheckCase

from app.config import settings


@swagger_path(f"{settings.SWAGGER_PATH}/health_check.yaml")
class HealthCheckView(web.View, AsyncCheckCase):
    @property
    def loop(self):
        return

    async def get(self) -> "web.Response":
        """
        Should return 200 if all dependencies are ok, 500 otherwise.
        :returns: A HTTP response with True or False for each check
        """
        await self.check()

        status_code = 200 if self.has_succeeded() else 500

        return web.json_response(data=self.check_report, status=status_code)

    @check
    async def validate_mongo_connection(self):
        conn = self.request.app["mongo_db"].client
        await conn.server_info()
        return True

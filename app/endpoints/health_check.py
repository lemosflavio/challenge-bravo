from aiohttp import web
from aiohttp_swagger import swagger_path
from healthchecker import check
from healthchecker.async_checker import AsyncCheckCase

from app.config import settings


@swagger_path(f"{settings.SWAGGER_PATH}/health_check.yaml")
class HealthCheckView(web.View, AsyncCheckCase):
    async def get(self) -> "web.Response":
        """
        Should return 200 if all dependencies are ok, 500 otherwise.
        :returns: A HTTP response with True or False for each check
        """
        await self.check()

        status_code = 200 if self.has_succeeded() else 500
        # self.check_report.update({"version": config.LAST_HASH_GIT[:9]})

        return web.json_response(data=self.check_report, status=status_code)

    @check
    async def health_check(self):
        return True

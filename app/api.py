import asyncio
from typing import Iterable

from aiohttp import web
from aiohttp_swagger import setup_swagger
from aiologger.handlers.files import AsyncFileHandler
from aiologger.loggers.json import JsonLogger

from app.config import settings
from app.middlewares import middleware
from app.routes import ROUTES, RouteView


class Api:
    def __init__(self, routes: Iterable[RouteView] = ROUTES):
        self.loop = asyncio.get_event_loop()
        self.app: web.Application = web.Application(
            middlewares=[middleware]
        )
        self.app["api"] = self
        self._views = routes or []
        self.register_routes()
        self.register_signals()
        self.app.on_startup.append(self.init_services)
        self.app.on_shutdown.append(self.shutdown)

    async def init_services(self, app):
        handler = AsyncFileHandler(filename=settings.LOG_FILENAME)
        self.app["logger"] = JsonLogger.with_default_handlers(
            level=settings.LOG_LEVEL,
            flatten=True,
        )
        self.app["logger"].add_handler(handler)

    def register_routes(self):
        for view in self._views:
            self.app.router.add_route(
                method=view.method, path=view.path, handler=view.handler
            )

    async def shutdown(self, app):
        await self.app["logger"].shutdown()

    def register_signals(self):
        self.app.on_shutdown.append(self.shutdown)

    def start(self):
        setup_swagger(
            self.app,
            description=settings.SWAGGER_DESCRIPTION,
            title=settings.SWAGGER_TITLE,
        )
        web.run_app(self.app, port=settings.PORT, host=settings.HOST)

from collections import namedtuple

from app.endpoints.conversion import Conversion
from app.endpoints.health_check import HealthCheckView

RouteView = namedtuple("RouteView", ["method", "path", "handler"])

ROUTES = (
    RouteView(method="GET", path="/health_check", handler=HealthCheckView),
    RouteView(method="GET", path="/conversion", handler=Conversion),
)

ROUTES_MAPPING = {route.handler: route for route in ROUTES}

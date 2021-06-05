from collections import namedtuple

from app.endpoints.conversion import Conversion
from app.endpoints.health_check import HealthCheckView

RouteView = namedtuple("RouteView", ["method", "path", "handler"])

ROUTES_MAPPING = {
    "get_health_check": RouteView(method="GET", path="/health_check", handler=HealthCheckView),
    "get_conversion": RouteView(method="GET", path="/conversion", handler=Conversion),
}

ROUTES = tuple(ROUTES_MAPPING.values())

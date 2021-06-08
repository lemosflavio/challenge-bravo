from collections import namedtuple

from app.endpoints.conversion import Conversion
from app.endpoints.exchange_rate import ExchangeRate
from app.endpoints.health_check import HealthCheckView

RouteView = namedtuple("RouteView", ["method", "path", "handler"])

ROUTES_MAPPING = {
    "get_health_check": RouteView(method="GET", path="/health_check", handler=HealthCheckView),
    "get_conversion": RouteView(method="GET", path="/conversion", handler=Conversion),
    "get_exchange_rates": RouteView(method="GET", path="/exchange_rate", handler=ExchangeRate),
    "post_exchange_rate": RouteView(method="POST", path="/exchange_rate", handler=ExchangeRate),
    "put_exchange_rate": RouteView(method="PUT", path="/exchange_rate", handler=ExchangeRate),
}

ROUTES = tuple(ROUTES_MAPPING.values())

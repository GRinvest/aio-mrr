"""Модели для Info API.

Этот модуль содержит модели для эндпоинтов /info/*:
- /info/servers
- /info/algos
- /info/algos/{name}
- /info/currencies
"""

from aio_mrr.models.info.request import InfoAlgosQueryParams
from aio_mrr.models.info.response import AlgoInfo, CurrencyInfo, ServersList

__all__ = [
    "AlgoInfo",
    "CurrencyInfo",
    "InfoAlgosQueryParams",
    "ServersList",
]

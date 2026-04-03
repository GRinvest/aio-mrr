"""Request модели для Info API.

Этот модуль содержит модели для query параметров запросов к Info API.
"""

from pydantic import Field

from aio_mrr.models.base import BaseMRRModel


class InfoAlgosQueryParams(BaseMRRModel):
    """Query параметры для GET /info/algos.

    Attributes:
        currency: Валюта для цен (BTC, LTC, ETH, DOGE, BCH). По умолчанию BTC.
    """

    currency: str | None = Field(default=None, description="Валюта для цен")

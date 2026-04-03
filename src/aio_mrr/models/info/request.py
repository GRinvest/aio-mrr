"""Request models for Info API.

This module contains models for query parameters of requests to the Info API.
"""

from pydantic import Field

from aio_mrr.models.base import BaseMRRModel


class InfoAlgosQueryParams(BaseMRRModel):
    """Query parameters for GET /info/algos.

    Attributes:
        currency: Currency for prices (BTC, LTC, ETH, DOGE, BCH). Default BTC.
    """

    currency: str | None = Field(default=None, description="Currency for prices")

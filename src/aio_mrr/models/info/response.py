"""Response models for Info API.

This module contains models for responses from the Info API:
- ServersList — response for GET /info/servers
- AlgoInfo — response for GET /info/algos and GET /info/algos/{name}
- CurrencyInfo — response for GET /info/currencies
"""

from typing import Any

from aio_mrr.models.base import BaseMRRModel
from pydantic import field_validator


def _parse_float_or_none(value: Any) -> float | None:
    """Parse float value, returning None for empty strings."""
    if value == "" or value is None:
        return None
    return float(value)


class HashInfo(BaseMRRModel):
    """Hashrate information.

    Attributes:
        hash: Hashrate value.
        unit: Unit of measurement (mh, th, etc.).
        nice: Human-readable representation (e.g., "882.70G").
    """

    hash: float | None = None
    unit: str
    nice: str

    @field_validator("hash", mode="before")
    @classmethod
    def parse_hash(cls, v: Any) -> float | None:
        return _parse_float_or_none(v)


class PriceInfo(BaseMRRModel):
    """Price information.

    Attributes:
        amount: Price value.
        currency: Currency (BTC, LTC, ETH, DOGE, BCH).
        unit: Unit of measurement (e.g., "mh*day", "th*day").
    """

    amount: str
    currency: str
    unit: str


class AvailableHashInfo(BaseMRRModel):
    """Available hashrate information.

    Attributes:
        rigs: Number of available rigs.
        hash: Hashrate information.
    """

    rigs: str
    hash: HashInfo


class RentedHashInfo(BaseMRRModel):
    """Rented hashrate information.

    Attributes:
        rigs: Number of rented rigs.
        hash: Hashrate information.
    """

    rigs: str
    hash: HashInfo


class PricesInfo(BaseMRRModel):
    """Price information.

    Attributes:
        lowest: Lowest price.
        last_10: Price of the last 10 rentals.
        last: Last price.
    """

    lowest: PriceInfo
    last_10: PriceInfo
    last: PriceInfo


class AlgoStats(BaseMRRModel):
    """Statistics for an algorithm.

    Attributes:
        available: Available hashrate information.
        rented: Rented hashrate information.
        prices: Price information.
    """

    available: AvailableHashInfo
    rented: RentedHashInfo
    prices: PricesInfo


# --- Main models ---


class AlgoInfo(BaseMRRModel):
    """Mining algorithm information.

    Used for responses:
    - GET /info/algos (list of algorithms)
    - GET /info/algos/{name} (single algorithm)

    Attributes:
        name: Algorithm name (e.g., "scrypt", "sha256").
        display: Display name (e.g., "Scrypt").
        suggested_price: Suggested price.
        stats: Algorithm statistics.
    """

    name: str
    display: str
    suggested_price: PriceInfo
    stats: AlgoStats


class ServerInfo(BaseMRRModel):
    """MRR server information.

    Attributes:
        id: Server identifier.
        name: Server name (e.g., "us-central01.miningrigrentals.com").
        region: Server region (e.g., "us-central", "eu-ru").
        port: Connection port (deprecated field).
        ethereum_port: Ethereum port (deprecated field).
    """

    id: str
    name: str
    region: str
    port: str | None = None
    ethereum_port: str | None = None


class ServersList(BaseMRRModel):
    """List of MRR servers.

    Response for GET /info/servers.

    Attributes:
        servers: List of server information.
    """

    servers: list[ServerInfo]


class CurrencyInfo(BaseMRRModel):
    """Currency information.

    Used for GET /info/currencies response.

    Attributes:
        name: Currency name (e.g., "BTC", "LTC").
        enabled: Flag indicating currency availability for payments.
        txfee: Withdrawal fee.
    """

    name: str
    enabled: bool
    txfee: str

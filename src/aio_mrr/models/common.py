"""Common data models for the aio-mrr library.

This module contains common models used in multiple places:
- HashInfo: hashrate information
- PriceInfo: price information
- PoolInfo: pool information
- ServerInfo: server information
"""

from __future__ import annotations

from .base import BaseMRRModel


class HashInfo(BaseMRRModel):
    """Hashrate information.

    Used to represent hashrate in various contexts
    (algorithms, rig, rental, etc.).

    Attributes:
        hash: Hashrate value.
        unit: Unit of measurement (e.g., "mh", "th").
        nice: Human-readable representation (e.g., "882.70G").
    """

    hash: float
    unit: str
    nice: str


class PriceInfo(BaseMRRModel):
    """Price information.

    Used to represent the price of an algorithm or hashrate.

    Attributes:
        amount: Price value.
        currency: Price currency (e.g., "BTC", "LTC", "ETH").
        unit: Price unit of measurement (e.g., "mh*day", "th*day").
    """

    amount: str
    currency: str
    unit: str


class PoolInfo(BaseMRRModel):
    """Pool information.

    Used to represent mining pool information.
    Can be used in the context of profile, rig, rental.

    Attributes:
        priority: Pool priority (0-4).
        type: Pool algorithm type (e.g., "scrypt", "sha256").
        host: Pool host.
        port: Pool port.
        user: Username/worker name.
        pass_: Worker password.
        status: Pool status (optional, may be empty).
    """

    priority: int
    type: str
    host: str
    port: str
    user: str
    pass_: str
    status: str | None = None


class ServerInfo(BaseMRRModel):
    """MRR server information.

    Used to represent MiningRigRentals server information.

    Attributes:
        id: Server identifier.
        name: Server name (hostname).
        region: Server region (e.g., "us-central", "eu-ru").
        port: Connection port (optional, deprecated field).
        ethereum_port: Ethereum port (optional, deprecated field).
    """

    id: str
    name: str
    region: str
    port: str | None = None
    ethereum_port: str | None = None

"""Request models for Account API.

This module contains models for query parameters and request bodies for the Account API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel


class TransactionsQueryParams(BaseMRRModel):
    """Query parameters for GET /account/transactions.

    Used to retrieve and filter transaction history.

    Attributes:
        start: Pagination start. Default 0.
        limit: Record limit. Default 100.
        algo: Filter by algorithm.
        type: Transaction type (credit, payout, referral, deposit, payment,
              credit/refund, debit/refund, rental fee).
        rig: Filter by rig ID.
        rental: Filter by rental ID.
        txid: Filter by txid.
        time_greater_eq: Time >= (Unix timestamp).
        time_less_eq: Time <= (Unix timestamp).
    """

    start: int | None = Field(default=None, description="Pagination start")
    limit: int | None = Field(default=None, description="Record limit")
    algo: str | None = Field(default=None, description="Filter by algorithm")
    type: str | None = Field(default=None, description="Transaction type")
    rig: int | None = Field(default=None, description="Filter by rig ID")
    rental: int | None = Field(default=None, description="Filter by rental ID")
    txid: str | None = Field(default=None, description="Filter by txid")
    time_greater_eq: str | None = Field(default=None, description="Time >= (Unix timestamp)")
    time_less_eq: str | None = Field(default=None, description="Time <= (Unix timestamp)")


class ProfileCreateBody(BaseMRRModel):
    """Request body for PUT /account/profile.

    Used to create a new pool profile.

    Attributes:
        name: Profile name (required).
        algo: Profile algorithm (required).
    """

    name: str = Field(..., description="Profile name")
    algo: str = Field(..., description="Profile algorithm")


class PoolTestBody(BaseMRRModel):
    """Request body for PUT /account/pools/test.

    Used to test pool connection.

    Attributes:
        method: Test method (simple or full).
        extramethod: For ethhash: [esm0,esm1,esm2,esm3]. Default esm0.
        type: Algorithm (scrypt, sha256, x11). Required for full method.
        host: Pool host (may include port).
        port: Pool port. Required if not in host.
        user: Username. Required for full method.
        pass: Password. Required for full method.
        source: MRR server for testing. Default us-central01.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    method: str = Field(..., description="Test method (simple or full)")
    extramethod: str | None = Field(default=None, description="For ethhash: [esm0,esm1,esm2,esm3]")
    type: str | None = Field(default=None, description="Algorithm (for full method)")
    host: str | None = Field(default=None, description="Pool host")
    port: int | None = Field(default=None, description="Pool port")
    user: str | None = Field(default=None, description="Username")
    password: str | None = Field(default=None, alias="pass", description="Password")
    source: str | None = Field(default=None, description="MRR server for testing")


class PoolCreateBody(BaseMRRModel):
    """Request body for PUT /account/pool.

    Used to create a saved pool.

    Attributes:
        type: Algorithm (sha256, scrypt, x11, etc.) (required).
        name: Name for identification (required).
        host: Pool host (required).
        port: Pool port (required).
        user: Worker name (required).
        pass: Worker password (optional).
        notes: Notes (optional).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type: str = Field(..., description="Pool algorithm")
    name: str = Field(..., description="Pool name")
    host: str = Field(..., description="Pool host")
    port: int = Field(..., description="Pool port")
    user: str = Field(..., description="Worker name")
    password: str | None = Field(default=None, alias="pass", description="Worker password")
    notes: str | None = Field(default=None, description="Notes")

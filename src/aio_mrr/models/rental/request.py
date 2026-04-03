"""Request models for Rental API.

This module contains models for query parameters and request bodies for the Rental API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel


class RentalListQueryParams(BaseMRRModel):
    """Query parameters for GET /rental.

    Used to retrieve a list of rentals with filtering and pagination.

    Attributes:
        type: Rental type - 'owner' or 'renter'. Default 'renter'.
        algo: Filter by algorithm.
        history: true = completed, false = active. Default false.
        rig: Filter by rig ID.
        start: Pagination start. Default 0.
        limit: Pagination limit. Default 25.
        currency: Currency - [BTC,LTC,ETH,DOGE,BCH].
    """

    type: str | None = Field(default=None, description="Rental type - 'owner' or 'renter'")
    algo: str | None = Field(default=None, description="Filter by algorithm")
    history: bool | None = Field(default=None, description="true = completed, false = active")
    rig: int | None = Field(default=None, description="Filter by rig ID")
    start: int | None = Field(default=None, description="Pagination start")
    limit: int | None = Field(default=None, description="Pagination limit")
    currency: str | None = Field(default=None, description="Currency - [BTC,LTC,ETH,DOGE,BCH]")


class RentalCreateBody(BaseMRRModel):
    """Request body for PUT /rental.

    Used to create a new rental.

    Attributes:
        rig: Rig ID for rental (required).
        length: Duration in hours (required).
        profile: Pool profile ID (required).
        currency: Payment currency. Default BTC.
        rate_type: Hash type. Default 'mh'.
        rate_price: Price per hash unit per day.
    """

    model_config = ConfigDict(populate_by_name=True)

    rig: int = Field(..., description="Rig ID for rental")
    length: float = Field(..., description="Duration in hours")
    profile: int = Field(..., description="Pool profile ID")
    currency: str | None = Field(default=None, description="Payment currency")
    rate_type: str | None = Field(default=None, alias="rate.type", description="Hash type")
    rate_price: float | None = Field(default=None, alias="rate.price", description="Price per hash unit per day")


class RentalExtendBody(BaseMRRModel):
    """Request body for PUT /rental/{ids}/extend.

    Used to extend a rental.

    Attributes:
        length: Hours to extend (required).
        getcost: If set, simulates extension and returns cost.
    """

    length: float = Field(..., description="Hours to extend")
    getcost: bool | None = Field(default=None, description="Simulate extension and return cost")


class RentalPoolBody(BaseMRRModel):
    """Request body for PUT /rental/{ids}/pool.

    Used to add or replace a pool on rentals.

    Attributes:
        host: Pool host (required).
        port: Pool port (required).
        user: Worker name (required).
        pass: Worker password (required).
        priority: Priority (0-4).
    """

    host: str = Field(..., description="Pool host")
    port: int = Field(..., description="Pool port")
    user: str = Field(..., description="Worker name")
    password: str = Field(..., alias="pass", description="Worker password")
    priority: int | None = Field(default=None, description="Priority (0-4)")

"""Response models for Rental API.

This module contains models for responses from the Rental API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel


class RateInfo(BaseMRRModel):
    """Rental rate information.

    Attributes:
        type: Hash type (mh, gh, etc.).
        price: Price per hash unit per day.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: str | None = Field(default=None, alias="rate.type", description="Hash type")
    price: str | None = Field(default=None, alias="rate.price", description="Price per hash unit per day")


class RentalHashInfo(BaseMRRModel):
    """Rental hashrate information.

    Attributes:
        hash: Hashrate.
        type: Hash type (hash, kh, mh, gh, etc.).
    """

    hash: float | None = Field(default=None, description="Hashrate")
    type: str | None = Field(default=None, description="Hash type")


class RentalCostInfo(BaseMRRModel):
    """Rental cost information.

    Attributes:
        amount: Cost amount.
        currency: Cost currency.
    """

    amount: str | None = Field(default=None, description="Cost amount")
    currency: str | None = Field(default=None, description="Cost currency")


class RentalInfo(BaseMRRModel):
    """Rental information.

    Used for responses:
    - GET /rental
    - GET /rental/{ids}

    Attributes:
        id: Rental identifier.
        rig_id: Rig ID.
        rig_name: Rig name.
        owner: Rig owner name.
        renter: Renter name.
        status: Rental status (active, etc.).
        started: Rental start time.
        ends: Rental end time.
        length: Duration in hours.
        currency: Payment currency.
        rate: Rate information.
        hash: Hashrate information.
        cost: Cost information.
    """

    id: str = Field(..., description="Rental identifier")
    rig_id: str | None = Field(default=None, alias="rig_id", description="Rig ID")
    rig_name: str | None = Field(default=None, description="Rig name")
    owner: str | None = Field(default=None, description="Rig owner name")
    renter: str | None = Field(default=None, description="Renter name")
    status: str | None = Field(default=None, description="Rental status")
    started: str | None = Field(default=None, description="Rental start time")
    ends: str | None = Field(default=None, description="Rental end time")
    length: float | None = Field(default=None, description="Duration in hours")
    currency: str | None = Field(default=None, description="Payment currency")
    rate: RateInfo | None = Field(default=None, description="Rate information")
    hash: RentalHashInfo | None = Field(default=None, description="Hashrate information")
    cost: RentalCostInfo | None = Field(default=None, description="Cost information")


class RentalList(BaseMRRModel):
    """List of rentals.

    Response for GET /rental.

    Attributes:
        rentals: List of rentals.
    """

    rentals: list[RentalInfo] = Field(..., description="List of rentals")


class RentalLogEntry(BaseMRRModel):
    """Rental activity log entry.

    Used for GET /rental/{ids}/log response.

    Attributes:
        time: Entry time.
        message: Event message.
    """

    time: str = Field(..., description="Entry time")
    message: str = Field(..., description="Event message")


class RentalMessage(BaseMRRModel):
    """Rental message.

    Used for GET /rental/{ids}/message response.

    Attributes:
        time: Message time.
        user: Username of the message sender.
        message: Message text.
    """

    time: str = Field(..., description="Message time")
    user: str = Field(..., description="Username")
    message: str = Field(..., description="Message text")


class GraphDataPoint(BaseMRRModel):
    """Data point on the rental graph.

    Attributes:
        time: Timestamp.
        hashrate: Hashrate at this point.
        downtime: Downtime flag.
    """

    time: str | None = Field(default=None, description="Timestamp")
    hashrate: float | None = Field(default=None, description="Hashrate")
    downtime: bool | None = Field(default=None, description="Downtime flag")


class GraphData(BaseMRRModel):
    """Rental graph data.

    Response for GET /rental/{ids}/graph.

    Attributes:
        hashrate_data: Hashrate history.
        downtime_data: Downtime history.
        hours: Number of hours of data.
    """

    hashrate_data: list[GraphDataPoint] | None = Field(default=None, description="Hashrate history")
    downtime_data: list[GraphDataPoint] | None = Field(default=None, description="Downtime history")
    hours: float | None = Field(default=None, description="Number of hours of data")

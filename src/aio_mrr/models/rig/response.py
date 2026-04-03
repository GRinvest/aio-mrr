"""Response models for Rig API.

This module contains models for responses from the Rig API.
"""

from typing import Any
from pydantic import Field, field_validator

from aio_mrr.models.base import BaseMRRModel


class RigPriceInfo(BaseMRRModel):
    """Rig price information.

    Attributes:
        enabled: Whether pricing is enabled.
        price: Rig price per day.
        autoprice: Whether auto-pricing is enabled.
        minimum: Minimum auto-pricer price.
        modifier: Percentage +/- for auto-pricing.
    """

    enabled: bool | None = None
    price: float | None = None
    autoprice: bool | None = None
    minimum: float | None = None
    modifier: float | str | None = None

    @field_validator("modifier", mode="before")
    @classmethod
    def parse_modifier(cls, v: Any) -> float | str | None:
        if v is None:
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return v


class RigHashInfo(BaseMRRModel):
    """Rig hashrate information.

    Attributes:
        hash: Hashrate.
        type: Hash type (hash,kh,mh,gh,th,ph,eh).
    """

    hash: float | None = None
    type: str | None = None


class RigInfo(BaseMRRModel):
    """Rig information.

    Used for responses:
    - GET /rig
    - GET /rig/mine
    - GET /rig/{ids}

    Attributes:
        id: Rig identifier.
        name: Rig name.
        description: Rig description.
        server: Server name.
        status: Rig status (enabled/disabled).
        price: Price information by currency.
        price_type: Hash type for price.
        minhours: Minimum hours.
        maxhours: Maximum hours.
        extensions: Whether rental extension is allowed.
        hash: Hashrate information.
        suggested_diff: Suggested difficulty.
        ndevices: Number of devices (workers).
        type: Algorithm (sha256, scrypt, etc.).
        region: Region.
        online: Online status.
        rented: Rental status.
        last_hashrate: Last hashrate.
        rpi: RPI rating (0-100).
        owner: Rig owner.
    """

    id: int
    name: str
    description: str | None = None
    server: str | None = None
    status: dict[str, Any] | str | None = None
    price: dict[str, Any] | None = None
    price_type: str | None = Field(default=None, alias="price.type")
    minhours: float | None = None
    maxhours: float | None = None
    extensions: bool | None = None
    hash: RigHashInfo | None = Field(default=None)
    suggested_diff: float | None = None
    ndevices: int | None = None
    type: str | None = None
    region: str | None = None
    online: bool | None = None
    rented: bool | None = None
    last_hashrate: float | None = None
    rpi: float | None = None
    owner: str | None = None

    @field_validator("rpi", "suggested_diff", "last_hashrate", mode="before")
    @classmethod
    def parse_float_or_none(cls, v: Any) -> float | None:
        if v is None or v == "":
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None


class RigList(BaseMRRModel):
    """List of rigs.

    Response for GET /rig, GET /rig/mine, GET /rig/{ids}.
    API returns the list directly, but this model is for typing.

    Attributes:
        rigs: List of rigs.
    """

    rigs: list[RigInfo] = Field(..., description="List of rigs")


class RigPortInfo(BaseMRRModel):
    """Port information for a rig.

    Response for GET /rig/{ids}/port.

    Attributes:
        rigid: Rig ID.
        port: Direct port number for server connection.
        server: Server name.
        worker: Worker name for connection.
    """

    rigid: str | None = None
    port: int
    server: str | None = None
    worker: str | None = None


class RigThreadDetail(BaseMRRModel):
    """Details of a single thread.

    Attributes:
        id: Thread identifier.
        worker: Worker name.
        status: Thread status.
        hashrate: Current hashrate.
        last_share: Time of last share.
    """

    id: int | None = None
    worker: str | None = None
    status: str | None = None
    hashrate: float | None = None
    last_share: str | None = None


class RigThreadInfo(BaseMRRModel):
    """Thread information for a rig.

    Response for GET /rig/{ids}/threads — returns a list of rig groups with threads.

    Attributes:
        rigid: Rig ID.
        access: Access level (owner/renter).
        threads: List of thread details.
    """

    rigid: str | None = None
    access: str | None = None
    threads: list[RigThreadDetail] = []


class RigGraphData(BaseMRRModel):
    """Rig graph data.

    Response for GET /rig/{ids}/graph.

    Attributes:
        rigid: Rig ID.
        chartdata: Chart data (time_start, time_end, timestamp_start, timestamp_end, bars).
    """

    rigid: str | None = None
    chartdata: dict[str, Any] | None = None

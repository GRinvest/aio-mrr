"""Request models for Rig API.

This module contains models for query parameters and request bodies for the Rig API.
"""

from pydantic import Field

from aio_mrr.models.base import BaseMRRModel


class RigSearchParams(BaseMRRModel):
    """Query parameters for GET /rig.

    Used to search rigs by algorithm with filtering and sorting.

    Attributes:
        currency: Currency: [BTC,LTC,ETH,DOGE,BCH]. Default BTC.
        type: Algorithm: sha256, scrypt, x11, etc. (required).
        minhours_min: Minimum hours.
        minhours_max: Maximum hours.
        maxhours_min: Minimum maximum time.
        maxhours_max: Maximum maximum time.
        rpi_min: Minimum RPI (0-100).
        rpi_max: Maximum RPI (0-100).
        hash_min: Minimum hashrate.
        hash_max: Maximum hashrate.
        hash_type: Type: [hash,kh,mh,gh,th,ph,eh]. Default mh.
        price_min: Minimum price.
        price_max: Maximum price.
        price_type: Hash type for price.
        offline: Show offline rigs. Default false.
        rented: Show rented. Default false.
        region_type: 'include' or 'exclude'.
        expdiff: Expected worker difficulty.
        count: Number of results (max. 100). Default 100.
        islive: Filter for rigs with hashrate [yes].
        xnonce: Filter by xnonce [yes,no].
        offset: Pagination offset. Default 0.
        orderby: Sorting. Default score.
        orderdir: Direction [asc,desc]. Default asc.
    """

    currency: str | None = Field(default=None, description="Currency: [BTC,LTC,ETH,DOGE,BCH]")
    type: str = Field(..., description="Algorithm: sha256, scrypt, x11, etc.")
    minhours_min: int | None = Field(default=None, alias="minhours.min", description="Minimum hours")
    minhours_max: int | None = Field(default=None, alias="minhours.max", description="Maximum hours")
    maxhours_min: int | None = Field(default=None, alias="maxhours.min", description="Minimum maximum time")
    maxhours_max: int | None = Field(default=None, alias="maxhours.max", description="Maximum maximum time")
    rpi_min: int | None = Field(default=None, alias="rpi.min", description="Minimum RPI (0-100)")
    rpi_max: int | None = Field(default=None, alias="rpi.max", description="Maximum RPI (0-100)")
    hash_min: int | None = Field(default=None, alias="hash.min", description="Minimum hashrate")
    hash_max: int | None = Field(default=None, alias="hash.max", description="Maximum hashrate")
    hash_type: str | None = Field(default=None, alias="hash.type", description="Type: [hash,kh,mh,gh,th,ph,eh]")
    price_min: float | None = Field(default=None, alias="price.min", description="Minimum price")
    price_max: float | None = Field(default=None, alias="price.max", description="Maximum price")
    price_type: str | None = Field(default=None, alias="price.type", description="Hash type for price")
    offline: bool | None = Field(default=None, description="Show offline rigs")
    rented: bool | None = Field(default=None, description="Show rented")
    region_type: str | None = Field(default=None, alias="region.type", description="'include' or 'exclude'")
    expdiff: float | None = Field(default=None, description="Expected worker difficulty")
    count: int | None = Field(default=None, description="Number of results (max. 100)")
    islive: str | None = Field(default=None, description="Filter for rigs with hashrate [yes]")
    xnonce: str | None = Field(default=None, description="Filter by xnonce [yes,no]")
    offset: int | None = Field(default=None, description="Pagination offset")
    orderby: str | None = Field(default=None, description="Sorting")
    orderdir: str | None = Field(default=None, description="Direction [asc,desc]")


class RigCreateBody(BaseMRRModel):
    """Request body for PUT /rig.

    Used to create a new rig.

    Attributes:
        name: Rig name (required).
        description: Rig description.
        status: 'enabled' or 'disabled'.
        server: Server name (required, see /info/servers).
        price_btc_enabled: Enable BTC pricing. Default true.
        price_btc_price: Rig price per day (BTC).
        price_btc_autoprice: Enable auto-pricing.
        price_btc_minimum: Minimum auto-pricer price.
        price_btc_modifier: Percentage +/- for auto-pricing.
        price_ltc_enabled: Enable LTC pricing. Default true.
        price_eth_enabled: Enable ETH pricing. Default true.
        price_doge_enabled: Enable DOGE pricing. Default true.
        price_type: Hash type: [hash,kh,mh,gh,th,ph,eh]. Default mh.
        minhours: Minimum hours.
        maxhours: Maximum hours.
        extensions: Allow rental extension. Default true.
        hash_hash: Advertised hashrate.
        hash_type: Hash type. Default mh.
        suggested_diff: Suggested difficulty.
        ndevices: Number of devices (workers).
    """

    name: str = Field(..., description="Rig name")
    description: str | None = Field(default=None, description="Description")
    status: str | None = Field(default=None, description="'enabled' or 'disabled'")
    server: str = Field(..., description="Server name")
    price_btc_enabled: bool | None = Field(default=None, alias="price.btc.enabled", description="Enable BTC pricing")
    price_btc_price: float | None = Field(default=None, alias="price.btc.price", description="Rig price per day (BTC)")
    price_btc_autoprice: bool | None = Field(
        default=None, alias="price.btc.autoprice", description="Enable auto-pricing"
    )
    price_btc_minimum: float | None = Field(
        default=None, alias="price.btc.minimum", description="Minimum auto-pricer price"
    )
    price_btc_modifier: str | None = Field(
        default=None, alias="price.btc.modifier", description="Percentage +/- for auto-pricing"
    )
    price_ltc_enabled: bool | None = Field(default=None, alias="price.ltc.enabled", description="Enable LTC pricing")
    price_eth_enabled: bool | None = Field(default=None, alias="price.eth.enabled", description="Enable ETH pricing")
    price_doge_enabled: bool | None = Field(default=None, alias="price.doge.enabled", description="Enable DOGE pricing")
    price_type: str | None = Field(default=None, alias="price.type", description="Hash type: [hash,kh,mh,gh,th,ph,eh]")
    minhours: float | None = Field(default=None, description="Minimum hours")
    maxhours: float | None = Field(default=None, description="Maximum hours")
    extensions: bool | None = Field(default=None, description="Allow rental extension")
    hash_hash: float | None = Field(default=None, alias="hash.hash", description="Advertised hashrate")
    hash_type: str | None = Field(default=None, alias="hash.type", description="Hash type")
    suggested_diff: float | None = Field(default=None, description="Suggested difficulty")
    ndevices: int | None = Field(default=None, description="Number of devices (workers)")


class RigBatchBody(BaseMRRModel):
    """Request body for POST /rig/batch.

    Used for batch updating rigs.

    Attributes:
        rigs: List of rigs to update with fields id, name, status, etc.
    """

    rigs: list[dict[str, object]] = Field(..., description="List of rigs to update")


class RigExtendBody(BaseMRRModel):
    """Request body for PUT /rig/{ids}/extend.

    Used to extend rig rental (for owners).

    Attributes:
        hours: Hours to extend.
        minutes: Minutes to extend.
    """

    hours: float | None = Field(default=None, description="Hours to extend")
    minutes: float | None = Field(default=None, description="Minutes to extend")


class RigPoolBody(BaseMRRModel):
    """Request body for PUT /rig/{ids}/pool.

    Used to add or replace a pool on rigs.

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

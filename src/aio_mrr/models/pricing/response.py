"""Response models for Pricing API.

This module contains models for responses from the Pricing API:
- ConversionRates — currency conversion rates relative to BTC
- MarketRates — market rates for algorithms in different currencies
- PricingInfo — general response for GET /pricing
"""

from __future__ import annotations

from aio_mrr.models.base import BaseMRRModel


class ConversionRates(BaseMRRModel):
    """Currency conversion rates relative to BTC.

    Used in GET /pricing response.

    Attributes:
        LTC: Litecoin to BTC conversion rate.
        ETH: Ethereum to BTC conversion rate.
        BCH: Bitcoin Cash to BTC conversion rate.
        DOGE: Dogecoin to BTC conversion rate.
    """

    LTC: str
    ETH: str
    BCH: str
    DOGE: str


class MarketRate(BaseMRRModel):
    """Market rate for a single algorithm across different currencies.

    Attributes:
        BTC: Price in BTC.
        LTC: Price in LTC.
        ETH: Price in ETH.
        BCH: Price in BCH.
        DOGE: Price in DOGE.
    """

    BTC: str
    LTC: str
    ETH: str
    BCH: str
    DOGE: str


class MarketRates(BaseMRRModel):
    """Market rates for mining algorithms.

    Used in GET /pricing response. Each currency (BTC, LTC, ETH, BCH, DOGE)
    has its own rate for each algorithm.

    Attributes:
        allium: Market rates for Allium algorithm.
        argon2dchukwa: Market rates for Argon2/Chukwa algorithm.
        autolykosv2: Market rates for Autolykos v2 (ERGO) algorithm.
        kawpow: Market rates for KawPOW (RVN) algorithm.
        kheavyhash: Market rates for kHeavyHash (Kaspa) algorithm.
        randomx: Market rates for RandomX (XMR) algorithm.
        scrypt: Market rates for Scrypt algorithm.
        sha256: Market rates for SHA256 algorithm.
        x11: Market rates for X11 algorithm.
    """

    allium: MarketRate
    argon2dchukwa: MarketRate
    autolykosv2: MarketRate
    kawpow: MarketRate
    kheavyhash: MarketRate
    randomx: MarketRate
    scrypt: MarketRate
    sha256: MarketRate
    x11: MarketRate


class PricingInfo(BaseMRRModel):
    """Pricing information for GET /pricing.

    Response from MiningRigRentals API for obtaining market pricing rates.

    Attributes:
        conversion_rates: Currency conversion rates relative to BTC.
        market_rates: Market rates for algorithms in different currencies.
    """

    conversion_rates: ConversionRates
    market_rates: MarketRates

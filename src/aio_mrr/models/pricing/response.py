"""Response модели для Pricing API.

Этот модуль содержит модели для ответов от Pricing API:
- ConversionRates — курсы конвертации валют относительно BTC
- MarketRates — рыночные ставки по алгоритмам в разных валютах
- PricingInfo — общий ответ для GET /pricing
"""

from __future__ import annotations

from aio_mrr.models.base import BaseMRRModel


class ConversionRates(BaseMRRModel):
    """Курсы конвертации валют относительно BTC.

    Используется в ответе GET /pricing.

    Attributes:
        LTC: Курс конвертации Litecoin в BTC.
        ETH: Курс конвертации Ethereum в BTC.
        BCH: Курс конвертации Bitcoin Cash в BTC.
        DOGE: Курс конвертации Dogecoin в BTC.
    """

    LTC: str
    ETH: str
    BCH: str
    DOGE: str


class MarketRate(BaseMRRModel):
    """Рыночная ставка для одного алгоритма в разных валютах.

    Attributes:
        BTC: Цена в BTC.
        LTC: Цена в LTC.
        ETH: Цена в ETH.
        BCH: Цена в BCH.
        DOGE: Цена в DOGE.
    """

    BTC: str
    LTC: str
    ETH: str
    BCH: str
    DOGE: str


class MarketRates(BaseMRRModel):
    """Рыночные ставки по алгоритмам майнинга.

    Используется в ответе GET /pricing. Каждая валюта (BTC, LTC, ETH, BCH, DOGE)
    имеет свою ставку для каждого алгоритма.

    Attributes:
        allium: Рыночные ставки для алгоритма Allium.
        argon2dchukwa: Рыночные ставки для алгоритма Argon2/Chukwa.
        autolykosv2: Рыночные ставки для алгоритма Autolykos v2 (ERGO).
        kawpow: Рыночные ставки для алгоритма KawPOW (RVN).
        kheavyhash: Рыночные ставки для алгоритма kHeavyHash (Kaspa).
        randomx: Рыночные ставки для алгоритма RandomX (XMR).
        scrypt: Рыночные ставки для алгоритма Scrypt.
        sha256: Рыночные ставки для алгоритма SHA256.
        x11: Рыночные ставки для алгоритма X11.
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
    """Информация о ценообразовании для GET /pricing.

    Ответ от API MiningRigRentals для получения рыночных ставок ценообразования.

    Attributes:
        conversion_rates: Курсы конвертации валют относительно BTC.
        market_rates: Рыночные ставки по алгоритмам в разных валютах.
    """

    conversion_rates: ConversionRates
    market_rates: MarketRates

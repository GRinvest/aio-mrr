"""Response модели для Info API.

Этот модуль содержит модели для ответов от Info API:
- ServersList — ответ для GET /info/servers
- AlgoInfo — ответ для GET /info/algos и GET /info/algos/{name}
- CurrencyInfo — ответ для GET /info/currencies
"""

from typing import Any

from pydantic import field_validator

from aio_mrr.models.base import BaseMRRModel


def _parse_float_or_none(value: Any) -> float | None:
    """Parse float value, returning None for empty strings."""
    if value == "" or value is None:
        return None
    return float(value)


class HashInfo(BaseMRRModel):
    """Информация о хешрэйте.

    Attributes:
        hash: Значение хешрейта.
        unit: Единица измерения (mh, th, etc.).
        nice: Человекочитаемое представление (например, "882.70G").
    """

    hash: float | None = None
    unit: str
    nice: str

    @field_validator("hash", mode="before")
    @classmethod
    def parse_hash(cls, v: Any) -> float | None:
        return _parse_float_or_none(v)


class PriceInfo(BaseMRRModel):
    """Информация о цене.

    Attributes:
        amount: Значение цены.
        currency: Валюта (BTC, LTC, ETH, DOGE, BCH).
        unit: Единица измерения (например, "mh*day", "th*day").
    """

    amount: str
    currency: str
    unit: str


class AvailableHashInfo(BaseMRRModel):
    """Информация о доступном хешрэйте.

    Attributes:
        rigs: Количество доступных ригов.
        hash: Информация о хешрэйте.
    """

    rigs: str
    hash: HashInfo


class RentedHashInfo(BaseMRRModel):
    """Информация об арендованном хешрэйте.

    Attributes:
        rigs: Количество арендованных ригов.
        hash: Информация о хешрэйте.
    """

    rigs: str
    hash: HashInfo


class PricesInfo(BaseMRRModel):
    """Информация о ценах.

    Attributes:
        lowest: Самая низкая цена.
        last_10: Цена последних 10 аренд.
        last: Последняя цена.
    """

    lowest: PriceInfo
    last_10: PriceInfo
    last: PriceInfo


class AlgoStats(BaseMRRModel):
    """Статистика для алгоритма.

    Attributes:
        available: Информация о доступном хешрэйте.
        rented: Информация об арендованном хешрэйте.
        prices: Информация о ценах.
    """

    available: AvailableHashInfo
    rented: RentedHashInfo
    prices: PricesInfo


# --- Основные модели ---


class AlgoInfo(BaseMRRModel):
    """Информация об алгоритме майнинга.

    Используется для ответов:
    - GET /info/algos (список алгоритмов)
    - GET /info/algos/{name} (один алгоритм)

    Attributes:
        name: Название алгоритма (например, "scrypt", "sha256").
        display: Отображаемое название (например, "Scrypt").
        suggested_price: Рекомендуемая цена.
        stats: Статистика по алгоритму.
    """

    name: str
    display: str
    suggested_price: PriceInfo
    stats: AlgoStats


class ServerInfo(BaseMRRModel):
    """Информация о сервере MRR.

    Attributes:
        id: Идентификатор сервера.
        name: Имя сервера (например, "us-central01.miningrigrentals.com").
        region: Регион сервера (например, "us-central", "eu-ru").
        port: Порт для подключения (устаревшее поле).
        ethereum_port: Порт для Ethereum (устаревшее поле).
    """

    id: str
    name: str
    region: str
    port: str | None = None
    ethereum_port: str | None = None


class ServersList(BaseMRRModel):
    """Список серверов MRR.

    Ответ для GET /info/servers.

    Attributes:
        servers: Список информации о серверах.
    """

    servers: list[ServerInfo]


class CurrencyInfo(BaseMRRModel):
    """Информация о валюте.

    Используется для ответа GET /info/currencies.

    Attributes:
        name: Название валюты (например, "BTC", "LTC").
        enabled: Флаг доступности валюты для платежей.
        txfee: Комиссия за вывод средств.
    """

    name: str
    enabled: bool
    txfee: str

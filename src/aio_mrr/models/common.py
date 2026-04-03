"""Общие модели данных для библиотеки aio-mrr.

Этот модуль содержит общие модели, которые используются в нескольких местах:
- HashInfo: информация о хешрейте
- PriceInfo: информация о цене
- PoolInfo: информация о пуле
- ServerInfo: информация о сервере
"""

from __future__ import annotations

from .base import BaseMRRModel


class HashInfo(BaseMRRModel):
    """Информация о хешрейте.

    Используется для представления хешрейта в различных контекстах
    (алгоритмы, rig, rental и т.д.).

    Attributes:
        hash: Значение хешрейта.
        unit: Единица измерения (например, "mh", "th").
        nice: Человекочитаемое представление (например, "882.70G").
    """

    hash: float
    unit: str
    nice: str


class PriceInfo(BaseMRRModel):
    """Информация о цене.

    Используется для представления цены алгоритма или хешрейта.

    Attributes:
        amount: Значение цены.
        currency: Валюта цены (например, "BTC", "LTC", "ETH").
        unit: Единица измерения цены (например, "mh*day", "th*day").
    """

    amount: str
    currency: str
    unit: str


class PoolInfo(BaseMRRModel):
    """Информация о пуле.

    Используется для представления информации о майнинг-пуле.
    Может использоваться в контексте профиля, rig, rental.

    Attributes:
        priority: Приоритет пула (0-4).
        type: Тип алгоритма пула (например, "scrypt", "sha256").
        host: Хост пула.
        port: Порт пула.
        user: Имя пользователя/worker.
        pass_: Пароль worker.
        status: Статус пула (опционально, может быть пустым).
    """

    priority: int
    type: str
    host: str
    port: str
    user: str
    pass_: str
    status: str | None = None


class ServerInfo(BaseMRRModel):
    """Информация о сервере MRR.

    Используется для представления информации о серверах MiningRigRentals.

    Attributes:
        id: Идентификатор сервера.
        name: Название сервера (hostname).
        region: Регион сервера (например, "us-central", "eu-ru").
        port: Порт для подключения (опционально, устаревшее поле).
        ethereum_port: Порт для Ethereum (опционально, устаревшее поле).
    """

    id: str
    name: str
    region: str
    port: str | None = None
    ethereum_port: str | None = None

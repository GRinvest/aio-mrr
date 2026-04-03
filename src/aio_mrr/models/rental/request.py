"""Request модели для Rental API.

Этот модуль содержит модели для query параметров и body запросов к Rental API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel


class RentalListQueryParams(BaseMRRModel):
    """Query параметры для GET /rental.

    Используется для получения списка аренд с фильтрацией и пагинацией.

    Attributes:
        type: Тип аренды - 'owner' или 'renter'. По умолчанию 'renter'.
        algo: Фильтр по алгоритму.
        history: true = завершённые, false = активные. По умолчанию false.
        rig: Фильтр по rig ID.
        start: Старт пагинации. По умолчанию 0.
        limit: Лимит пагинации. По умолчанию 25.
        currency: Валюта - [BTC,LTC,ETH,DOGE,BCH].
    """

    type: str | None = Field(default=None, description="Тип аренды - 'owner' или 'renter'")
    algo: str | None = Field(default=None, description="Фильтр по алгоритму")
    history: bool | None = Field(default=None, description="true = завершённые, false = активные")
    rig: int | None = Field(default=None, description="Фильтр по rig ID")
    start: int | None = Field(default=None, description="Старт пагинации")
    limit: int | None = Field(default=None, description="Лимит пагинации")
    currency: str | None = Field(default=None, description="Валюта - [BTC,LTC,ETH,DOGE,BCH]")


class RentalCreateBody(BaseMRRModel):
    """Body запроса для PUT /rental.

    Используется для создания новой аренды.

    Attributes:
        rig: ID rig для аренды (обязательное).
        length: Длительность в часах (обязательное).
        profile: ID профиля пула (обязательное).
        currency: Валюта оплаты. По умолчанию BTC.
        rate_type: Тип хеша. По умолчанию 'mh'.
        rate_price: Цена за единицу хеша в день.
    """

    model_config = ConfigDict(populate_by_name=True)

    rig: int = Field(..., description="ID rig для аренды")
    length: float = Field(..., description="Длительность в часах")
    profile: int = Field(..., description="ID профиля пула")
    currency: str | None = Field(default=None, description="Валюта оплаты")
    rate_type: str | None = Field(default=None, alias="rate.type", description="Тип хеша")
    rate_price: float | None = Field(default=None, alias="rate.price", description="Цена за единицу хеша в день")


class RentalExtendBody(BaseMRRModel):
    """Body запроса для PUT /rental/{ids}/extend.

    Используется для продления аренды.

    Attributes:
        length: Часы для продления (обязательное).
        getcost: Если установлено, симулирует продление и возвращает стоимость.
    """

    length: float = Field(..., description="Часы для продления")
    getcost: bool | None = Field(default=None, description="Симулировать продление и вернуть стоимость")


class RentalPoolBody(BaseMRRModel):
    """Body запроса для PUT /rental/{ids}/pool.

    Используется для добавления или замены пула на арендах.

    Attributes:
        host: Хост пула (обязательное).
        port: Порт пула (обязательное).
        user: Имя worker (обязательное).
        pass: Пароль worker (обязательное).
        priority: Приоритет (0-4).
    """

    host: str = Field(..., description="Хост пула")
    port: int = Field(..., description="Порт пула")
    user: str = Field(..., description="Имя worker")
    password: str = Field(..., alias="pass", description="Пароль worker")
    priority: int | None = Field(default=None, description="Приоритет (0-4)")

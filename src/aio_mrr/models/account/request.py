"""Request модели для Account API.

Этот модуль содержит модели для query параметров и body запросов к Account API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel


class TransactionsQueryParams(BaseMRRModel):
    """Query параметры для GET /account/transactions.

    Используется для получения и фильтрации истории транзакций.

    Attributes:
        start: Старт пагинации. По умолчанию 0.
        limit: Лимит записей. По умолчанию 100.
        algo: Фильтр по алгоритму.
        type: Тип транзакции (credit, payout, referral, deposit, payment,
              credit/refund, debit/refund, rental fee).
        rig: Фильтр по rig ID.
        rental: Фильтр по rental ID.
        txid: Фильтр по txid.
        time_greater_eq: Время >= (Unix timestamp).
        time_less_eq: Время <= (Unix timestamp).
    """

    start: int | None = Field(default=None, description="Старт пагинации")
    limit: int | None = Field(default=None, description="Лимит записей")
    algo: str | None = Field(default=None, description="Фильтр по алгоритму")
    type: str | None = Field(default=None, description="Тип транзакции")
    rig: int | None = Field(default=None, description="Фильтр по rig ID")
    rental: int | None = Field(default=None, description="Фильтр по rental ID")
    txid: str | None = Field(default=None, description="Фильтр по txid")
    time_greater_eq: str | None = Field(default=None, description="Время >= (Unix timestamp)")
    time_less_eq: str | None = Field(default=None, description="Время <= (Unix timestamp)")


class ProfileCreateBody(BaseMRRModel):
    """Body запроса для PUT /account/profile.

    Используется для создания нового профиля пула.

    Attributes:
        name: Название профиля (обязательное).
        algo: Алгоритм профиля (обязательное).
    """

    name: str = Field(..., description="Название профиля")
    algo: str = Field(..., description="Алгоритм профиля")


class PoolTestBody(BaseMRRModel):
    """Body запроса для PUT /account/pools/test.

    Используется для тестирования подключения к пулу.

    Attributes:
        method: Метод теста (simple или full).
        extramethod: Для ethhash: [esm0,esm1,esm2,esm3]. По умолчанию esm0.
        type: Алгоритм (scrypt, sha256, x11). Требуется для full метода.
        host: Хост пула (может включать порт).
        port: Порт пула. Требуется если нет в host.
        user: Имя пользователя. Требуется для full метода.
        pass: Пароль. Требуется для full метода.
        source: Сервер MRR для теста. По умолчанию us-central01.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    method: str = Field(..., description="Метод теста (simple или full)")
    extramethod: str | None = Field(default=None, description="Для ethhash: [esm0,esm1,esm2,esm3]")
    type: str | None = Field(default=None, description="Алгоритм (для full метода)")
    host: str | None = Field(default=None, description="Хост пула")
    port: int | None = Field(default=None, description="Порт пула")
    user: str | None = Field(default=None, description="Имя пользователя")
    password: str | None = Field(default=None, alias="pass", description="Пароль")
    source: str | None = Field(default=None, description="Сервер MRR для теста")


class PoolCreateBody(BaseMRRModel):
    """Body запроса для PUT /account/pool.

    Используется для создания сохранённого пула.

    Attributes:
        type: Алгоритм (sha256, scrypt, x11 и т.д.) (обязательное).
        name: Название для идентификации (обязательное).
        host: Хост пула (обязательное).
        port: Порт пула (обязательное).
        user: Имя worker (обязательное).
        pass: Пароль worker (опциональное).
        notes: Заметки (опциональное).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type: str = Field(..., description="Алгоритм пула")
    name: str = Field(..., description="Название пула")
    host: str = Field(..., description="Хост пула")
    port: int = Field(..., description="Порт пула")
    user: str = Field(..., description="Имя worker")
    password: str | None = Field(default=None, alias="pass", description="Пароль worker")
    notes: str | None = Field(default=None, description="Заметки")

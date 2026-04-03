"""Response модели для Rig API.

Этот модуль содержит модели для ответов от Rig API.
"""

from typing import Any

from pydantic import Field, field_validator

from aio_mrr.models.base import BaseMRRModel


class RigPriceInfo(BaseMRRModel):
    """Информация о цене rig.

    Attributes:
        enabled: Включено ли ценообразование.
        price: Цена rig в день.
        autoprice: Включено ли автоценообразование.
        minimum: Минимальная цена автоценообразователя.
        modifier: Процент +/- для автоценообразования.
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
    """Информация о хешрэйте rig.

    Attributes:
        hash: Хешрейт.
        type: Тип хеша (hash,kh,mh,gh,th,ph,eh).
    """

    hash: float | None = None
    type: str | None = None


class RigInfo(BaseMRRModel):
    """Информация о rig.

    Используется для ответов:
    - GET /rig
    - GET /rig/mine
    - GET /rig/{ids}

    Attributes:
        id: Идентификатор rig.
        name: Название rig.
        description: Описание rig.
        server: Имя сервера.
        status: Статус rig (enabled/disabled).
        price: Информация о цене по валютам.
        price_type: Тип хеша для цены.
        minhours: Минимальное количество часов.
        maxhours: Максимальное количество часов.
        extensions: Разрешено ли продление аренды.
        hash: Информация о хешрэйте.
        suggested_diff: Рекомендуемая сложность.
        ndevices: Количество устройств (workers).
        type: Алгоритм (sha256, scrypt и т.д.).
        region: Регион.
        online: Статус онлайн.
        rented: Статус аренды.
        last_hashrate: Последний хешрейт.
        rpi: RPI рейтинг (0-100).
        owner: Владелец rig.
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
    """Список rig'ов.

    Ответ для GET /rig, GET /rig/mine, GET /rig/{ids}.
    API возвращает список напрямую, но эта модель для типизации.

    Attributes:
        rigs: Список rig'ов.
    """

    rigs: list[RigInfo] = Field(..., description="Список rig'ов")


class RigPortInfo(BaseMRRModel):
    """Информация о портах для rig.

    Ответ для GET /rig/{ids}/port.

    Attributes:
        rigid: ID rig.
        port: Прямой номер порта для подключения к серверу.
        server: Имя сервера.
        worker: Имя worker для подключения.
    """

    rigid: str | None = None
    port: int
    server: str | None = None
    worker: str | None = None


class RigThreadDetail(BaseMRRModel):
    """Детали одного thread'а.

    Attributes:
        id: Идентификатор thread.
        worker: Имя worker.
        status: Статус thread.
        hashrate: Текущий хешрейт.
        last_share: Время последней работы.
    """

    id: int | None = None
    worker: str | None = None
    status: str | None = None
    hashrate: float | None = None
    last_share: str | None = None


class RigThreadInfo(BaseMRRModel):
    """Информация о thread'ах для rig.

    Ответ для GET /rig/{ids}/threads — возвращает список rig-групп с threads.

    Attributes:
        rigid: ID rig.
        access: Уровень доступа (owner/renter).
        threads: Список деталей thread'ов.
    """

    rigid: str | None = None
    access: str | None = None
    threads: list[RigThreadDetail] = []


class RigGraphData(BaseMRRModel):
    """Графические данные rig.

    Ответ для GET /rig/{ids}/graph.

    Attributes:
        rigid: ID rig.
        chartdata: Данные графика (time_start, time_end, timestamp_start, timestamp_end, bars).
    """

    rigid: str | None = None
    chartdata: dict[str, Any] | None = None

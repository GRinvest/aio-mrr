"""Response модели для Rig API.

Этот модуль содержит модели для ответов от Rig API.
"""

from pydantic import Field

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
    modifier: str | None = None


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
    status: str | None = None
    price: dict[str, RigPriceInfo] | None = None
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
    rpi: int | None = None
    owner: str | None = None


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
        port: Прямой номер порта для подключения к серверу.
    """

    port: int = Field(..., description="Прямой номер порта")


class RigThreadInfo(BaseMRRModel):
    """Информация о thread'ах для rig.

    Используется для ответа GET /rig/{ids}/threads.

    Attributes:
        id: Идентификатор thread.
        rig_id: ID rig.
        worker: Имя worker.
        status: Статус thread.
        hashrate: Текущий хешрейт.
        last_share: Время последней работы.
    """

    id: int
    rig_id: int
    worker: str
    status: str
    hashrate: float | None = None
    last_share: str | None = None


class RigGraphDataPoint(BaseMRRModel):
    """Точка данных на графике rig.

    Attributes:
        time: Timestamp.
        hashrate: Хешрейт в точке.
        downtime: Флаг простоя.
    """

    time: str
    hashrate: float | None = None
    downtime: bool | None = None


class RigGraphData(BaseMRRModel):
    """Графические данные rig.

    Ответ для GET /rig/{ids}/graph.

    Attributes:
        hashrate_data: История хешрейта.
        downtime_data: История простоев.
        hours: Количество часов данных.
    """

    hashrate_data: list[RigGraphDataPoint] | None = None
    downtime_data: list[RigGraphDataPoint] | None = None
    hours: float | None = None

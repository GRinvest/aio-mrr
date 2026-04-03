"""Response модели для Rental API.

Этот модуль содержит модели для ответов от Rental API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel


class RateInfo(BaseMRRModel):
    """Информация о ставке аренды.

    Attributes:
        type: Тип хеша (mh, gh и т.д.).
        price: Цена за единицу хеша в день.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: str | None = Field(default=None, alias="rate.type", description="Тип хеша")
    price: str | None = Field(default=None, alias="rate.price", description="Цена за единицу хеша в день")


class RentalHashInfo(BaseMRRModel):
    """Информация о хешрэйте аренды.

    Attributes:
        hash: Хешрейт.
        type: Тип хеша (hash, kh, mh, gh и т.д.).
    """

    hash: float | None = Field(default=None, description="Хешрейт")
    type: str | None = Field(default=None, description="Тип хеша")


class RentalCostInfo(BaseMRRModel):
    """Информация о стоимости аренды.

    Attributes:
        amount: Сумма стоимости.
        currency: Валюта стоимости.
    """

    amount: str | None = Field(default=None, description="Сумма стоимости")
    currency: str | None = Field(default=None, description="Валюта стоимости")


class RentalInfo(BaseMRRModel):
    """Информация об аренде.

    Используется для ответов:
    - GET /rental
    - GET /rental/{ids}

    Attributes:
        id: Идентификатор аренды.
        rig_id: ID rig.
        rig_name: Название rig.
        owner: Имя владельца rig.
        renter: Имя арендатора.
        status: Статус аренды (active и т.д.).
        started: Время начала аренды.
        ends: Время окончания аренды.
        length: Длительность в часах.
        currency: Валюта оплаты.
        rate: Информация о ставке.
        hash: Информация о хешрэйте.
        cost: Информация о стоимости.
    """

    id: str = Field(..., description="Идентификатор аренды")
    rig_id: str | None = Field(default=None, alias="rig_id", description="ID rig")
    rig_name: str | None = Field(default=None, description="Название rig")
    owner: str | None = Field(default=None, description="Имя владельца rig")
    renter: str | None = Field(default=None, description="Имя арендатора")
    status: str | None = Field(default=None, description="Статус аренды")
    started: str | None = Field(default=None, description="Время начала аренды")
    ends: str | None = Field(default=None, description="Время окончания аренды")
    length: float | None = Field(default=None, description="Длительность в часах")
    currency: str | None = Field(default=None, description="Валюта оплаты")
    rate: RateInfo | None = Field(default=None, description="Rate information")
    hash: RentalHashInfo | None = Field(default=None, description="Hash information")
    cost: RentalCostInfo | None = Field(default=None, description="Cost information")


class RentalList(BaseMRRModel):
    """Список аренд.

    Ответ для GET /rental.

    Attributes:
        rentals: Список аренд.
    """

    rentals: list[RentalInfo] = Field(..., description="Список аренд")


class RentalLogEntry(BaseMRRModel):
    """Запись журнала активности аренды.

    Используется для ответа GET /rental/{ids}/log.

    Attributes:
        time: Время записи.
        message: Сообщение события.
    """

    time: str = Field(..., description="Время записи")
    message: str = Field(..., description="Сообщение события")


class RentalMessage(BaseMRRModel):
    """Сообщение аренды.

    Используется для ответа GET /rental/{ids}/message.

    Attributes:
        time: Время сообщения.
        user: Имя пользователя, отправившего сообщение.
        message: Текст сообщения.
    """

    time: str = Field(..., description="Время сообщения")
    user: str = Field(..., description="Имя пользователя")
    message: str = Field(..., description="Текст сообщения")


class GraphDataPoint(BaseMRRModel):
    """Точка данных на графике аренды.

    Attributes:
        time: Timestamp.
        hashrate: Хешрейт в точке.
        downtime: Флаг простоя.
    """

    time: str | None = Field(default=None, description="Timestamp")
    hashrate: float | None = Field(default=None, description="Хешрейт")
    downtime: bool | None = Field(default=None, description="Флаг простоя")


class GraphData(BaseMRRModel):
    """Графические данные аренды.

    Ответ для GET /rental/{ids}/graph.

    Attributes:
        hashrate_data: История хешрейта.
        downtime_data: История простоев.
        hours: Количество часов данных.
    """

    hashrate_data: list[GraphDataPoint] | None = Field(default=None, description="История хешрейта")
    downtime_data: list[GraphDataPoint] | None = Field(default=None, description="История простоев")
    hours: float | None = Field(default=None, description="Количество часов данных")

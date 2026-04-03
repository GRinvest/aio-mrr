"""Request модели для RigGroup API.

Этот модуль содержит модели для request данных RigGroup API:
- RigGroupCreateBody — тело запроса для PUT /riggroup
- RigGroupUpdateBody — тело запроса для PUT /riggroup/{id}
"""

from pydantic import Field

from aio_mrr.models.base import BaseMRRModel


class RigGroupCreateBody(BaseMRRModel):
    """Тело запроса для создания новой группы rig'ов (PUT /riggroup).

    Attributes:
        name: Название группы. Обязательное поле.
        enabled: Флаг включения группы. По умолчанию True.
        rental_limit: Лимит активных аренд. По умолчанию 1.
    """

    name: str = Field(..., description="Название группы")
    enabled: bool = Field(default=True, description="Включена/отключена группа")
    rental_limit: int = Field(default=1, description="Лимит активных аренд")


class RigGroupUpdateBody(BaseMRRModel):
    """Тело запроса для обновления группы rig'ов (PUT /riggroup/{id}).

    Все поля опциональные — можно обновлять только нужные.

    Attributes:
        name: Новое название группы (опционально).
        enabled: Новый статус включения (опционально).
        rental_limit: Новый лимит аренд (опционально).
    """

    name: str | None = Field(default=None, description="Новое название группы")
    enabled: bool | None = Field(default=None, description="Новый статус включения")
    rental_limit: int | None = Field(default=None, description="Новый лимит аренд")

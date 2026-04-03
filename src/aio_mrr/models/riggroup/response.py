"""Response модели для RigGroup API.

Этот модуль содержит модели для ответов RigGroup API:
- RigGroupInfo — информация о группе rig'ов
- RigGroupList — список групп rig'ов
"""

from aio_mrr.models.base import BaseMRRModel


class RigGroupInfo(BaseMRRModel):
    """Информация о группе rig'ов.

    Используется для ответов:
    - GET /riggroup (в списке)
    - GET /riggroup/{id} (одна группа)

    Attributes:
        id: Идентификатор группы.
        name: Название группы.
        enabled: Флаг включения группы.
        rental_limit: Лимит активных аренд.
        rigs: Список идентификаторов rig'ов в группе.
        algo: Алгоритм майнинга группы (опционально).
    """

    id: str
    name: str
    enabled: bool
    rental_limit: int
    rigs: list[int]
    algo: str | None = None


class RigGroupList(BaseMRRModel):
    """Список групп rig'ов.

    Ответ для GET /riggroup.

    Attributes:
        groups: Список информации о группах rig'ов.
    """

    groups: list[RigGroupInfo]

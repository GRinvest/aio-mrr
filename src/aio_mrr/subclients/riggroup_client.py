"""RigGroup Client для взаимодействия с RigGroup API.

Этот модуль предоставляет RigGroupClient для работы с RigGroup API endpoints:
- GET /riggroup — Получение списка групп rig'ов
- PUT /riggroup — Создание новой группы rig'ов
- GET /riggroup/{id} — Получение деталей группы rig'ов
- PUT /riggroup/{id} — Обновление группы rig'ов
- DELETE /riggroup/{id} — Удаление группы rig'ов
- POST /riggroup/{id}/add/{rig_ids} — Добавление rig'ов в группу
- POST /riggroup/{id}/remove/{rig_ids} — Удаление rig'ов из группы
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.riggroup.request import RigGroupCreateBody, RigGroupUpdateBody
from aio_mrr.models.riggroup.response import RigGroupInfo
from aio_mrr.subclients.base import BaseSubClient


class RigGroupClient(BaseSubClient):
    """Client для работы с RigGroup API.

    Предоставляет методы для управления группами майнинг-установок (rig groups):
    - создание и удаление групп
    - обновление информации о группах
    - добавление и удаление rig'ов из групп

    Пример использования:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.riggroup_client.get_list()
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует RigGroupClient.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        super().__init__(http_client)

    async def get_list(self) -> MRRResponse[list[RigGroupInfo]]:
        """Получает список ваших групп rig'ов.

        Returns:
            MRRResponse[list[RigGroupInfo]] — ответ со списком групп:
            - При успехе: MRRResponse(success=True, data=[RigGroupInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await riggroup_client.get_list()
            >>> if response.success:
            ...     for group in response.data:
            ...         print(f"{group.id}: {group.name}")
        """
        endpoint = "/riggroup"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            groups_data: list[dict[str, Any]] = result.data
            groups = [RigGroupInfo.model_validate(g) for g in groups_data]
            return MRRResponse(
                success=True,
                data=groups,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_by_id(self, id: int) -> MRRResponse[RigGroupInfo]:
        """Получает детали группы rig'ов по ID.

        Args:
            id: Идентификатор группы rig'ов.

        Returns:
            MRRResponse[RigGroupInfo] — ответ с информацией о группе:
            - При успехе: MRRResponse(success=True, data=RigGroupInfo)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await riggroup_client.get_by_id(id=123)
            >>> if response.success:
            ...     print(f"Group: {response.data.name}, Rigs: {response.data.rigs}")
        """
        endpoint = f"/riggroup/{id}"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            group_data: dict[str, Any] = result.data
            group = RigGroupInfo.model_validate(group_data)
            return MRRResponse(
                success=True,
                data=group,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def create(self, body: RigGroupCreateBody) -> MRRResponse[dict[str, Any]]:
        """Создаёт новую группу rig'ов.

        Args:
            body: Тело запроса с параметрами создания группы.

        Returns:
            MRRResponse[dict] — ответ с ID созданной группы:
            - При успехе: MRRResponse(success=True, data={"id": 123, "message": "..."})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RigGroupCreateBody(name="My Scrypt Rigs", rental_limit=10)
            >>> response = await riggroup_client.create(body)
            >>> if response.success:
            ...     print(f"Group created with ID: {response.data['id']}")
        """
        endpoint = "/riggroup"
        body_dict = body.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body_dict)

        if result.success and result.data is not None:
            return MRRResponse(
                success=True,
                data=result.data,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def update(self, id: int, body: RigGroupUpdateBody) -> MRRResponse[None]:
        """Обновляет группу rig'ов.

        Args:
            id: Идентификатор группы rig'ов для обновления.
            body: Тело запроса с параметрами обновления (все поля опциональные).

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RigGroupUpdateBody(name="Updated Group Name", rental_limit=15)
            >>> response = await riggroup_client.update(id=123, body=body)
            >>> if response.success:
            ...     print("Group updated successfully")
        """
        endpoint = f"/riggroup/{id}"
        body_dict = body.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body_dict)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def delete(self, id: int) -> MRRResponse[dict[str, Any]]:
        """Удаляет группу rig'ов.

        Args:
            id: Идентификатор группы rig'ов для удаления.

        Returns:
            MRRResponse[dict] — ответ с подтверждением удаления:
            - При успехе: MRRResponse(success=True, data={"id": 123, "message": "..."})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await riggroup_client.delete(id=123)
            >>> if response.success:
            ...     print("Group deleted successfully")
        """
        endpoint = f"/riggroup/{id}"

        result = await self._http.request(method="DELETE", endpoint=endpoint)

        if result.success and result.data is not None:
            return MRRResponse(
                success=True,
                data=result.data,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def add_rigs(self, id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]:
        """Добавляет rig'и в группу.

        Args:
            id: Идентификатор группы rig'ов.
            rig_ids: Список ID rig'ов для добавления в группу.

        Returns:
            MRRResponse[dict] — ответ с подтверждением добавления:
            - При успехе: MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await riggroup_client.add_rigs(id=123, rig_ids=[12345, 12346])
            >>> if response.success:
            ...     print(f"Rigs added: {response.data['rigs']}")
        """
        rig_ids_str = ";".join(str(rig_id) for rig_id in rig_ids)
        endpoint = f"/riggroup/{id}/add/{rig_ids_str}"

        result = await self._http.request(method="POST", endpoint=endpoint)

        if result.success and result.data is not None:
            return MRRResponse(
                success=True,
                data=result.data,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def remove_rigs(self, id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]:
        """Удаляет rig'и из группы.

        Args:
            id: Идентификатор группы rig'ов.
            rig_ids: Список ID rig'ов для удаления из группы.

        Returns:
            MRRResponse[dict] — ответ с подтверждением удаления:
            - При успехе: MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await riggroup_client.remove_rigs(id=123, rig_ids=[12345, 12346])
            >>> if response.success:
            ...     print(f"Rigs removed: {response.data['rigs']}")
        """
        rig_ids_str = ";".join(str(rig_id) for rig_id in rig_ids)
        endpoint = f"/riggroup/{id}/remove/{rig_ids_str}"

        result = await self._http.request(method="POST", endpoint=endpoint)

        if result.success and result.data is not None:
            return MRRResponse(
                success=True,
                data=result.data,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

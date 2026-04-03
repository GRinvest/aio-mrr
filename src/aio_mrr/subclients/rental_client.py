"""Rental Client для взаимодействия с Rental API.

Этот модуль предоставляет RentalClient для работы с Rental API endpoints:
- GET /rental — Список аренд
- GET /rental/{ids} — Получение аренды по ID
- PUT /rental — Создание новой аренды
- PUT /rental/{ids}/profile — Применение профиля пула к арендам
- GET /rental/{ids}/pool — Получение пулов, назначенных арендам
- PUT /rental/{ids}/pool — Добавление или замена пула на арендах
- DELETE /rental/{ids}/pool — Удаление пула с аренд
- PUT /rental/{ids}/extend — Продление аренды
- GET /rental/{ids}/graph — Получение графических данных аренды
- GET /rental/{ids}/log — Получение журнала активности аренды
- GET /rental/{ids}/message — Получение сообщений аренды
- PUT /rental/{ids}/message — Отправка сообщения аренде
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.account.response import Pool
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.rental.request import RentalCreateBody, RentalPoolBody
from aio_mrr.models.rental.response import GraphData, RentalInfo, RentalLogEntry, RentalMessage
from aio_mrr.subclients.base import BaseSubClient


class RentalClient(BaseSubClient):
    """Client для работы с Rental API.

    Предоставляет методы для управления арендами майнинг-установок:
    - создание и получение аренд
    - управление пулами и профилями
    - продление аренды
    - получение статистики, графических данных и логов

    Пример использования:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.rental.get_list(params={"type": "renter"})
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует RentalClient.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        super().__init__(http_client)

    async def get_list(self, params: dict[str, Any] | None = None) -> MRRResponse[list[RentalInfo]]:
        """Получает список аренд с фильтрацией и пагинацией.

        Args:
            params: Query параметры для фильтрации:
                - type: 'owner' или 'renter'
                - algo: фильтр по алгоритму
                - history: true = завершённые, false = активные
                - rig: фильтр по rig ID
                - start: старт пагинации
                - limit: лимит пагинации
                - currency: валюта [BTC,LTC,ETH,DOGE,BCH]

        Returns:
            MRRResponse[list[RentalInfo]] — ответ со списком аренд:
            - При успехе: MRRResponse(success=True, data=[RentalInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.get_list(params={"type": "renter", "history": False})
            >>> if response.success:
            ...     for rental in response.data:
            ...         print(f"{rental.id}: {rental.status}")
        """
        endpoint = "/rental"
        query_params: dict[str, Any] = {}

        if params is not None:
            query_params = params

        result = await self._http.request(method="GET", endpoint=endpoint, params=query_params)

        if result.success and result.data is not None:
            rentals_data = result.data
            if isinstance(rentals_data, dict):
                rentals_list = rentals_data.get("rentals", [])
            else:
                rentals_list = rentals_data
            rentals = [RentalInfo.model_validate(r) for r in rentals_list]
            return MRRResponse(
                success=True,
                data=rentals,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_by_ids(self, ids: list[int]) -> MRRResponse[RentalInfo]:
        """Получает информацию об аренде по ID.

        Args:
            ids: Список ID аренд для получения (используется первый ID).

        Returns:
            MRRResponse[RentalInfo] — ответ с информацией об аренде:
            - При успехе: MRRResponse(success=True, data=RentalInfo)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.get_by_ids(ids=[54321])
            >>> if response.success:
            ...     print(f"Rental: {response.data.id}, Status: {response.data.status}")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            rental_data: dict[str, Any] = result.data
            rental = RentalInfo.model_validate(rental_data)
            return MRRResponse(
                success=True,
                data=rental,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def create(self, body: RentalCreateBody) -> MRRResponse[dict[str, Any]]:
        """Создаёт новую аренду.

        Args:
            body: Тело запроса с параметрами создания аренды:
                - rig: ID rig для аренды (обязательное)
                - length: длительность в часах (обязательное)
                - profile: ID профиля пула (обязательное)
                - currency: валюта оплаты (по умолчанию BTC)
                - rate_type: тип хеша (по умолчанию 'mh')
                - rate_price: цена за единицу хеша в день

        Returns:
            MRRResponse[dict] — ответ с ID созданной аренды:
            - При успехе: MRRResponse(success=True, data={"id": "54321"})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RentalCreateBody(rig=12345, length=24, profile=678, currency="BTC")
            >>> response = await rental_client.create(body)
            >>> if response.success:
            ...     print(f"Rental created with ID: {response.data['id']}")
        """
        endpoint = "/rental"
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

    async def update_profile(self, ids: list[int], profile: int) -> MRRResponse[None]:
        """Применяет профиль пула к арендам.

        Args:
            ids: Список ID аренд для обновления.
            profile: ID профиля для применения.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.update_profile(ids=[54321], profile=678)
            >>> if response.success:
            ...     print("Profile applied successfully")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/profile"
        body_dict = {"profile": profile}

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

    async def get_pools(self, ids: list[int]) -> MRRResponse[list[Pool]]:
        """Получает пулы, назначенные арендам.

        Args:
            ids: Список ID аренд для получения пулов.

        Returns:
            MRRResponse[list[Pool]] — ответ со списком пулов:
            - При успехе: MRRResponse(success=True, data=[Pool, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.get_pools(ids=[54321])
            >>> if response.success:
            ...     for pool in response.data:
            ...         print(f"{pool.name}: {pool.host}")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/pool"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            pools_data: list[dict[str, Any]] = result.data
            pools = [Pool.model_validate(p) for p in pools_data]
            return MRRResponse(
                success=True,
                data=pools,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def update_pool(self, ids: list[int], body: RentalPoolBody) -> MRRResponse[None]:
        """Добавляет или заменяет пул на арендах.

        Args:
            ids: Список ID аренд для обновления.
            body: Тело запроса с данными пула:
                - host: хост пула (обязательное)
                - port: порт пула (обязательное)
                - user: имя worker (обязательное)
                - password: пароль worker (обязательное)
                - priority: приоритет (0-4)

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RentalPoolBody(
            ...     host="pool.example.com",
            ...     port=3333,
            ...     user="worker1",
            ...     password="password",
            ...     priority=0,
            ... )
            >>> response = await rental_client.update_pool(ids=[54321], body=body)
            >>> if response.success:
            ...     print("Pool updated successfully")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/pool"
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

    async def delete_pool(self, ids: list[int]) -> MRRResponse[None]:
        """Удаляет пул с аренд.

        Удаляет пул с указанным приоритетом с аренд.

        Args:
            ids: Список ID аренд для удаления пула.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.delete_pool(ids=[54321])
            >>> if response.success:
            ...     print("Pool deleted successfully")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/pool"

        result = await self._http.request(method="DELETE", endpoint=endpoint)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def extend(self, ids: list[int], length: float, getcost: bool | None = None) -> MRRResponse[None]:
        """Покупает продление аренды.

        Args:
            ids: Список ID аренд для продления.
            length: часы для продления.
            getcost: если установлено, симулирует продление и возвращает стоимость.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            # Продление аренды
            >>> response = await rental_client.extend(ids=[54321], length=12)
            >>> if response.success:
            ...     print("Rental extended successfully")

            # Симуляция стоимости продления
            >>> response = await rental_client.extend(ids=[54321], length=12, getcost=True)
            >>> if response.success:
            ...     print("Cost simulation completed")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/extend"
        body_dict: dict[str, Any] = {"length": length}

        if getcost is not None:
            body_dict["getcost"] = getcost

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

    async def get_graph(
        self, ids: list[int], hours: float | None = None, interval: str | None = None
    ) -> MRRResponse[GraphData]:
        """Получает графические данные аренды (исторический хешрейт, простои).

        Args:
            ids: Список ID аренд (используется первый ID).
            hours: часы данных (макс. 2 недели). По умолчанию 168.
            interval: интервал данных. По умолчанию None.

        Returns:
            MRRResponse[GraphData] — ответ с графическими данными:
            - При успехе: MRRResponse(success=True, data=GraphData)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.get_graph(ids=[54321], hours=24)
            >>> if response.success:
            ...     print(f"Hours of data: {response.data.hours}")
            ...     print(f"Hashrate points: {len(response.data.hashrate_data or [])}")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/graph"
        params: dict[str, Any] = {}

        if hours is not None:
            params["hours"] = hours
        if interval is not None:
            params["interval"] = interval

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            graph_data: dict[str, Any] = result.data
            graph = GraphData.model_validate(graph_data)
            return MRRResponse(
                success=True,
                data=graph,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_log(self, ids: list[int]) -> MRRResponse[list[RentalLogEntry]]:
        """Получает журнал активности аренды.

        Args:
            ids: Список ID аренд для получения логов (используется первый ID).

        Returns:
            MRRResponse[list[RentalLogEntry]] — ответ со списком записей лога:
            - При успехе: MRRResponse(success=True, data=[RentalLogEntry, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.get_log(ids=[54321])
            >>> if response.success:
            ...     for log_entry in response.data:
            ...         print(f"{log_entry.time}: {log_entry.message}")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/log"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            logs_data: list[dict[str, Any]] = result.data
            logs = [RentalLogEntry.model_validate(log_entry) for log_entry in logs_data]
            return MRRResponse(
                success=True,
                data=logs,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_message(self, ids: list[int]) -> MRRResponse[list[RentalMessage]]:
        """Получает сообщения аренды.

        Args:
            ids: Список ID аренд для получения сообщений (используется первый ID).

        Returns:
            MRRResponse[list[RentalMessage]] — ответ со списком сообщений:
            - При успехе: MRRResponse(success=True, data=[RentalMessage, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.get_message(ids=[54321])
            >>> if response.success:
            ...     for msg in response.data:
            ...         print(f"{msg.time} [{msg.user}]: {msg.message}")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/message"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            messages_data: list[dict[str, Any]] = result.data
            messages = [RentalMessage.model_validate(m) for m in messages_data]
            return MRRResponse(
                success=True,
                data=messages,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def send_message(self, ids: list[int], message: str) -> MRRResponse[None]:
        """Отправляет сообщение аренде.

        Args:
            ids: Список ID аренд для отправки сообщения (используется первый ID).
            message: текст сообщения.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rental_client.send_message(ids=[54321], message="Please check the rig status")
            >>> if response.success:
            ...     print("Message sent successfully")
        """
        ids_str = ";".join(str(rental_id) for rental_id in ids)
        endpoint = f"/rental/{ids_str}/message"
        body_dict = {"message": message}

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

"""Rig Client для взаимодействия с Rig API.

Этот модуль предоставляет RigClient для работы с Rig API endpoints:
- GET /rig — Поиск rig'ов по алгоритму
- GET /rig/mine — Список ваших rig'ов
- GET /rig/{ids} — Получение rig'ов по ID
- PUT /rig — Создание нового rig
- POST /rig/batch — Пакетное обновление rig'ов
- DELETE /rig/{ids} — Удаление rig'ов
- PUT /rig/{ids}/extend — Продление аренды rig'а
- POST /rig/batch/extend — Пакетное продление аренды
- PUT /rig/{ids}/profile — Применение профиля пула к rig'ам
- GET /rig/{ids}/pool — Получение пулов, назначенных rig'ам
- PUT /rig/{ids}/pool — Добавление или замена пула на rig'ах
- DELETE /rig/{ids}/pool — Удаление пула с rig'ов
- GET /rig/{ids}/port — Получение прямого номера порта
- GET /rig/{ids}/threads — Получение списка активных threads
- GET /rig/{ids}/graph — Получение графических данных rig'а
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.account.response import Pool
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.rig.request import RigBatchBody, RigCreateBody, RigPoolBody
from aio_mrr.models.rig.response import RigGraphData, RigInfo, RigPortInfo, RigThreadInfo
from aio_mrr.subclients.base import BaseSubClient


class RigClient(BaseSubClient):
    """Client для работы с Rig API.

    Предоставляет методы для управления майнинг-установками (rigs):
    - поиск и фильтрация rig'ов
    - создание и удаление rig'ов
    - продление аренды
    - управление пулами и профилями
    - получение статистики и графических данных

    Пример использования:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.rig_client.search_rigs(type="scrypt")
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует RigClient.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        super().__init__(http_client)

    async def search_rigs(
        self,
        type: str,
        currency: str | None = None,
        minhours_min: int | None = None,
        minhours_max: int | None = None,
        maxhours_min: int | None = None,
        maxhours_max: int | None = None,
        rpi_min: int | None = None,
        rpi_max: int | None = None,
        hash_min: int | None = None,
        hash_max: int | None = None,
        hash_type: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        price_type: str | None = None,
        offline: bool | None = None,
        rented: bool | None = None,
        region_type: str | None = None,
        expdiff: float | None = None,
        count: int | None = None,
        islive: str | None = None,
        xnonce: str | None = None,
        offset: int | None = None,
        orderby: str | None = None,
        orderdir: str | None = None,
    ) -> MRRResponse[list[RigInfo]]:
        """Ищет rig'ы по алгоритму с фильтрацией и сортировкой.

        Аналогично основной странице списка rig'ов на сайте MRR.

        Args:
            type: Алгоритм: sha256, scrypt, x11 и т.д. (обязательное).
            currency: Валюта: [BTC,LTC,ETH,DOGE,BCH]. По умолчанию BTC.
            minhours_min: Минимальное количество часов.
            minhours_max: Максимальное количество часов.
            maxhours_min: Минимальное максимальное время.
            maxhours_max: Максимальное максимальное время.
            rpi_min: Минимальный RPI (0-100).
            rpi_max: Максимальный RPI (0-100).
            hash_min: Минимальный хешрейт.
            hash_max: Максимальный хешрейт.
            hash_type: Тип: [hash,kh,mh,gh,th,ph,eh]. По умолчанию mh.
            price_min: Минимальная цена.
            price_max: Максимальная цена.
            price_type: Тип хеша для цены.
            offline: Показывать оффлайн rig'и. По умолчанию false.
            rented: Показывать арендованные. По умолчанию false.
            region_type: 'include' или 'exclude'.
            expdiff: Ожидаемая сложность worker.
            count: Количество результатов (макс. 100). По умолчанию 100.
            islive: Фильтр по rig'ам с хешрейтом [yes].
            xnonce: Фильтр по xnonce [yes,no].
            offset: Смещение пагинации. По умолчанию 0.
            orderby: Сортировка. По умолчанию score.
            orderdir: Направление [asc,desc]. По умолчанию asc.

        Returns:
            MRRResponse[list[RigInfo]] — ответ со списком rig'ов:
            - При успехе: MRRResponse(success=True, data=[RigInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.search_rigs(type="scrypt", orderby="price", orderdir="asc")
            >>> if response.success:
            ...     for rig in response.data:
            ...         print(f"{rig.name}: {rig.price}")
        """
        endpoint = "/rig"
        params: dict[str, Any] = {"type": type}

        if currency is not None:
            params["currency"] = currency
        if minhours_min is not None:
            params["minhours.min"] = minhours_min
        if minhours_max is not None:
            params["minhours.max"] = minhours_max
        if maxhours_min is not None:
            params["maxhours.min"] = maxhours_min
        if maxhours_max is not None:
            params["maxhours.max"] = maxhours_max
        if rpi_min is not None:
            params["rpi.min"] = rpi_min
        if rpi_max is not None:
            params["rpi.max"] = rpi_max
        if hash_min is not None:
            params["hash.min"] = hash_min
        if hash_max is not None:
            params["hash.max"] = hash_max
        if hash_type is not None:
            params["hash.type"] = hash_type
        if price_min is not None:
            params["price.min"] = price_min
        if price_max is not None:
            params["price.max"] = price_max
        if price_type is not None:
            params["price.type"] = price_type
        if offline is not None:
            params["offline"] = offline
        if rented is not None:
            params["rented"] = rented
        if region_type is not None:
            params["region.type"] = region_type
        if expdiff is not None:
            params["expdiff"] = expdiff
        if count is not None:
            params["count"] = count
        if islive is not None:
            params["islive"] = islive
        if xnonce is not None:
            params["xnonce"] = xnonce
        if offset is not None:
            params["offset"] = offset
        if orderby is not None:
            params["orderby"] = orderby
        if orderdir is not None:
            params["orderdir"] = orderdir

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            rigs_data = result.data
            if isinstance(rigs_data, dict):
                rigs_list = rigs_data.get("records", [])
            else:
                rigs_list = rigs_data
            rigs = [RigInfo.model_validate(r) for r in rigs_list]
            return MRRResponse(
                success=True,
                data=rigs,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_mining_rigs(
        self, type: str | None = None, hashrate: bool | None = None
    ) -> MRRResponse[list[RigInfo]]:
        """Получает список ваших rig'ов.

        Args:
            type: Фильтр по алгоритму.
            hashrate: Показывать расчёт хешрейта.

        Returns:
            MRRResponse[list[RigInfo]] — ответ со списком ваших rig'ов:
            - При успехе: MRRResponse(success=True, data=[RigInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_mining_rigs(type="scrypt", hashrate=True)
            >>> if response.success:
            ...     print(f"Found {len(response.data)} rigs")
        """
        endpoint = "/rig/mine"
        params: dict[str, Any] = {}

        if type is not None:
            params["type"] = type
        if hashrate is not None:
            params["hashrate"] = hashrate

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            rigs_data: list[dict[str, Any]] = result.data
            rigs = [RigInfo.model_validate(r) for r in rigs_data]
            return MRRResponse(
                success=True,
                data=rigs,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_rigs(self, ids: list[int], fields: list[str] | None = None) -> MRRResponse[list[RigInfo]]:
        """Получает один или несколько rig'ов по ID.

        Args:
            ids: Список ID rig'ов для получения.
            fields: Фильтр полей root level (например, ["name", "status"]).

        Returns:
            MRRResponse[list[RigInfo]] — ответ со списком rig'ов:
            - При успехе: MRRResponse(success=True, data=[RigInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_rigs(ids=[12345, 12346])
            >>> if response.success:
            ...     for rig in response.data:
            ...         print(f"{rig.id}: {rig.name}")
        """
        # Формируем ID строку: "12345;12346;12347"
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}"
        params: dict[str, Any] = {}

        if fields is not None:
            params["fields"] = ",".join(fields)

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            rigs_data: list[dict[str, Any]] = result.data
            rigs = [RigInfo.model_validate(r) for r in rigs_data]
            return MRRResponse(
                success=True,
                data=rigs,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def create_rig(self, body: RigCreateBody) -> MRRResponse[dict[str, Any]]:
        """Создаёт новый rig.

        Args:
            body: Тело запроса с параметрами создания rig.

        Returns:
            MRRResponse[dict] — ответ с ID созданного rig:
            - При успехе: MRRResponse(success=True, data={"id": 12345})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RigCreateBody(
            ...     name="My Scrypt Rig",
            ...     server="us-east01.miningrigrentals.com",
            ...     price_type="mh",
            ... )
            >>> response = await rig_client.create_rig(body)
            >>> if response.success:
            ...     print(f"Rig created with ID: {response.data['id']}")
        """
        endpoint = "/rig"
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

    async def batch_update_rigs(self, body: RigBatchBody) -> MRRResponse[None]:
        """Обновляет пакет rig'ов.

        Args:
            body: Тело запроса со списком rig'ов для обновления.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RigBatchBody(rigs=[{"id": 12345, "name": "Updated Name"}])
            >>> response = await rig_client.batch_update_rigs(body)
            >>> if response.success:
            ...     print("Rigs updated successfully")
        """
        endpoint = "/rig/batch"
        body_dict = body.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.request(method="POST", endpoint=endpoint, body=body_dict)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def delete_rigs(self, ids: list[int]) -> MRRResponse[None]:
        """Удаляет один или несколько rig'ов по ID.

        Args:
            ids: Список ID rig'ов для удаления.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.delete_rigs(ids=[12345, 12346])
            >>> if response.success:
            ...     print("Rigs deleted successfully")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}"

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

    async def extend_rigs(
        self, ids: list[int], hours: float | None = None, minutes: float | None = None
    ) -> MRRResponse[None]:
        """Продлевает аренду rig'а (для владельцев).

        Args:
            ids: Список ID rig'ов для продления.
            hours: Часы для продления.
            minutes: Минуты для продления.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.extend_rigs(ids=[12345], hours=24)
            >>> if response.success:
            ...     print("Rig extended successfully")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/extend"
        body_dict: dict[str, Any] = {}

        if hours is not None:
            body_dict["hours"] = hours
        if minutes is not None:
            body_dict["minutes"] = minutes

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

    async def batch_extend_rigs(self, rig_hours: dict[int, float]) -> MRRResponse[None]:
        """Пакетное продление аренды для нескольких rig'ов.

        Args:
            rig_hours: Словарь {rig_id: hours} для продления.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.batch_extend_rigs({12345: 24, 12346: 48})
            >>> if response.success:
            ...     print("Rigs extended successfully")
        """
        endpoint = "/rig/batch/extend"
        body_dict = {"rigs": rig_hours}

        result = await self._http.request(method="POST", endpoint=endpoint, body=body_dict)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def update_rig_profile(self, ids: list[int], profile: int) -> MRRResponse[None]:
        """Применяет профиль пула к одному или нескольким rig'ам.

        Args:
            ids: Список ID rig'ов для обновления.
            profile: ID профиля для применения.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.update_rig_profile(ids=[12345], profile=678)
            >>> if response.success:
            ...     print("Profile applied successfully")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/profile"
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

    async def get_rig_pools(self, ids: list[int]) -> MRRResponse[list[Pool]]:
        """Получает пулы, назначенные rig'ам.

        Args:
            ids: Список ID rig'ов для получения пулов.

        Returns:
            MRRResponse[list[Pool]] — ответ со списком пулов:
            - При успехе: MRRResponse(success=True, data=[Pool, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_rig_pools(ids=[12345])
            >>> if response.success:
            ...     for pool in response.data:
            ...         print(f"{pool.name}: {pool.host}")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/pool"

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

    async def update_rig_pool(self, ids: list[int], body: RigPoolBody) -> MRRResponse[None]:
        """Добавляет или заменяет пул на rig'ах.

        Args:
            ids: Список ID rig'ов для обновления.
            body: Тело запроса с данными пула.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = RigPoolBody(
            ...     host="pool.example.com",
            ...     port=3333,
            ...     user="worker1",
            ...     password="password",
            ...     priority=0,
            ... )
            >>> response = await rig_client.update_rig_pool(ids=[12345], body=body)
            >>> if response.success:
            ...     print("Pool updated successfully")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/pool"
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

    async def delete_rig_pool(self, ids: list[int]) -> MRRResponse[None]:
        """Удаляет пул с rig'ов.

        Удаляет пул с указанным приоритетом с rig'ов.

        Args:
            ids: Список ID rig'ов для удаления пула.

        Returns:
            MRRResponse[None] — ответ:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.delete_rig_pool(ids=[12345])
            >>> if response.success:
            ...     print("Pool deleted successfully")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/pool"

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

    async def get_rig_ports(self, ids: list[int]) -> MRRResponse[RigPortInfo]:
        """Получает прямой номер порта для подключения к серверу.

        Args:
            ids: Список ID rig'ов (используется первый ID).

        Returns:
            MRRResponse[RigPortInfo] — ответ с информацией о порте:
            - При успехе: MRRResponse(success=True, data=RigPortInfo)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_rig_ports(ids=[12345])
            >>> if response.success:
            ...     print(f"Port: {response.data.port}")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/port"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            port_data: dict[str, Any] = result.data
            port_info = RigPortInfo.model_validate(port_data)
            return MRRResponse(
                success=True,
                data=port_info,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_rig_threads(self, ids: list[int]) -> MRRResponse[list[RigThreadInfo]]:
        """Получает список активных threads для rig'ов.

        Args:
            ids: Список ID rig'ов для получения threads.

        Returns:
            MRRResponse[list[RigThreadInfo]] — ответ со списком threads:
            - При успехе: MRRResponse(success=True, data=[RigThreadInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_rig_threads(ids=[12345])
            >>> if response.success:
            ...     for thread in response.data:
            ...         print(f"{thread.worker}: {thread.status}")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/threads"

        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            threads_data: list[dict[str, Any]] = result.data
            threads = [RigThreadInfo.model_validate(t) for t in threads_data]
            return MRRResponse(
                success=True,
                data=threads,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_rig_graph(
        self, ids: list[int], hours: float | None = None, deflate: bool | None = None
    ) -> MRRResponse[RigGraphData]:
        """Получает графические данные rig'а (исторический хешрейт, простои).

        Args:
            ids: Список ID rig'ов (используется первый ID).
            hours: Часы данных (макс. 2 недели). По умолчанию 168.
            deflate: Base64 кодирование. По умолчанию false.

        Returns:
            MRRResponse[RigGraphData] — ответ с графическими данными:
            - При успехе: MRRResponse(success=True, data=RigGraphData)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_rig_graph(ids=[12345], hours=24)
            >>> if response.success:
            ...     print(f"Hours of data: {response.data.hours}")
            ...     print(f"Hashrate points: {len(response.data.hashrate_data or [])}")
        """
        ids_str = ";".join(str(rig_id) for rig_id in ids)
        endpoint = f"/rig/{ids_str}/graph"
        params: dict[str, Any] = {}

        if hours is not None:
            params["hours"] = hours
        if deflate is not None:
            params["deflate"] = deflate

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            graph_data: dict[str, Any] = result.data
            graph = RigGraphData.model_validate(graph_data)
            return MRRResponse(
                success=True,
                data=graph,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

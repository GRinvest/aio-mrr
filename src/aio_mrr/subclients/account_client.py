"""Account Client для взаимодействия с Account API.

Этот модуль предоставляет AccountClient для работы с Account API endpoints:
- GET /account
- GET /account/balance
- GET /account/transactions
- GET /account/profile
- PUT /account/profile
- GET /account/profile/{id}
- PUT /account/profile/{id}
- PUT /account/profile/{id}/{priority}
- DELETE /account/profile/{id}
- GET /account/pool
- GET /account/pool/{ids}
- PUT /account/pool
- PUT /account/pool/{ids}
- DELETE /account/pool/{ids}
- PUT /account/pool/test
- GET /account/currencies

> ⚠️ PUT /account/balance (вывод средств) — эндпоинт отключён на стороне MRR.
  НЕ реализован.
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.account.request import (
    PoolCreateBody,
    PoolTestBody,
    ProfileCreateBody,
    TransactionsQueryParams,
)
from aio_mrr.models.account.response import (
    AccountInfo,
    BalanceInfo,
    CurrencyStatus,
    Pool,
    PoolCreateResponse,
    PoolTestResult,
    Profile,
    ProfileCreateResponse,
    ProfileDeleteResponse,
    TransactionsList,
)
from aio_mrr.models.base import MRRResponse
from aio_mrr.subclients.base import BaseSubClient


class AccountClient(BaseSubClient):
    """Client для работы с Account API.

    Предоставляет методы для управления аккаунтом:
    - получение информации об аккаунте и балансе
    - управление транзакциями
    - управление профилями пулов
    - управление сохранёнными пулами
    - тестирование подключения к пулам
    - получение статуса валют

    Пример использования:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.account.get_balance()
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует AccountClient.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        super().__init__(http_client)

    async def get_account(self) -> MRRResponse[AccountInfo]:
        """Получает информацию об аккаунте.

        Возвращает детальную информацию об аккаунте пользователя, включая
        адреса для депозитов и выводов, настройки уведомлений и параметры.

        Returns:
            MRRResponse[AccountInfo] — ответ с информацией об аккаунте:
            - При успехе: MRRResponse(success=True, data=AccountInfo)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_account()
            >>> if response.success:
            ...     print(f"Username: {response.data.username}")
        """
        endpoint = "/account"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            account_data: dict[str, Any] = result.data
            account = AccountInfo.model_validate(account_data)
            return MRRResponse(
                success=True,
                data=account,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_balance(self) -> MRRResponse[dict[str, BalanceInfo]]:
        """Получает балансы аккаунта по всем валютам.

        Возвращает информацию о балансах по каждой валюте, включая
        подтверждённые, ожидающие и неподтверждённые средства.

        > ℹ️ Балансы обновляются в реальном времени при поступлениях.

        Returns:
            MRRResponse[dict[str, BalanceInfo]] — ответ с балансами по валютам:
            - При успехе: MRRResponse(success=True, data={"BTC": BalanceInfo, ...})
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_balance()
            >>> if response.success:
            ...     for currency, balance in response.data.items():
            ...         print(f"{currency}: {balance.confirmed}")
        """
        endpoint = "/account/balance"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            balance_data: dict[str, dict[str, Any]] = result.data
            balances = {currency: BalanceInfo.model_validate(b) for currency, b in balance_data.items()}
            return MRRResponse(
                success=True,
                data=balances,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_transactions(self, params: TransactionsQueryParams | None = None) -> MRRResponse[TransactionsList]:
        """Получает историю транзакций аккаунта.

        Возвращает список транзакций с возможностью фильтрации по типу,
        алгоритму, rig/rental ID и временному диапазону.

        Args:
            params: Query параметры для фильтрации транзакций.
                   По умолчанию возвращает все транзакции (limit=100).

        Returns:
            MRRResponse[TransactionsList] — ответ со списком транзакций:
            - При успехе: MRRResponse(success=True, data=TransactionsList)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> params = TransactionsQueryParams(type="credit", limit=10)
            >>> response = await account_client.get_transactions(params)
            >>> if response.success:
            ...     for tx in response.data.transactions:
            ...         print(f"{tx.type}: {tx.amount}")
        """
        endpoint = "/account/transactions"
        params_dict: dict[str, Any] = {}

        if params is not None:
            params_dict = params.model_dump(exclude_none=True)

        result = await self._http.request(method="GET", endpoint=endpoint, params=params_dict)

        if result.success and result.data is not None:
            transactions_data: dict[str, Any] = result.data
            transactions = TransactionsList.model_validate(transactions_data)
            return MRRResponse(
                success=True,
                data=transactions,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_profiles(self, algo: str | None = None) -> MRRResponse[list[Profile]]:
        """Получает список профилей пулов.

        Возвращает все сохранённые профили пулов или фильтрует по алгоритму.
        Каждый профиль содержит информацию об алгоритме и список пулов с приоритетами.

        Args:
            algo: Фильтр по алгоритму (например, "scrypt", "sha256").
                 По умолчанию возвращает все профили.

        Returns:
            MRRResponse[list[Profile]] — ответ со списком профилей:
            - При успехе: MRRResponse(success=True, data=[Profile, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_profiles(algo="scrypt")
            >>> if response.success:
            ...     for profile in response.data:
            ...         print(f"{profile.name}: {len(profile.pools)} pools")
        """
        endpoint = "/account/profile"
        params: dict[str, Any] = {}

        if algo is not None:
            params["algo"] = algo

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            profiles_data: list[dict[str, Any]] = result.data
            profiles = [Profile.model_validate(p) for p in profiles_data]
            return MRRResponse(
                success=True,
                data=profiles,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def create_profile(self, body: ProfileCreateBody) -> MRRResponse[ProfileCreateResponse]:
        """Создаёт новый профиль пула.

        Создаёт новый профиль для указанного алгоритма майнинга. Профиль
        может содержать несколько пулов с разными приоритетами.

        Args:
            body: Тело запроса с названием и алгоритмом профиля.

        Returns:
            MRRResponse[ProfileCreateResponse] — ответ с ID созданного профиля:
            - При успехе: MRRResponse(success=True, data=ProfileCreateResponse)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = ProfileCreateBody(name="My Scrypt Profile", algo="scrypt")
            >>> response = await account_client.create_profile(body)
            >>> if response.success:
            ...     print(f"Profile created with ID: {response.data.pid}")
        """
        endpoint = "/account/profile"
        body_dict = body.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body_dict)

        if result.success and result.data is not None:
            profile_data: dict[str, Any] = result.data
            profile_response = ProfileCreateResponse.model_validate(profile_data)
            return MRRResponse(
                success=True,
                data=profile_response,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_profile(self, pid: int) -> MRRResponse[Profile]:
        """Получает конкретный профиль пула по ID.

        Возвращает детальную информацию о профиле, включая список пулов
        с их приоритетами и настройками подключения.

        Args:
            pid: Идентификатор профиля.

        Returns:
            MRRResponse[Profile] — ответ с информацией о профиле:
            - При успехе: MRRResponse(success=True, data=Profile)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_profile(pid=40073)
            >>> if response.success:
            ...     print(f"Profile: {response.data.name}")
            ...     for pool in response.data.pools:
            ...         print(f"  - {pool.host}:{pool.port} (priority {pool.priority})")
        """
        endpoint = f"/account/profile/{pid}"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            profile_data: dict[str, Any] = result.data
            profile = Profile.model_validate(profile_data)
            return MRRResponse(
                success=True,
                data=profile,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def update_profile(self, pid: int, poolid: int, priority: int | None = None) -> MRRResponse[None]:
        """Добавляет или заменяет пул в профиле.

        Добавляет пул в профиль с указанным приоритетом или заменяет
        существующий пул на этом приоритете.

        Args:
            pid: Идентификатор профиля.
            poolid: Идентификатор пула для добавления.
            priority: Приоритет пула (0-4). Если не указан, пул добавляется
                     на первый доступный приоритет.

        Returns:
            MRRResponse[None] — ответ о результате:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.update_profile(pid=40073, poolid=98708, priority=0)
            >>> if response.success:
            ...     print("Pool added to profile")
        """
        endpoint = f"/account/profile/{pid}"
        body: dict[str, Any] = {"poolid": poolid}

        if priority is not None:
            body["priority"] = priority

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def update_profile_priority(self, pid: int, priority: int, poolid: int) -> MRRResponse[None]:
        """Добавляет пул на конкретную позицию приоритета.

        Добавляет пул в профиль на указанную позицию приоритета (0-4).
        Пулы на более низких приоритетах имеют большее значение.

        Args:
            pid: Идентификатор профиля.
            priority: Приоритет пула (0-4).
            poolid: Идентификатор пула для добавления.

        Returns:
            MRRResponse[None] — ответ о результате:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.update_profile_priority(pid=41818, priority=0, poolid=98708)
            >>> if response.success:
            ...     print("Pool added at priority 0")
        """
        endpoint = f"/account/profile/{pid}/{priority}"
        body = {"poolid": poolid}

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def delete_profile(self, pid: int) -> MRRResponse[ProfileDeleteResponse]:
        """Удаляет профиль пула.

        Удаляет профиль пула по ID. Все пулы, связанные с профилем,
        также будут удалены из профиля.

        Args:
            pid: Идентификатор профиля для удаления.

        Returns:
            MRRResponse[ProfileDeleteResponse] — ответ о результате удаления:
            - При успехе: MRRResponse(success=True, data=ProfileDeleteResponse)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.delete_profile(pid=42281)
            >>> if response.success:
            ...     print(f"Deleted: {response.data.message}")
        """
        endpoint = f"/account/profile/{pid}"
        result = await self._http.request(method="DELETE", endpoint=endpoint)

        if result.success and result.data is not None:
            delete_data: dict[str, Any] = result.data
            delete_response = ProfileDeleteResponse.model_validate(delete_data)
            return MRRResponse(
                success=True,
                data=delete_response,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_pools(self) -> MRRResponse[list[Pool]]:
        """Получает список сохранённых пулов.

        Возвращает все сохранённые пулы аккаунта с полной информацией
        о подключении и настройках.

        Returns:
            MRRResponse[list[Pool]] — ответ со списком пулов:
            - При успехе: MRRResponse(success=True, data=[Pool, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_pools()
            >>> if response.success:
            ...     for pool in response.data:
            ...         print(f"{pool.name}: {pool.host}:{pool.port}")
        """
        endpoint = "/account/pool"
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

    async def get_pools_by_ids(self, ids: list[int]) -> MRRResponse[list[Pool]]:
        """Получает конкретные пулы по ID.

        Возвращает информацию о сохранённых пулах по списку их идентификаторов.
        Пулы разделяются точкой с запятой в URL.

        Args:
            ids: Список идентификаторов пулов.

        Returns:
            MRRResponse[list[Pool]] — ответ со списком пулов:
            - При успехе: MRRResponse(success=True, data=[Pool, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_pools_by_ids(ids=[12345, 12346])
            >>> if response.success:
            ...     for pool in response.data:
            ...         print(f"{pool.name}: {pool.type}")
        """
        ids_str = ";".join(str(i) for i in ids)
        endpoint = f"/account/pool/{ids_str}"
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

    async def create_pool(self, body: PoolCreateBody) -> MRRResponse[PoolCreateResponse]:
        """Создаёт сохранённый пул.

        Создаёт новый сохранённый пул с указанными параметрами подключения.
        Сохранённые пулы можно использовать в профилях и арендах.

        Args:
            body: Тело запроса с параметрами пула.

        Returns:
            MRRResponse[PoolCreateResponse] — ответ с ID созданного пула:
            - При успехе: MRRResponse(success=True, data=PoolCreateResponse)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = PoolCreateBody(
            ...     type="scrypt",
            ...     name="My Pool",
            ...     host="pool.example.com",
            ...     port=3333,
            ...     user="worker1",
            ...     password="pass123"
            ... )
            >>> response = await account_client.create_pool(body)
            >>> if response.success:
            ...     print(f"Pool created with ID: {response.data.id}")
        """
        endpoint = "/account/pool"
        body_dict = body.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body_dict)

        if result.success and result.data is not None:
            pool_data: dict[str, Any] = result.data
            pool_response = PoolCreateResponse.model_validate(pool_data)
            return MRRResponse(
                success=True,
                data=pool_response,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def update_pools(self, ids: list[int], body: dict[str, Any]) -> MRRResponse[None]:
        """Обновляет сохранённые пулы.

        Обновляет параметры существующих пулов по списку их идентификаторов.
        Можно обновить название, хост, порт, пользователя или пароль.

        Args:
            ids: Список идентификаторов пулов для обновления.
            body: Тело запроса с новыми параметрами пулов.

        Returns:
            MRRResponse[None] — ответ о результате:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> body = {"name": "Updated Pool Name", "host": "new.pool.com"}
            >>> response = await account_client.update_pools(ids=[12345], body=body)
            >>> if response.success:
            ...     print("Pool updated")
        """
        ids_str = ";".join(str(i) for i in ids)
        endpoint = f"/account/pool/{ids_str}"

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body)

        if result.success:
            return MRRResponse(
                success=True,
                data=None,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def delete_pools(self, ids: list[int]) -> MRRResponse[None]:
        """Удаляет сохранённые пулы.

        Удаляет сохранённые пулы по списку их идентификаторов.

        Args:
            ids: Список идентификаторов пулов для удаления.

        Returns:
            MRRResponse[None] — ответ о результате:
            - При успехе: MRRResponse(success=True, data=None)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.delete_pools(ids=[12345, 12346])
            >>> if response.success:
            ...     print("Pools deleted")
        """
        ids_str = ";".join(str(i) for i in ids)
        endpoint = f"/account/pool/{ids_str}"
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

    async def test_pool(self, body: PoolTestBody) -> MRRResponse[PoolTestResult]:
        """Тестирует подключение к пулу.

        Проверяет совместимость пула с MRR через тест подключения с разных
        серверов. Поддерживает простой тест (только подключение) и полный
        тест (с аутентификацией и получением работы).

        Args:
            body: Тело запроса с параметрами теста.

        Returns:
            MRRResponse[PoolTestResult] — ответ с результатами тестов:
            - При успехе: MRRResponse(success=True, data=PoolTestResult)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            # Простой тест
            >>> body = PoolTestBody(method="simple", host="de.minexmr.com:4444")
            >>> response = await account_client.test_pool(body)
            >>> if response.success:
            ...     for item in response.data.result:
            ...         print(f"{item.source} -> {item.dest}: {item.connection}")

            # Полный тест
            >>> body = PoolTestBody(
            ...     method="full",
            ...     type="cryptonote",
            ...     host="de.minexmr.com",
            ...     port=4444,
            ...     user="test",
            ...     password="x"
            ... )
            >>> response = await account_client.test_pool(body)
            >>> if response.success:
            ...     result = response.data.result[0]
            ...     print(f"Auth: {result.auth}, Work: {result.work}")
        """
        endpoint = "/account/pool/test"
        body_dict = body.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.request(method="PUT", endpoint=endpoint, body=body_dict)

        if result.success and result.data is not None:
            test_data: dict[str, Any] = result.data
            test_result = PoolTestResult.model_validate(test_data)
            return MRRResponse(
                success=True,
                data=test_result,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_currencies(self) -> MRRResponse[list[CurrencyStatus]]:
        """Получает список валют с статусом для аккаунта.

        Возвращает информацию о доступных валютах для платежей и их статусе
        включённости для аккаунта пользователя.

        Returns:
            MRRResponse[list[CurrencyStatus]] — ответ со списком валют:
            - При успехе: MRRResponse(success=True, data=[CurrencyStatus, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await account_client.get_currencies()
            >>> if response.success:
            ...     for currency in response.data:
            ...         status = "enabled" if currency.enabled else "disabled"
            ...         print(f"{currency.name}: {status}")
        """
        endpoint = "/account/currencies"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            # Ответ имеет структуру {"currencies": [...]}
            currencies_data: dict[str, list[dict[str, Any]]] = result.data
            currencies_list = currencies_data.get("currencies", [])
            currencies = [CurrencyStatus.model_validate(c) for c in currencies_list]
            return MRRResponse(
                success=True,
                data=currencies,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

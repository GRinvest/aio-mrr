"""Account Client for interacting with the Account API.

This module provides AccountClient for working with Account API endpoints:
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

> Note: PUT /account/balance (withdrawal) — endpoint is disabled on the MRR side.
  NOT implemented.
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
    """Client for working with the Account API.

    Provides methods for account management:
    - retrieving account information and balance
    - managing transactions
    - managing pool profiles
    - managing saved pools
    - testing pool connections
    - retrieving currency statuses

    Usage example:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.account.get_balance()
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initializes AccountClient.

        Args:
            http_client: HTTPClient instance for performing requests.
        """
        super().__init__(http_client)

    async def get_account(self) -> MRRResponse[AccountInfo]:
        """Retrieves account information.

        Returns detailed information about the user's account, including
        deposit and withdrawal addresses, notification settings, and preferences.

        Returns:
            MRRResponse[AccountInfo] — response with account information:
            - On success: MRRResponse(success=True, data=AccountInfo)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves account balances for all currencies.

        Returns balance information for each currency, including
        confirmed, pending, and unconfirmed funds.

        > Note: Balances are updated in real-time upon deposits.

        Returns:
            MRRResponse[dict[str, BalanceInfo]] — response with balances by currency:
            - On success: MRRResponse(success=True, data={"BTC": BalanceInfo, ...})
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves account transaction history.

        Returns a list of transactions with filtering by type,
        algorithm, rig/rental ID, and time range.

        Args:
            params: Query parameters for filtering transactions.
                   Defaults to returning all transactions (limit=100).

        Returns:
            MRRResponse[TransactionsList] — response with transaction list:
            - On success: MRRResponse(success=True, data=TransactionsList)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves the list of pool profiles.

        Returns all saved pool profiles or filters by algorithm.
        Each profile contains algorithm information and a list of pools with priorities.

        Args:
            algo: Filter by algorithm (e.g., "scrypt", "sha256").
                 Defaults to returning all profiles.

        Returns:
            MRRResponse[list[Profile]] — response with profile list:
            - On success: MRRResponse(success=True, data=[Profile, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Creates a new pool profile.

        Creates a new profile for the specified mining algorithm. A profile
        can contain multiple pools with different priorities.

        Args:
            body: Request body with profile name and algorithm.

        Returns:
            MRRResponse[ProfileCreateResponse] — response with created profile ID:
            - On success: MRRResponse(success=True, data=ProfileCreateResponse)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves a specific pool profile by ID.

        Returns detailed information about a profile, including the list of pools
        with their priorities and connection settings.

        Args:
            pid: Profile identifier.

        Returns:
            MRRResponse[Profile] — response with profile information:
            - On success: MRRResponse(success=True, data=Profile)
            - On error: MRRResponse(success=False, error=...)

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
        """Adds or replaces a pool in a profile.

        Adds a pool to a profile with the specified priority or replaces
        an existing pool at that priority.

        Args:
            pid: Profile identifier.
            poolid: Pool ID to add.
            priority: Pool priority (0-4). If not specified, the pool is added
                     to the first available priority.

        Returns:
            MRRResponse[None] — response with result:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Adds a pool to a specific priority position.

        Adds a pool to a profile at the specified priority position (0-4).
        Pools at lower priority numbers have higher precedence.

        Args:
            pid: Profile identifier.
            priority: Pool priority (0-4).
            poolid: Pool ID to add.

        Returns:
            MRRResponse[None] — response with result:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Deletes a pool profile.

        Deletes a pool profile by ID. All pools associated with the profile
        will also be removed from the profile.

        Args:
            pid: Profile identifier to delete.

        Returns:
            MRRResponse[ProfileDeleteResponse] — response with deletion result:
            - On success: MRRResponse(success=True, data=ProfileDeleteResponse)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves the list of saved pools.

        Returns all saved account pools with full connection
        information and settings.

        Returns:
            MRRResponse[list[Pool]] — response with pool list:
            - On success: MRRResponse(success=True, data=[Pool, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves specific pools by ID.

        Returns information about saved pools by their identifiers.
        Pools are separated by semicolons in the URL.

        Args:
            ids: List of pool identifiers.

        Returns:
            MRRResponse[list[Pool]] — response with pool list:
            - On success: MRRResponse(success=True, data=[Pool, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Creates a saved pool.

        Creates a new saved pool with the specified connection parameters.
        Saved pools can be used in profiles and rentals.

        Args:
            body: Request body with pool parameters.

        Returns:
            MRRResponse[PoolCreateResponse] — response with created pool ID:
            - On success: MRRResponse(success=True, data=PoolCreateResponse)
            - On error: MRRResponse(success=False, error=...)

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
        """Updates saved pools.

        Updates parameters of existing pools by their identifiers.
        You can update name, host, port, user, or password.

        Args:
            ids: List of pool identifiers to update.
            body: Request body with new pool parameters.

        Returns:
            MRRResponse[None] — response with result:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Deletes saved pools.

        Deletes saved pools by their identifiers.

        Args:
            ids: List of pool identifiers to delete.

        Returns:
            MRRResponse[None] — response with result:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Tests pool connection.

        Checks pool compatibility with MRR via connection test from different
        servers. Supports simple test (connection only) and full
        test (with authentication and work reception).

        Args:
            body: Request body with test parameters.

        Returns:
            MRRResponse[PoolTestResult] — response with test results:
            - On success: MRRResponse(success=True, data=PoolTestResult)
            - On error: MRRResponse(success=False, error=...)

        Example:
            # Simple test
            >>> body = PoolTestBody(method="simple", host="de.minexmr.com:4444")
            >>> response = await account_client.test_pool(body)
            >>> if response.success:
            ...     for item in response.data.result:
            ...         print(f"{item.source} -> {item.dest}: {item.connection}")

            # Full test
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
        """Retrieves the list of currencies with status for the account.

        Returns information about available currencies for payments and their
        enabled status for the user's account.

        Returns:
            MRRResponse[list[CurrencyStatus]] — response with currency list:
            - On success: MRRResponse(success=True, data=[CurrencyStatus, ...])
            - On error: MRRResponse(success=False, error=...)

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
            # Response has structure {"currencies": [...]}
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

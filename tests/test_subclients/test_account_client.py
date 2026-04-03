"""Tests for AccountClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.account.request import (
    PoolCreateBody,
    PoolTestBody,
    ProfileCreateBody,
    TransactionsQueryParams,
)
from aio_mrr.subclients.account_client import AccountClient


@pytest.fixture
async def account_client(api_key: str, api_secret: str) -> AsyncGenerator[AccountClient, None]:
    """Fixture for AccountClient."""
    http_client = HTTPClient(api_key=api_key, api_secret=api_secret)
    client = AccountClient(http_client=http_client)
    yield client
    await http_client.close()


class TestAccountClientGetAccount:
    """Tests for AccountClient.get_account method."""

    @pytest.mark.asyncio
    async def test_get_account_success(self, account_client: AccountClient) -> None:
        """Test successful get_account request."""
        endpoint = "/account"
        response_data = {
            "success": True,
            "data": {
                "username": "testuser",
                "email": "test@example.com",
                "withdraw": {},
                "deposit": {},
                "notifications": {
                    "rental_comm": "email",
                    "new_rental": "email",
                    "offline": "email",
                    "news": "email",
                    "deposit": "email",
                },
                "settings": {
                    "live_data": "yes",
                    "public_profile": "yes",
                    "2factor_auth": "no",
                },
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_account()

            assert result.success is True
            assert result.data is not None
            assert result.data.username == "testuser"
            assert result.data.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_account_api_error(self, account_client: AccountClient) -> None:
        """Test get_account with API error response."""
        endpoint = "/account"
        response_data = {
            "success": False,
            "data": {"message": "Invalid API key"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_account()

            assert result.success is False
            assert result.error is not None


class TestAccountClientGetBalance:
    """Tests for AccountClient.get_balance method."""

    @pytest.mark.asyncio
    async def test_get_balance_success(self, account_client: AccountClient) -> None:
        """Test successful get_balance request."""
        endpoint = "/account/balance"
        response_data = {
            "success": True,
            "data": {
                "BTC": {"confirmed": "0.1", "pending": 0, "unconfirmed": "0.0"},
                "LTC": {"confirmed": "10.0", "pending": "1.0", "unconfirmed": "0.0"},
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_balance()

            assert result.success is True
            assert result.data is not None
            assert "BTC" in result.data
            assert result.data["BTC"].confirmed == "0.1"
            assert result.data["LTC"].confirmed == "10.0"

    @pytest.mark.asyncio
    async def test_get_balance_empty(self, account_client: AccountClient) -> None:
        """Test get_balance with empty response."""
        endpoint = "/account/balance"
        response_data = {"success": True, "data": {}}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_balance()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 0


class TestAccountClientGetTransactions:
    """Tests for AccountClient.get_transactions method."""

    @pytest.mark.asyncio
    async def test_get_transactions_success(self, account_client: AccountClient) -> None:
        """Test successful get_transactions request."""
        endpoint = "/account/transactions"
        response_data = {
            "success": True,
            "data": {
                "transactions": [
                    {
                        "id": "1",
                        "type": "credit",
                        "amount": "0.1",
                        "currency": "BTC",
                        "when": "2024-01-01T00:00:00Z",
                        "status": "Cleared",
                    },
                    {
                        "id": "2",
                        "type": "debit",
                        "amount": "0.05",
                        "currency": "BTC",
                        "when": "2024-01-02T00:00:00Z",
                        "status": "Cleared",
                    },
                ],
                "total": "2",
                "returned": 2,
                "start": 0,
                "limit": 100,
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_transactions()

            assert result.success is True
            assert result.data is not None
            assert len(result.data.transactions) == 2

    @pytest.mark.asyncio
    async def test_get_transactions_with_params(self, account_client: AccountClient) -> None:
        """Test get_transactions with query parameters."""
        endpoint = "/account/transactions"
        params = TransactionsQueryParams(type="credit", limit=10)
        response_data = {
            "success": True,
            "data": {
                "transactions": [
                    {
                        "id": "1",
                        "type": "credit",
                        "amount": "0.1",
                        "currency": "BTC",
                        "when": "2024-01-01T00:00:00Z",
                        "status": "Cleared",
                    }
                ],
                "total": "1",
                "returned": 1,
                "start": 0,
                "limit": 10,
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?type=credit&limit=10",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_transactions(params=params)

            assert result.success is True
            assert result.data is not None
            assert len(result.data.transactions) == 1


class TestAccountClientGetProfiles:
    """Tests for AccountClient.get_profiles method."""

    @pytest.mark.asyncio
    async def test_get_profiles_success(self, account_client: AccountClient) -> None:
        """Test successful get_profiles request."""
        endpoint = "/account/profile"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": "1",
                    "name": "Scrypt Profile",
                    "algo": {
                        "name": "scrypt",
                        "display": "Scrypt",
                        "suggested_price": {"amount": "0.0001", "currency": "BTC", "unit": "mh"},
                    },
                    "pools": [
                        {
                            "host": "pool1.com",
                            "port": "3333",
                            "priority": 0,
                            "type": "scrypt",
                            "user": "worker1",
                            "pass": "x",
                            "status": "enabled",
                        }
                    ],
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_profiles()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].name == "Scrypt Profile"

    @pytest.mark.asyncio
    async def test_get_profiles_with_algo(self, account_client: AccountClient) -> None:
        """Test get_profiles with algo filter."""
        endpoint = "/account/profile"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": "1",
                    "name": "SHA256 Profile",
                    "algo": {
                        "name": "sha256",
                        "display": "SHA256",
                        "suggested_price": {"amount": "0.0002", "currency": "BTC", "unit": "mh"},
                    },
                    "pools": [],
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?algo=sha256",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_profiles(algo="sha256")

            assert result.success is True
            assert result.data is not None
            assert result.data[0].algo.name == "sha256"


class TestAccountClientCreateProfile:
    """Tests for AccountClient.create_profile method."""

    @pytest.mark.asyncio
    async def test_create_profile_success(self, account_client: AccountClient) -> None:
        """Test successful create_profile request."""
        endpoint = "/account/profile"
        body = ProfileCreateBody(name="New Profile", algo="scrypt")
        response_data = {"success": True, "data": {"pid": "12345"}}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.create_profile(body)

            assert result.success is True
            assert result.data is not None
            assert result.data.pid == "12345"


class TestAccountClientGetProfile:
    """Tests for AccountClient.get_profile method."""

    @pytest.mark.asyncio
    async def test_get_profile_success(self, account_client: AccountClient) -> None:
        """Test successful get_profile request."""
        pid = 12345
        endpoint = f"/account/profile/{pid}"
        response_data = {
            "success": True,
            "data": {
                "id": str(pid),
                "name": "Test Profile",
                "algo": {
                    "name": "scrypt",
                    "display": "Scrypt",
                    "suggested_price": {"amount": "0.0001", "currency": "BTC", "unit": "mh"},
                },
                "pools": [
                    {
                        "host": "pool.com",
                        "port": "3333",
                        "priority": 0,
                        "type": "scrypt",
                        "user": "worker1",
                        "pass": "x",
                        "status": "enabled",
                    }
                ],
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_profile(pid=pid)

            assert result.success is True
            assert result.data is not None
            assert result.data.id == str(pid)
            assert result.data.name == "Test Profile"


class TestAccountClientUpdateProfile:
    """Tests for AccountClient.update_profile method."""

    @pytest.mark.asyncio
    async def test_update_profile_success(self, account_client: AccountClient) -> None:
        """Test successful update_profile request."""
        pid = 12345
        poolid = 67890
        endpoint = f"/account/profile/{pid}"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.update_profile(pid=pid, poolid=poolid, priority=0)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_update_profile_without_priority(self, account_client: AccountClient) -> None:
        """Test update_profile without priority."""
        pid = 12345
        poolid = 67890
        endpoint = f"/account/profile/{pid}"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.update_profile(pid=pid, poolid=poolid)

            assert result.success is True


class TestAccountClientUpdateProfilePriority:
    """Tests for AccountClient.update_profile_priority method."""

    @pytest.mark.asyncio
    async def test_update_profile_priority_success(self, account_client: AccountClient) -> None:
        """Test successful update_profile_priority request."""
        pid = 12345
        priority = 0
        poolid = 67890
        endpoint = f"/account/profile/{pid}/{priority}"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.update_profile_priority(pid=pid, priority=priority, poolid=poolid)

            assert result.success is True


class TestAccountClientDeleteProfile:
    """Tests for AccountClient.delete_profile method."""

    @pytest.mark.asyncio
    async def test_delete_profile_success(self, account_client: AccountClient) -> None:
        """Test successful delete_profile request."""
        pid = 12345
        endpoint = f"/account/profile/{pid}"
        response_data = {"success": True, "data": {"id": str(pid), "success": True, "message": "Profile deleted"}}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.delete_profile(pid=pid)

            assert result.success is True
            assert result.data is not None
            assert result.data.message == "Profile deleted"


class TestAccountClientGetPools:
    """Tests for AccountClient.get_pools method."""

    @pytest.mark.asyncio
    async def test_get_pools_success(self, account_client: AccountClient) -> None:
        """Test successful get_pools request."""
        endpoint = "/account/pool"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "name": "Pool 1",
                    "type": "scrypt",
                    "host": "pool1.com",
                    "port": 3333,
                    "user": "worker1",
                    "pass": "x",
                },
                {
                    "id": 2,
                    "name": "Pool 2",
                    "type": "scrypt",
                    "host": "pool2.com",
                    "port": 3333,
                    "user": "worker2",
                    "pass": "y",
                },
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_pools()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 2
            assert result.data[0].name == "Pool 1"


class TestAccountClientGetPoolsByIds:
    """Tests for AccountClient.get_pools_by_ids method."""

    @pytest.mark.asyncio
    async def test_get_pools_by_ids_success(self, account_client: AccountClient) -> None:
        """Test successful get_pools_by_ids request."""
        ids = [1, 2]
        ids_str = "1;2"
        endpoint = f"/account/pool/{ids_str}"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "name": "Pool 1",
                    "type": "scrypt",
                    "host": "pool1.com",
                    "port": 3333,
                    "user": "worker1",
                    "pass": "x",
                },
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_pools_by_ids(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].id == 1


class TestAccountClientCreatePool:
    """Tests for AccountClient.create_pool method."""

    @pytest.mark.asyncio
    async def test_create_pool_success(self, account_client: AccountClient) -> None:
        """Test successful create_pool request."""
        endpoint = "/account/pool"
        body = PoolCreateBody(
            type="scrypt",
            name="New Pool",
            host="pool.example.com",
            port=3333,
            user="worker1",
            pass_="pass123",  # type: ignore[call-arg]
        )
        response_data = {"success": True, "data": {"id": 12345}}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.create_pool(body)

            assert result.success is True
            assert result.data is not None
            assert result.data.id == 12345


class TestAccountClientUpdatePools:
    """Tests for AccountClient.update_pools method."""

    @pytest.mark.asyncio
    async def test_update_pools_success(self, account_client: AccountClient) -> None:
        """Test successful update_pools request."""
        ids = [1, 2]
        ids_str = "1;2"
        endpoint = f"/account/pool/{ids_str}"
        body = {"name": "Updated Pool"}
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.update_pools(ids=ids, body=body)

            assert result.success is True


class TestAccountClientDeletePools:
    """Tests for AccountClient.delete_pools method."""

    @pytest.mark.asyncio
    async def test_delete_pools_success(self, account_client: AccountClient) -> None:
        """Test successful delete_pools request."""
        ids = [1, 2]
        ids_str = "1;2"
        endpoint = f"/account/pool/{ids_str}"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.delete_pools(ids=ids)

            assert result.success is True


class TestAccountClientTestPool:
    """Tests for AccountClient.test_pool method."""

    @pytest.mark.asyncio
    async def test_test_pool_simple_success(self, account_client: AccountClient) -> None:
        """Test successful simple pool test."""
        endpoint = "/account/pool/test"
        body = PoolTestBody(method="simple", host="de.minexmr.com:4444")
        response_data = {
            "success": True,
            "data": {
                "result": [
                    {
                        "source": "us-central01.miningrigrentals.com",
                        "dest": "de.minexmr.com:4444",
                        "error": "none",
                        "connection": True,
                        "executiontime": 0.123,
                    }
                ],
                "error": [],
            },
        }

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.test_pool(body)

            assert result.success is True
            assert result.data is not None
            assert len(result.data.result) == 1
            assert result.data.result[0].connection is True

    @pytest.mark.asyncio
    async def test_test_pool_full_success(self, account_client: AccountClient) -> None:
        """Test successful full pool test."""
        endpoint = "/account/pool/test"
        body = PoolTestBody(
            method="full",
            type="cryptonote",
            host="de.minexmr.com",
            port=4444,
            user="test",
            pass_="x",  # type: ignore[call-arg]
        )
        response_data = {
            "success": True,
            "data": {
                "result": [
                    {
                        "source": "ca-tor01.miningrigrentals.com",
                        "dest": "de.minexmr.com:4444",
                        "protocol": "stratum",
                        "connection": True,
                        "sub": True,
                        "auth": True,
                        "error": "none",
                        "executiontime": 0.123,
                    }
                ],
                "error": [],
            },
        }

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.test_pool(body)

            assert result.success is True
            assert result.data is not None
            assert result.data.result[0].auth is True


class TestAccountClientGetCurrencies:
    """Tests for AccountClient.get_currencies method."""

    @pytest.mark.asyncio
    async def test_get_currencies_success(self, account_client: AccountClient) -> None:
        """Test successful get_currencies request."""
        endpoint = "/account/currencies"
        response_data = {
            "success": True,
            "data": {
                "currencies": [
                    {"name": "BTC", "enabled": True},
                    {"name": "LTC", "enabled": True},
                    {"name": "ETH", "enabled": False},
                ]
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await account_client.get_currencies()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 3
            assert result.data[0].name == "BTC"
            assert result.data[0].enabled is True

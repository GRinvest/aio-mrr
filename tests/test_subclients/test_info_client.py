"""Tests for InfoClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.subclients.info_client import InfoClient


@pytest.fixture
async def info_client(api_key: str, api_secret: str) -> AsyncGenerator[InfoClient, None]:
    """Fixture for InfoClient."""
    http_client = HTTPClient(api_key=api_key, api_secret=api_secret)
    client = InfoClient(http_client=http_client)
    yield client
    await http_client.close()


class TestInfoClientGetServers:
    """Tests for InfoClient.get_servers method."""

    @pytest.mark.asyncio
    async def test_get_servers_success(self, info_client: InfoClient) -> None:
        """Test successful get_servers request."""
        endpoint = "/info/servers"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": "1",
                    "name": "us-east01",
                    "region": "US East",
                    "port": "443",
                    "ethereum_port": "8443",
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_servers()

            assert result.success is True
            assert result.data is not None
            assert len(result.data.servers) == 1
            assert result.data.servers[0].id == "1"
            assert result.data.servers[0].name == "us-east01"
            assert result.http_status == 200

    @pytest.mark.asyncio
    async def test_get_servers_empty(self, info_client: InfoClient) -> None:
        """Test get_servers with empty response."""
        endpoint = "/info/servers"
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_servers()

            assert result.success is True
            assert result.data is not None
            assert len(result.data.servers) == 0

    @pytest.mark.asyncio
    async def test_get_servers_api_error(self, info_client: InfoClient) -> None:
        """Test get_servers with API error response."""
        endpoint = "/info/servers"
        response_data = {
            "success": False,
            "data": {"message": "Internal server error"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_servers()

            assert result.success is False
            assert result.error is not None
            assert result.error.code == "api_error"


class TestInfoClientGetAlgos:
    """Tests for InfoClient.get_algos method."""

    @pytest.mark.asyncio
    async def test_get_algos_success(self, info_client: InfoClient) -> None:
        """Test successful get_algos request."""
        endpoint = "/info/algos"
        response_data = {
            "success": True,
            "data": [
                {
                    "name": "scrypt",
                    "display": "Scrypt",
                    "suggested_price": {"amount": "0.0001", "currency": "BTC", "unit": "mh"},
                    "stats": {
                        "available": {"rigs": "100", "hash": {"hash": 500.0, "unit": "mh", "nice": "500.00Mh"}},
                        "rented": {"rigs": "50", "hash": {"hash": 250.0, "unit": "mh", "nice": "250.00Mh"}},
                        "prices": {
                            "lowest": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                            "last_10": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                            "last": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                        },
                    },
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_algos()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].name == "scrypt"
            assert result.data[0].display == "Scrypt"

    @pytest.mark.asyncio
    async def test_get_algos_with_currency(self, info_client: InfoClient) -> None:
        """Test get_algos with currency parameter."""
        endpoint = "/info/algos"
        response_data = {
            "success": True,
            "data": [
                {
                    "name": "scrypt",
                    "display": "Scrypt",
                    "suggested_price": {"amount": "0.01", "currency": "LTC", "unit": "mh"},
                    "stats": {
                        "available": {"rigs": "100", "hash": {"hash": 500.0, "unit": "mh", "nice": "500.00Mh"}},
                        "rented": {"rigs": "50", "hash": {"hash": 250.0, "unit": "mh", "nice": "250.00Mh"}},
                        "prices": {
                            "lowest": {"amount": "0.01", "currency": "LTC", "unit": "mh*day"},
                            "last_10": {"amount": "0.01", "currency": "LTC", "unit": "mh*day"},
                            "last": {"amount": "0.01", "currency": "LTC", "unit": "mh*day"},
                        },
                    },
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?currency=LTC",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_algos(currency="LTC")

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].name == "scrypt"

    @pytest.mark.asyncio
    async def test_get_algos_api_error(self, info_client: InfoClient) -> None:
        """Test get_algos with API error response."""
        endpoint = "/info/algos"
        response_data = {
            "success": False,
            "data": {"message": "Invalid currency"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_algos()

            assert result.success is False
            assert result.error is not None


class TestInfoClientGetAlgo:
    """Tests for InfoClient.get_algo method."""

    @pytest.mark.asyncio
    async def test_get_algo_success(self, info_client: InfoClient) -> None:
        """Test successful get_algo request."""
        algo_name = "scrypt"
        endpoint = f"/info/algos/{algo_name}"
        response_data = {
            "success": True,
            "data": {
                "name": "scrypt",
                "display": "Scrypt",
                "suggested_price": {"amount": "0.0001", "currency": "BTC", "unit": "mh"},
                "stats": {
                    "available": {"rigs": "100", "hash": {"hash": 500.0, "unit": "mh", "nice": "500.00Mh"}},
                    "rented": {"rigs": "50", "hash": {"hash": 250.0, "unit": "mh", "nice": "250.00Mh"}},
                    "prices": {
                        "lowest": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                        "last_10": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                        "last": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                    },
                },
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_algo(name=algo_name)

            assert result.success is True
            assert result.data is not None
            assert result.data.name == "scrypt"
            assert result.data.display == "Scrypt"

    @pytest.mark.asyncio
    async def test_get_algo_with_currency(self, info_client: InfoClient) -> None:
        """Test get_algo with currency parameter."""
        algo_name = "sha256"
        endpoint = f"/info/algos/{algo_name}"
        response_data = {
            "success": True,
            "data": {
                "name": "sha256",
                "display": "SHA256",
                "suggested_price": {"amount": "0.0002", "currency": "BTC", "unit": "mh"},
                "stats": {
                    "available": {"rigs": "200", "hash": {"hash": 1000.0, "unit": "mh", "nice": "1.00Th"}},
                    "rented": {"rigs": "100", "hash": {"hash": 500.0, "unit": "mh", "nice": "500.00Mh"}},
                    "prices": {
                        "lowest": {"amount": "0.0002", "currency": "BTC", "unit": "mh*day"},
                        "last_10": {"amount": "0.0002", "currency": "BTC", "unit": "mh*day"},
                        "last": {"amount": "0.0002", "currency": "BTC", "unit": "mh*day"},
                    },
                },
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?currency=BTC",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_algo(name=algo_name, currency="BTC")

            assert result.success is True
            assert result.data is not None
            assert result.data.name == "sha256"

    @pytest.mark.asyncio
    async def test_get_algo_not_found(self, info_client: InfoClient) -> None:
        """Test get_algo with not found error."""
        algo_name = "invalid_algo"
        endpoint = f"/info/algos/{algo_name}"
        response_data = {
            "success": False,
            "data": {"message": "Algorithm not found"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_algo(name=algo_name)

            assert result.success is False
            assert result.error is not None
            assert "not found" in result.error.message.lower()


class TestInfoClientGetCurrencies:
    """Tests for InfoClient.get_currencies method."""

    @pytest.mark.asyncio
    async def test_get_currencies_success(self, info_client: InfoClient) -> None:
        """Test successful get_currencies request."""
        endpoint = "/info/currencies"
        response_data = {
            "success": True,
            "data": {
                "currencies": [
                    {"name": "BTC", "enabled": True, "txfee": "0.0005"},
                    {"name": "LTC", "enabled": True, "txfee": "0.01"},
                    {"name": "ETH", "enabled": False, "txfee": "0.005"},
                ]
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_currencies()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 3
            assert result.data[0].name == "BTC"
            assert result.data[0].enabled is True
            assert result.data[0].txfee == "0.0005"

    @pytest.mark.asyncio
    async def test_get_currencies_empty(self, info_client: InfoClient) -> None:
        """Test get_currencies with empty response."""
        endpoint = "/info/currencies"
        response_data = {"success": True, "data": {"currencies": []}}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_currencies()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 0

    @pytest.mark.asyncio
    async def test_get_currencies_api_error(self, info_client: InfoClient) -> None:
        """Test get_currencies with API error response."""
        endpoint = "/info/currencies"
        response_data = {
            "success": False,
            "data": {"message": "Internal server error"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await info_client.get_currencies()

            assert result.success is False
            assert result.error is not None

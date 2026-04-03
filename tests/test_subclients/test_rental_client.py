"""Tests for RentalClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.rental.request import RentalCreateBody, RentalPoolBody
from aio_mrr.subclients.rental_client import RentalClient


@pytest.fixture
async def rental_client(api_key: str, api_secret: str) -> AsyncGenerator[RentalClient, None]:
    """Fixture for RentalClient."""
    http_client = HTTPClient(api_key=api_key, api_secret=api_secret)
    client = RentalClient(http_client=http_client)
    yield client
    await http_client.close()


class TestRentalClientGetList:
    """Tests for RentalClient.get_list method."""

    @pytest.mark.asyncio
    async def test_get_list_success(self, rental_client: RentalClient) -> None:
        """Test successful get_list request."""
        endpoint = "/rental"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": "54321",
                    "rig_id": "12345",
                    "status": "active",
                    "length": 24,
                    "currency": "BTC",
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_list()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].id == "54321"
            assert result.data[0].status == "active"

    @pytest.mark.asyncio
    async def test_get_list_with_params(self, rental_client: RentalClient) -> None:
        """Test get_list with query parameters."""
        endpoint = "/rental"
        params = {"type": "renter", "history": False}
        response_data = {
            "success": True,
            "data": [
                {"id": "54321", "rig_id": "12345", "status": "active", "length": 24},
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?type=renter&history=false",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_list(params=params)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_get_list_empty(self, rental_client: RentalClient) -> None:
        """Test get_list with empty response."""
        endpoint = "/rental"
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_list()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 0


class TestRentalClientGetByIds:
    """Tests for RentalClient.get_by_ids method."""

    @pytest.mark.asyncio
    async def test_get_by_ids_success(self, rental_client: RentalClient) -> None:
        """Test successful get_by_ids request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}"
        response_data = {
            "success": True,
            "data": {
                "id": "54321",
                "rig_id": "12345",
                "status": "active",
                "length": 24,
                "currency": "BTC",
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_by_ids(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert result.data.id == "54321"
            assert result.data.rig_id == "12345"


class TestRentalClientCreate:
    """Tests for RentalClient.create method."""

    @pytest.mark.asyncio
    async def test_create_success(self, rental_client: RentalClient) -> None:
        """Test successful create request."""
        endpoint = "/rental"
        body = RentalCreateBody(rig=12345, length=24, profile=678, currency="BTC")
        response_data = {"success": True, "data": {"id": "54321"}}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.create(body)

            assert result.success is True
            assert result.data is not None
            assert result.data["id"] == "54321"


class TestRentalClientUpdateProfile:
    """Tests for RentalClient.update_profile method."""

    @pytest.mark.asyncio
    async def test_update_profile_success(self, rental_client: RentalClient) -> None:
        """Test successful update_profile request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/profile"
        profile = 678
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.update_profile(ids=ids, profile=profile)

            assert result.success is True


class TestRentalClientGetPools:
    """Tests for RentalClient.get_pools method."""

    @pytest.mark.asyncio
    async def test_get_pools_success(self, rental_client: RentalClient) -> None:
        """Test successful get_pools request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/pool"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "name": "Pool 1",
                    "type": "scrypt",
                    "host": "pool.com",
                    "port": 3333,
                    "user": "worker1",
                    "pass": "x",
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_pools(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].name == "Pool 1"


class TestRentalClientUpdatePool:
    """Tests for RentalClient.update_pool method."""

    @pytest.mark.asyncio
    async def test_update_pool_success(self, rental_client: RentalClient) -> None:
        """Test successful update_pool request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/pool"
        body = RentalPoolBody(
            host="pool.example.com",
            port=3333,
            user="worker1",
            **{"pass": "pass123"},
            priority=0,
        )
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.update_pool(ids=ids, body=body)

            assert result.success is True


class TestRentalClientDeletePool:
    """Tests for RentalClient.delete_pool method."""

    @pytest.mark.asyncio
    async def test_delete_pool_success(self, rental_client: RentalClient) -> None:
        """Test successful delete_pool request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/pool"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.delete_pool(ids=ids)

            assert result.success is True


class TestRentalClientExtend:
    """Tests for RentalClient.extend method."""

    @pytest.mark.asyncio
    async def test_extend_success(self, rental_client: RentalClient) -> None:
        """Test successful extend request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/extend"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.extend(ids=ids, length=12)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_extend_with_getcost(self, rental_client: RentalClient) -> None:
        """Test extend with getcost parameter."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/extend"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.extend(ids=ids, length=12, getcost=True)

            assert result.success is True


class TestRentalClientGetGraph:
    """Tests for RentalClient.get_graph method."""

    @pytest.mark.asyncio
    async def test_get_graph_success(self, rental_client: RentalClient) -> None:
        """Test successful get_graph request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/graph"
        response_data = {
            "success": True,
            "data": {
                "hours": 24,
                "hashrate_data": [{"time": "1234567890", "hashrate": 500.0}],
                "downtime_data": [],
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?hours=24",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_graph(ids=ids, hours=24)

            assert result.success is True
            assert result.data is not None
            assert result.data.hours == 24
            assert len(result.data.hashrate_data or []) == 1

    @pytest.mark.asyncio
    async def test_get_graph_with_interval(self, rental_client: RentalClient) -> None:
        """Test get_graph with interval parameter."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/graph"
        response_data = {
            "success": True,
            "data": {
                "hours": 24,
                "hashrate_data": [],
                "downtime_data": [],
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?hours=24&interval=1h",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_graph(ids=ids, hours=24, interval="1h")

            assert result.success is True


class TestRentalClientGetLog:
    """Tests for RentalClient.get_log method."""

    @pytest.mark.asyncio
    async def test_get_log_success(self, rental_client: RentalClient) -> None:
        """Test successful get_log request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/log"
        response_data = {
            "success": True,
            "data": [
                {"time": "2024-01-01T00:00:00Z", "message": "Rental started"},
                {"time": "2024-01-01T12:00:00Z", "message": "Pool changed"},
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_log(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 2
            assert result.data[0].message == "Rental started"


class TestRentalClientGetMessage:
    """Tests for RentalClient.get_message method."""

    @pytest.mark.asyncio
    async def test_get_message_success(self, rental_client: RentalClient) -> None:
        """Test successful get_message request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/message"
        response_data = {
            "success": True,
            "data": [
                {"time": "2024-01-01T00:00:00Z", "user": "admin", "message": "Welcome"},
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.get_message(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].user == "admin"


class TestRentalClientSendMessage:
    """Tests for RentalClient.send_message method."""

    @pytest.mark.asyncio
    async def test_send_message_success(self, rental_client: RentalClient) -> None:
        """Test successful send_message request."""
        ids = [54321]
        ids_str = "54321"
        endpoint = f"/rental/{ids_str}/message"
        message = "Please check the rig status"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rental_client.send_message(ids=ids, message=message)

            assert result.success is True

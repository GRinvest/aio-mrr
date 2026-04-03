"""Tests for RigClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.rig.request import RigBatchBody, RigCreateBody, RigPoolBody
from aio_mrr.subclients.rig_client import RigClient


@pytest.fixture
async def rig_client(api_key: str, api_secret: str) -> AsyncGenerator[RigClient, None]:
    """Fixture for RigClient."""
    http_client = HTTPClient(api_key=api_key, api_secret=api_secret)
    client = RigClient(http_client=http_client)
    yield client
    await http_client.close()


class TestRigClientSearchRigs:
    """Tests for RigClient.search_rigs method."""

    @pytest.mark.asyncio
    async def test_search_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful search_rigs request."""
        endpoint = "/rig"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": 12345,
                    "name": "Scrypt Rig 1",
                    "status": "enabled",
                    "type": "scrypt",
                    "hash": {"hash": 500.0, "type": "mh"},
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?type=scrypt&count=50",
                payload=response_data,
                status=200,
            )

            result = await rig_client.search_rigs(type="scrypt", count=50)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].id == 12345
            assert result.data[0].name == "Scrypt Rig 1"

    @pytest.mark.asyncio
    async def test_search_rigs_with_filters(self, rig_client: RigClient) -> None:
        """Test search_rigs with multiple filters."""
        endpoint = "/rig"
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?type=scrypt&price.min=0.0001&price.max=0.001",
                payload=response_data,
                status=200,
            )

            result = await rig_client.search_rigs(
                type="scrypt",
                price_min=0.0001,
                price_max=0.001,
            )

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 0

    @pytest.mark.asyncio
    async def test_search_rigs_empty(self, rig_client: RigClient) -> None:
        """Test search_rigs with empty results."""
        endpoint = "/rig"
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?type=sha256",
                payload=response_data,
                status=200,
            )

            result = await rig_client.search_rigs(type="sha256")

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 0


class TestRigClientGetMiningRigs:
    """Tests for RigClient.get_mining_rigs method."""

    @pytest.mark.asyncio
    async def test_get_mining_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful get_mining_rigs request."""
        endpoint = "/rig/mine"
        response_data = {
            "success": True,
            "data": [
                {
                    "id": 12345,
                    "name": "My Rig",
                    "status": "enabled",
                    "type": "scrypt",
                    "hash": {"hash": 500.0, "type": "mh"},
                }
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.get_mining_rigs()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_get_mining_rigs_with_params(self, rig_client: RigClient) -> None:
        """Test get_mining_rigs with parameters."""
        endpoint = "/rig/mine"
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?type=scrypt&hashrate=true",
                payload=response_data,
                status=200,
            )

            result = await rig_client.get_mining_rigs(type="scrypt", hashrate=True)

            assert result.success is True


class TestRigClientGetRigs:
    """Tests for RigClient.get_rigs method."""

    @pytest.mark.asyncio
    async def test_get_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful get_rigs request."""
        ids = [12345, 12346]
        ids_str = "12345;12346"
        endpoint = f"/rig/{ids_str}"
        response_data = {
            "success": True,
            "data": [
                {"id": 12345, "name": "Rig 1", "status": "enabled"},
                {"id": 12346, "name": "Rig 2", "status": "enabled"},
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.get_rigs(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 2

    @pytest.mark.asyncio
    async def test_get_rigs_with_fields(self, rig_client: RigClient) -> None:
        """Test get_rigs with fields filter."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}"
        response_data = {"success": True, "data": [{"id": 12345, "name": "Rig 1"}]}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}?fields=id,name",
                payload=response_data,
                status=200,
            )

            result = await rig_client.get_rigs(ids=ids, fields=["id", "name"])

            assert result.success is True
            assert result.data is not None


class TestRigClientCreateRig:
    """Tests for RigClient.create_rig method."""

    @pytest.mark.asyncio
    async def test_create_rig_success(self, rig_client: RigClient) -> None:
        """Test successful create_rig request."""
        endpoint = "/rig"
        body = RigCreateBody(
            name="New Rig",
            server="us-east01.miningrigrentals.com",
            minhours=24,
            maxhours=168,
        )
        response_data = {"success": True, "data": {"id": 12345}}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.create_rig(body)

            assert result.success is True
            assert result.data is not None
            assert result.data["id"] == 12345


class TestRigClientBatchUpdateRigs:
    """Tests for RigClient.batch_update_rigs method."""

    @pytest.mark.asyncio
    async def test_batch_update_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful batch_update_rigs request."""
        endpoint = "/rig/batch"
        body = RigBatchBody(rigs=[{"id": 12345, "name": "Updated Name"}])
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.batch_update_rigs(body)

            assert result.success is True


class TestRigClientDeleteRigs:
    """Tests for RigClient.delete_rigs method."""

    @pytest.mark.asyncio
    async def test_delete_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful delete_rigs request."""
        ids = [12345, 12346]
        ids_str = "12345;12346"
        endpoint = f"/rig/{ids_str}"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.delete_rigs(ids=ids)

            assert result.success is True


class TestRigClientExtendRigs:
    """Tests for RigClient.extend_rigs method."""

    @pytest.mark.asyncio
    async def test_extend_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful extend_rigs request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/extend"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.extend_rigs(ids=ids, hours=24, minutes=0)

            assert result.success is True


class TestRigClientBatchExtendRigs:
    """Tests for RigClient.batch_extend_rigs method."""

    @pytest.mark.asyncio
    async def test_batch_extend_rigs_success(self, rig_client: RigClient) -> None:
        """Test successful batch_extend_rigs request."""
        endpoint = "/rig/batch/extend"
        rig_hours: dict[int, float] = {12345: 24.0, 12346: 48.0}
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.batch_extend_rigs(rig_hours=rig_hours)

            assert result.success is True


class TestRigClientUpdateRigProfile:
    """Tests for RigClient.update_rig_profile method."""

    @pytest.mark.asyncio
    async def test_update_rig_profile_success(self, rig_client: RigClient) -> None:
        """Test successful update_rig_profile request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/profile"
        profile = 678
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.update_rig_profile(ids=ids, profile=profile)

            assert result.success is True


class TestRigClientGetRigPools:
    """Tests for RigClient.get_rig_pools method."""

    @pytest.mark.asyncio
    async def test_get_rig_pools_success(self, rig_client: RigClient) -> None:
        """Test successful get_rig_pools request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/pool"
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

            result = await rig_client.get_rig_pools(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 1


class TestRigClientUpdateRigPool:
    """Tests for RigClient.update_rig_pool method."""

    @pytest.mark.asyncio
    async def test_update_rig_pool_success(self, rig_client: RigClient) -> None:
        """Test successful update_rig_pool request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/pool"
        body = RigPoolBody(
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

            result = await rig_client.update_rig_pool(ids=ids, body=body)

            assert result.success is True


class TestRigClientDeleteRigPool:
    """Tests for RigClient.delete_rig_pool method."""

    @pytest.mark.asyncio
    async def test_delete_rig_pool_success(self, rig_client: RigClient) -> None:
        """Test successful delete_rig_pool request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/pool"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.delete_rig_pool(ids=ids)

            assert result.success is True


class TestRigClientGetRigPorts:
    """Tests for RigClient.get_rig_ports method."""

    @pytest.mark.asyncio
    async def test_get_rig_ports_success(self, rig_client: RigClient) -> None:
        """Test successful get_rig_ports request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/port"
        response_data = {
            "success": True,
            "data": {
                "id": 12345,
                "port": 12345,
                "server": "us-east01.miningrigrentals.com",
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.get_rig_ports(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert result.data.port == 12345


class TestRigClientGetRigThreads:
    """Tests for RigClient.get_rig_threads method."""

    @pytest.mark.asyncio
    async def test_get_rig_threads_success(self, rig_client: RigClient) -> None:
        """Test successful get_rig_threads request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/threads"
        response_data = {
            "success": True,
            "data": [
                {"id": 1, "rig_id": 12345, "worker": "worker1", "status": "accepted", "hashrate": 500.0},
                {"id": 2, "rig_id": 12345, "worker": "worker2", "status": "accepted", "hashrate": 500.0},
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await rig_client.get_rig_threads(ids=ids)

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 2
            assert result.data[0].worker == "worker1"


class TestRigClientGetRigGraph:
    """Tests for RigClient.get_rig_graph method."""

    @pytest.mark.asyncio
    async def test_get_rig_graph_success(self, rig_client: RigClient) -> None:
        """Test successful get_rig_graph request."""
        ids = [12345]
        ids_str = "12345"
        endpoint = f"/rig/{ids_str}/graph"
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

            result = await rig_client.get_rig_graph(ids=ids, hours=24)

            assert result.success is True
            assert result.data is not None
            assert result.data.hours == 24
            assert len(result.data.hashrate_data or []) == 1

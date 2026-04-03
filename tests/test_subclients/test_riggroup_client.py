"""Tests for RigGroupClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.riggroup.request import RigGroupCreateBody, RigGroupUpdateBody
from aio_mrr.subclients.riggroup_client import RigGroupClient


@pytest.fixture
async def riggroup_client(api_key: str, api_secret: str) -> AsyncGenerator[RigGroupClient, None]:
    """Fixture for RigGroupClient."""
    http_client = HTTPClient(api_key=api_key, api_secret=api_secret)
    client = RigGroupClient(http_client=http_client)
    yield client
    await http_client.close()


class TestRigGroupClientGetList:
    """Tests for RigGroupClient.get_list method."""

    @pytest.mark.asyncio
    async def test_get_list_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful get_list request."""
        endpoint = "/riggroup"
        response_data = {
            "success": True,
            "data": [
                {"id": "1", "name": "Scrypt Rigs", "rigs": [12345, 12346], "rental_limit": 10, "enabled": True},
                {"id": "2", "name": "SHA256 Rigs", "rigs": [12347], "rental_limit": 5, "enabled": True},
            ],
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.get_list()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 2
            assert result.data[0].name == "Scrypt Rigs"
            assert result.data[0].rental_limit == 10

    @pytest.mark.asyncio
    async def test_get_list_empty(self, riggroup_client: RigGroupClient) -> None:
        """Test get_list with empty response."""
        endpoint = "/riggroup"
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.get_list()

            assert result.success is True
            assert result.data is not None
            assert len(result.data) == 0


class TestRigGroupClientGetById:
    """Tests for RigGroupClient.get_by_id method."""

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful get_by_id request."""
        group_id = 1
        endpoint = f"/riggroup/{group_id}"
        response_data = {
            "success": True,
            "data": {
                "id": str(group_id),
                "name": "Scrypt Rigs",
                "rigs": [12345, 12346],
                "rental_limit": 10,
                "enabled": True,
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.get_by_id(id=group_id)

            assert result.success is True
            assert result.data is not None
            assert result.data.id == str(group_id)
            assert result.data.name == "Scrypt Rigs"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, riggroup_client: RigGroupClient) -> None:
        """Test get_by_id with not found error."""
        group_id = 999
        endpoint = f"/riggroup/{group_id}"
        response_data = {
            "success": False,
            "data": {"message": "Group not found"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.get_by_id(id=group_id)

            assert result.success is False
            assert result.error is not None


class TestRigGroupClientCreate:
    """Tests for RigGroupClient.create method."""

    @pytest.mark.asyncio
    async def test_create_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful create request."""
        endpoint = "/riggroup"
        body = RigGroupCreateBody(name="New Group", rental_limit=15)
        response_data = {"success": True, "data": {"id": 3, "message": "Group created"}}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.create(body)

            assert result.success is True
            assert result.data is not None
            assert result.data["id"] == 3
            assert result.data["message"] == "Group created"


class TestRigGroupClientUpdate:
    """Tests for RigGroupClient.update method."""

    @pytest.mark.asyncio
    async def test_update_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful update request."""
        group_id = 1
        endpoint = f"/riggroup/{group_id}"
        body = RigGroupUpdateBody(name="Updated Name", rental_limit=20)
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.update(id=group_id, body=body)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_update_partial(self, riggroup_client: RigGroupClient) -> None:
        """Test update with partial body."""
        group_id = 1
        endpoint = f"/riggroup/{group_id}"
        body = RigGroupUpdateBody(name="Only Name Changed")
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.update(id=group_id, body=body)

            assert result.success is True


class TestRigGroupClientDelete:
    """Tests for RigGroupClient.delete method."""

    @pytest.mark.asyncio
    async def test_delete_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful delete request."""
        group_id = 1
        endpoint = f"/riggroup/{group_id}"
        response_data = {"success": True, "data": {"id": group_id, "message": "Group deleted"}}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.delete(id=group_id)

            assert result.success is True
            assert result.data is not None
            assert result.data["message"] == "Group deleted"


class TestRigGroupClientAddRigs:
    """Tests for RigGroupClient.add_rigs method."""

    @pytest.mark.asyncio
    async def test_add_rigs_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful add_rigs request."""
        group_id = 1
        rig_ids = [12345, 12346]
        rig_ids_str = "12345;12346"
        endpoint = f"/riggroup/{group_id}/add/{rig_ids_str}"
        response_data = {
            "success": True,
            "data": {"id": group_id, "message": "Rigs added", "rigs": [12345, 12346]},
        }

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.add_rigs(id=group_id, rig_ids=rig_ids)

            assert result.success is True
            assert result.data is not None
            assert result.data["rigs"] == [12345, 12346]

    @pytest.mark.asyncio
    async def test_add_rigs_single(self, riggroup_client: RigGroupClient) -> None:
        """Test add_rigs with single rig."""
        group_id = 1
        rig_ids = [12345]
        rig_ids_str = "12345"
        endpoint = f"/riggroup/{group_id}/add/{rig_ids_str}"
        response_data = {
            "success": True,
            "data": {"id": group_id, "message": "Rig added", "rigs": [12345]},
        }

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.add_rigs(id=group_id, rig_ids=rig_ids)

            assert result.success is True
            assert result.data is not None


class TestRigGroupClientRemoveRigs:
    """Tests for RigGroupClient.remove_rigs method."""

    @pytest.mark.asyncio
    async def test_remove_rigs_success(self, riggroup_client: RigGroupClient) -> None:
        """Test successful remove_rigs request."""
        group_id = 1
        rig_ids = [12345, 12346]
        rig_ids_str = "12345;12346"
        endpoint = f"/riggroup/{group_id}/remove/{rig_ids_str}"
        response_data = {
            "success": True,
            "data": {"id": group_id, "message": "Rigs removed", "rigs": [12345, 12346]},
        }

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.remove_rigs(id=group_id, rig_ids=rig_ids)

            assert result.success is True
            assert result.data is not None
            assert result.data["rigs"] == [12345, 12346]

    @pytest.mark.asyncio
    async def test_remove_rigs_single(self, riggroup_client: RigGroupClient) -> None:
        """Test remove_rigs with single rig."""
        group_id = 1
        rig_ids = [12345]
        rig_ids_str = "12345"
        endpoint = f"/riggroup/{group_id}/remove/{rig_ids_str}"
        response_data = {
            "success": True,
            "data": {"id": group_id, "message": "Rig removed", "rigs": [12345]},
        }

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await riggroup_client.remove_rigs(id=group_id, rig_ids=rig_ids)

            assert result.success is True
            assert result.data is not None

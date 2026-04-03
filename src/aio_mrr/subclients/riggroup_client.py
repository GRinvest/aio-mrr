"""RigGroup Client for interacting with the RigGroup API.

This module provides RigGroupClient for working with RigGroup API endpoints:
- GET /riggroup — Get list of rig groups
- PUT /riggroup — Create new rig group
- GET /riggroup/{id} — Get rig group details
- PUT /riggroup/{id} — Update rig group
- DELETE /riggroup/{id} — Delete rig group
- POST /riggroup/{id}/add/{rig_ids} — Add rigs to group
- POST /riggroup/{id}/remove/{rig_ids} — Remove rigs from group
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.riggroup.request import RigGroupCreateBody, RigGroupUpdateBody
from aio_mrr.models.riggroup.response import RigGroupInfo
from aio_mrr.subclients.base import BaseSubClient


class RigGroupClient(BaseSubClient):
    """Client for working with the RigGroup API.

    Provides methods for managing mining rig groups:
    - creating and deleting groups
    - updating group information
    - adding and removing rigs from groups

    Usage example:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.riggroup_client.get_list()
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initializes RigGroupClient.

        Args:
            http_client: HTTPClient instance for performing requests.
        """
        super().__init__(http_client)

    async def get_list(self) -> MRRResponse[list[RigGroupInfo]]:
        """Retrieves the list of your rig groups.

        Returns:
            MRRResponse[list[RigGroupInfo]] — response with group list:
            - On success: MRRResponse(success=True, data=[RigGroupInfo, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves rig group details by ID.

        Args:
            id: Rig group identifier.

        Returns:
            MRRResponse[RigGroupInfo] — response with group information:
            - On success: MRRResponse(success=True, data=RigGroupInfo)
            - On error: MRRResponse(success=False, error=...)

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
        """Creates a new rig group.

        Args:
            body: Request body with group creation parameters.

        Returns:
            MRRResponse[dict] — response with created group ID:
            - On success: MRRResponse(success=True, data={"id": 123, "message": "..."})
            - On error: MRRResponse(success=False, error=...)

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
        """Updates a rig group.

        Args:
            id: Rig group identifier to update.
            body: Request body with update parameters (all fields optional).

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Deletes a rig group.

        Args:
            id: Rig group identifier to delete.

        Returns:
            MRRResponse[dict] — response with deletion confirmation:
            - On success: MRRResponse(success=True, data={"id": 123, "message": "..."})
            - On error: MRRResponse(success=False, error=...)

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
        """Adds rigs to a group.

        Args:
            id: Rig group identifier.
            rig_ids: List of rig IDs to add to the group.

        Returns:
            MRRResponse[dict] — response with addition confirmation:
            - On success: MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})
            - On error: MRRResponse(success=False, error=...)

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
        """Removes rigs from a group.

        Args:
            id: Rig group identifier.
            rig_ids: List of rig IDs to remove from the group.

        Returns:
            MRRResponse[dict] — response with removal confirmation:
            - On success: MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})
            - On error: MRRResponse(success=False, error=...)

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

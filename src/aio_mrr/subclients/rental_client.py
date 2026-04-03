"""Rental Client for interacting with the Rental API.

This module provides RentalClient for working with Rental API endpoints:
- GET /rental — List rentals
- GET /rental/{ids} — Get rental by ID
- PUT /rental — Create new rental
- PUT /rental/{ids}/profile — Apply pool profile to rentals
- GET /rental/{ids}/pool — Get pools assigned to rentals
- PUT /rental/{ids}/pool — Add or replace pool on rentals
- DELETE /rental/{ids}/pool — Remove pool from rentals
- PUT /rental/{ids}/extend — Extend rental
- GET /rental/{ids}/graph — Get rental graph data
- GET /rental/{ids}/log — Get rental activity log
- GET /rental/{ids}/message — Get rental messages
- PUT /rental/{ids}/message — Send message to rental
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
    """Client for working with the Rental API.

    Provides methods for managing mining rig rentals:
    - creating and retrieving rentals
    - managing pools and profiles
    - extending rentals
    - retrieving statistics, graph data, and logs

    Usage example:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.rental.get_list(params={"type": "renter"})
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initializes RentalClient.

        Args:
            http_client: HTTPClient instance for performing requests.
        """
        super().__init__(http_client)

    async def get_list(self, params: dict[str, Any] | None = None) -> MRRResponse[list[RentalInfo]]:
        """Retrieves a list of rentals with filtering and pagination.

        Args:
            params: Query parameters for filtering:
                - type: 'owner' or 'renter'
                - algo: filter by algorithm
                - history: true = completed, false = active
                - rig: filter by rig ID
                - start: pagination start
                - limit: pagination limit
                - currency: currency [BTC,LTC,ETH,DOGE,BCH]

        Returns:
            MRRResponse[list[RentalInfo]] — response with rental list:
            - On success: MRRResponse(success=True, data=[RentalInfo, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves rental information by ID.

        Args:
            ids: List of rental IDs to retrieve (first ID is used).

        Returns:
            MRRResponse[RentalInfo] — response with rental information:
            - On success: MRRResponse(success=True, data=RentalInfo)
            - On error: MRRResponse(success=False, error=...)

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
        """Creates a new rental.

        Args:
            body: Request body with rental creation parameters:
                - rig: Rig ID for rental (required)
                - length: duration in hours (required)
                - profile: Pool profile ID (required)
                - currency: payment currency (default BTC)
                - rate_type: hash type (default 'mh')
                - rate_price: price per hash unit per day

        Returns:
            MRRResponse[dict] — response with created rental ID:
            - On success: MRRResponse(success=True, data={"id": "54321"})
            - On error: MRRResponse(success=False, error=...)

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
        """Applies a pool profile to rentals.

        Args:
            ids: List of rental IDs to update.
            profile: Profile ID to apply.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves pools assigned to rentals.

        Args:
            ids: List of rental IDs to get pools for.

        Returns:
            MRRResponse[list[Pool]] — response with pool list:
            - On success: MRRResponse(success=True, data=[Pool, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Adds or replaces a pool on rentals.

        Args:
            ids: List of rental IDs to update.
            body: Request body with pool data:
                - host: pool host (required)
                - port: pool port (required)
                - user: worker name (required)
                - password: worker password (required)
                - priority: priority (0-4)

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Removes a pool from rentals.

        Removes the pool with the specified priority from rentals.

        Args:
            ids: List of rental IDs to remove the pool from.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Purchases a rental extension.

        Args:
            ids: List of rental IDs to extend.
            length: Hours to extend.
            getcost: If set, simulates extension and returns cost.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

        Example:
            # Extend rental
            >>> response = await rental_client.extend(ids=[54321], length=12)
            >>> if response.success:
            ...     print("Rental extended successfully")

            # Simulate extension cost
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
        """Retrieves rental graph data (historical hashrate, downtimes).

        Args:
            ids: List of rental IDs (first ID is used).
            hours: Hours of data (max. 2 weeks). Default 168.
            interval: Data interval. Default None.

        Returns:
            MRRResponse[GraphData] — response with graph data:
            - On success: MRRResponse(success=True, data=GraphData)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves rental activity log.

        Args:
            ids: List of rental IDs to get logs for (first ID is used).

        Returns:
            MRRResponse[list[RentalLogEntry]] — response with log entries:
            - On success: MRRResponse(success=True, data=[RentalLogEntry, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves rental messages.

        Args:
            ids: List of rental IDs to get messages for (first ID is used).

        Returns:
            MRRResponse[list[RentalMessage]] — response with message list:
            - On success: MRRResponse(success=True, data=[RentalMessage, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Sends a message to a rental.

        Args:
            ids: List of rental IDs to send message to (first ID is used).
            message: Message text.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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

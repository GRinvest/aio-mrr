"""Rig Client for interacting with the Rig API.

This module provides RigClient for working with Rig API endpoints:
- GET /rig — Search rigs by algorithm
- GET /rig/mine — List your rigs
- GET /rig/{ids} — Get rigs by ID
- PUT /rig — Create new rig
- POST /rig/batch — Batch update rigs
- DELETE /rig/{ids} — Delete rigs
- PUT /rig/{ids}/extend — Extend rig rental
- POST /rig/batch/extend — Batch extend rentals
- PUT /rig/{ids}/profile — Apply pool profile to rigs
- GET /rig/{ids}/pool — Get pools assigned to rigs
- PUT /rig/{ids}/pool — Add or replace pool on rigs
- DELETE /rig/{ids}/pool — Remove pool from rigs
- GET /rig/{ids}/port — Get direct port number
- GET /rig/{ids}/threads — Get list of active threads
- GET /rig/{ids}/graph — Get rig graph data
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
    """Client for working with the Rig API.

    Provides methods for managing mining rigs:
    - searching and filtering rigs
    - creating and deleting rigs
    - extending rentals
    - managing pools and profiles
    - retrieving statistics and graph data

    Usage example:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.rig_client.search_rigs(type="scrypt")
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initializes RigClient.

        Args:
            http_client: HTTPClient instance for performing requests.
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
        """Searches rigs by algorithm with filtering and sorting.

        Equivalent to the main rig listing page on the MRR website.

        Args:
            type: Algorithm: sha256, scrypt, x11, etc. (required).
            currency: Currency: [BTC,LTC,ETH,DOGE,BCH]. Default BTC.
            minhours_min: Minimum hours.
            minhours_max: Maximum hours.
            maxhours_min: Minimum maximum time.
            maxhours_max: Maximum maximum time.
            rpi_min: Minimum RPI (0-100).
            rpi_max: Maximum RPI (0-100).
            hash_min: Minimum hashrate.
            hash_max: Maximum hashrate.
            hash_type: Type: [hash,kh,mh,gh,th,ph,eh]. Default mh.
            price_min: Minimum price.
            price_max: Maximum price.
            price_type: Hash type for price.
            offline: Show offline rigs. Default false.
            rented: Show rented. Default false.
            region_type: 'include' or 'exclude'.
            expdiff: Expected worker difficulty.
            count: Number of results (max. 100). Default 100.
            islive: Filter for rigs with hashrate [yes].
            xnonce: Filter by xnonce [yes,no].
            offset: Pagination offset. Default 0.
            orderby: Sorting. Default score.
            orderdir: Direction [asc,desc]. Default asc.

        Returns:
            MRRResponse[list[RigInfo]] — response with rig list:
            - On success: MRRResponse(success=True, data=[RigInfo, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves the list of your rigs.

        Args:
            type: Filter by algorithm.
            hashrate: Show hashrate calculation.

        Returns:
            MRRResponse[list[RigInfo]] — response with your rig list:
            - On success: MRRResponse(success=True, data=[RigInfo, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves one or more rigs by ID.

        Args:
            ids: List of rig IDs to retrieve.
            fields: Filter root level fields (e.g., ["name", "status"]).

        Returns:
            MRRResponse[list[RigInfo]] — response with rig list:
            - On success: MRRResponse(success=True, data=[RigInfo, ...])
            - On error: MRRResponse(success=False, error=...)

        Example:
            >>> response = await rig_client.get_rigs(ids=[12345, 12346])
            >>> if response.success:
            ...     for rig in response.data:
            ...         print(f"{rig.id}: {rig.name}")
        """
        # Form the ID string: "12345;12346;12347"
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
        """Creates a new rig.

        Args:
            body: Request body with rig creation parameters.

        Returns:
            MRRResponse[dict] — response with created rig ID:
            - On success: MRRResponse(success=True, data={"id": 12345})
            - On error: MRRResponse(success=False, error=...)

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
        """Batch updates rigs.

        Args:
            body: Request body with list of rigs to update.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Deletes one or more rigs by ID.

        Args:
            ids: List of rig IDs to delete.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Extends rig rental (for owners).

        Args:
            ids: List of rig IDs to extend.
            hours: Hours to extend.
            minutes: Minutes to extend.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Batch extends rentals for multiple rigs.

        Args:
            rig_hours: Dictionary {rig_id: hours} for extension.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Applies a pool profile to one or more rigs.

        Args:
            ids: List of rig IDs to update.
            profile: Profile ID to apply.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves pools assigned to rigs.

        Args:
            ids: List of rig IDs to get pools for.

        Returns:
            MRRResponse[list[Pool]] — response with pool list:
            - On success: MRRResponse(success=True, data=[Pool, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Adds or replaces a pool on rigs.

        Args:
            ids: List of rig IDs to update.
            body: Request body with pool data.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Removes a pool from rigs.

        Removes the pool with the specified priority from rigs.

        Args:
            ids: List of rig IDs to remove the pool from.

        Returns:
            MRRResponse[None] — response:
            - On success: MRRResponse(success=True, data=None)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves direct port number for server connection.

        Args:
            ids: List of rig IDs (first ID is used).

        Returns:
            MRRResponse[RigPortInfo] — response with port information:
            - On success: MRRResponse(success=True, data=RigPortInfo)
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves list of active threads for rigs.

        Args:
            ids: List of rig IDs to get threads for.

        Returns:
            MRRResponse[list[RigThreadInfo]] — response with thread list:
            - On success: MRRResponse(success=True, data=[RigThreadInfo, ...])
            - On error: MRRResponse(success=False, error=...)

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
        """Retrieves rig graph data (historical hashrate, downtimes).

        Args:
            ids: List of rig IDs (first ID is used).
            hours: Hours of data (max. 2 weeks). Default 168.
            deflate: Base64 encoding. Default false.

        Returns:
            MRRResponse[RigGraphData] — response with graph data:
            - On success: MRRResponse(success=True, data=RigGraphData)
            - On error: MRRResponse(success=False, error=...)

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

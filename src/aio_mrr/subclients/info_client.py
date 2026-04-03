"""Info Client for interacting with the Info API.

This module provides InfoClient for working with Info API endpoints:
- GET /info/servers
- GET /info/algos
- GET /info/algos/{name}
- GET /info/currencies
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.info.response import AlgoInfo, CurrencyInfo, ServerInfo, ServersList
from aio_mrr.subclients.base import BaseSubClient


class InfoClient(BaseSubClient):
    """Client for working with the Info API.

    Provides methods for retrieving system information:
    - list of servers
    - mining algorithm information
    - list of available currencies

    Usage example:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.info_client.get_servers()
        ...     if response.success:
        ...         print(response.data.servers)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initializes InfoClient.

        Args:
            http_client: HTTPClient instance for performing requests.
        """
        super().__init__(http_client)

    async def get_servers(self) -> MRRResponse[ServersList]:
        """Retrieves the list of MRR servers.

        Returns information about all available MiningRigRentals servers,
        including their identifiers, names, regions, and ports.

        > Note: The port and ethereum_port fields are deprecated. Use /rig/port
        to get up-to-date port information.

        Returns:
            MRRResponse[ServersList] — response with server list:
            - On success: MRRResponse(success=True, data=ServersList)
            - On error: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_servers()
            >>> if response.success:
            ...     for server in response.data.servers:
            ...         print(f"{server.name} - {server.region}")
        """
        endpoint = "/info/servers"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            servers_data: list[dict[str, Any]] = result.data
            servers_list = ServersList(servers=[ServerInfo.model_validate(s) for s in servers_data])
            return MRRResponse(
                success=True,
                data=servers_list,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_algos(self, currency: str | None = None) -> MRRResponse[list[AlgoInfo]]:
        """Retrieves the list of all mining algorithms.

        Returns information about all available mining algorithms,
        including suggested prices, hashrate statistics, and current prices.

        Args:
            currency: Currency for prices (BTC, LTC, ETH, DOGE, BCH).
                     Default BTC.

        Returns:
            MRRResponse[list[AlgoInfo]] — response with algorithm list:
            - On success: MRRResponse(success=True, data=[AlgoInfo, ...])
            - On error: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_algos(currency="BTC")
            >>> if response.success:
            ...     for algo in response.data:
            ...         print(f"{algo.display}: {algo.suggested_price.amount}")
        """
        endpoint = "/info/algos"
        params: dict[str, Any] = {}

        if currency is not None:
            params["currency"] = currency

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            algos_data: list[dict[str, Any]] = result.data
            algos = [AlgoInfo.model_validate(a) for a in algos_data]
            return MRRResponse(
                success=True,
                data=algos,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_algo(self, name: str, currency: str | None = None) -> MRRResponse[AlgoInfo]:
        """Retrieves information about a specific mining algorithm.

        Returns detailed information about a single algorithm, including
        suggested prices, hashrate statistics, and current market prices.

        Args:
            name: Algorithm name (e.g., "scrypt", "sha256", "x11").
            currency: Currency for prices (BTC, LTC, ETH, DOGE, BCH).
                     Default BTC.

        Returns:
            MRRResponse[AlgoInfo] — response with algorithm information:
            - On success: MRRResponse(success=True, data=AlgoInfo)
            - On error: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_algo(name="scrypt", currency="BTC")
            >>> if response.success:
            ...     algo = response.data
            ...     print(f"{algo.display}: {algo.stats.available.rigs} rigs available")
        """
        endpoint = f"/info/algos/{name}"
        params: dict[str, Any] = {}

        if currency is not None:
            params["currency"] = currency

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            algo_data: dict[str, Any] = result.data
            algo = AlgoInfo.model_validate(algo_data)
            return MRRResponse(
                success=True,
                data=algo,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_currencies(self) -> MRRResponse[list[CurrencyInfo]]:
        """Retrieves the list of available currencies for payments.

        Returns information about all currencies that can be used
        to pay for rig rentals. Each currency has an availability status
        and a withdrawal fee.

        > Note: The txfee may change every 15 minutes.

        Returns:
            MRRResponse[list[CurrencyInfo]] — response with currency list:
            - On success: MRRResponse(success=True, data=[CurrencyInfo, ...])
            - On error: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_currencies()
            >>> if response.success:
            ...     for curr in response.data:
            ...         print(f"{curr.name}: enabled={curr.enabled}, txfee={curr.txfee}")
        """
        endpoint = "/info/currencies"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            # Response has structure {"currencies": [...]}
            currencies_data: dict[str, list[dict[str, Any]]] = result.data
            currencies_list = currencies_data.get("currencies", [])
            currencies = [CurrencyInfo.model_validate(c) for c in currencies_list]
            return MRRResponse(
                success=True,
                data=currencies,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

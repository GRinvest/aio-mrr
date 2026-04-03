"""MRRClient — main facade of the aio-mrr library.

This module provides MRRClient — the single entry point for interacting
with MiningRigRentals API v2. The client uses the Facade pattern to simplify
access to all API subsystems through a unified interface.

Author: GRinvest / SibNeuroTech
License: MIT

Usage pattern:
    async with MRRClient(
        api_key="YOUR_KEY",
        api_secret="YOUR_SECRET",
        connect_timeout=30.0,
        read_timeout=60.0,
        max_retries=3,
    ) as client:
        response = await client.account.get_balance()
        if response.success:
            print(response.data)
"""

from __future__ import annotations

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.subclients.account_client import AccountClient
from aio_mrr.subclients.info_client import InfoClient
from aio_mrr.subclients.pricing_client import PricingClient
from aio_mrr.subclients.rental_client import RentalClient
from aio_mrr.subclients.rig_client import RigClient
from aio_mrr.subclients.riggroup_client import RigGroupClient


class MRRClient:
    """Main facade for interacting with MiningRigRentals API v2.

    This class provides a single entry point for all API operations.
    It creates and manages the lifecycle of all sub-clients and the HTTP session.

    Attributes:
        info: Client for /info/* endpoints.
        account: Client for /account/* endpoints.
        rig: Client for /rig/* endpoints.
        riggroup: Client for /riggroup/* endpoints.
        rental: Client for /rental/* endpoints.
        pricing: Client for /pricing endpoint.

    Example:
        >>> async with MRRClient(
        ...     api_key="YOUR_KEY",
        ...     api_secret="YOUR_SECRET",
        ... ) as client:
        ...     response = await client.account.get_balance()
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        connect_timeout: float = 30.0,
        read_timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        """Initializes MRRClient.

        Args:
            api_key: MRR API key.
            api_secret: MRR API secret.
            connect_timeout: Connection timeout in seconds (default: 30.0).
            read_timeout: Read timeout in seconds (default: 60.0).
            max_retries: Maximum number of retry attempts (default: 3).
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._max_retries = max_retries

        # HTTP-client with shared settings
        self._http_client = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            max_retries=max_retries,
        )

        # Sub-clients with shared HTTP-client
        self.info: InfoClient = InfoClient(http_client=self._http_client)
        self.account: AccountClient = AccountClient(http_client=self._http_client)
        self.rig: RigClient = RigClient(http_client=self._http_client)
        self.riggroup: RigGroupClient = RigGroupClient(http_client=self._http_client)
        self.rental: RentalClient = RentalClient(http_client=self._http_client)
        self.pricing: PricingClient = PricingClient(http_client=self._http_client)

    async def __aenter__(self) -> MRRClient:
        """Async context manager entry.

        Returns:
            MRRClient: The client instance for use in async with.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Async context manager exit.

        Closes the HTTP session when exiting the context.

        Args:
            exc_type: Exception type if one occurred.
            exc_val: Exception value if one occurred.
            exc_tb: Stack trace if one occurred.
        """
        await self._http_client.close()

    async def whoami(self) -> MRRResponse[dict[str, str]]:
        """Retrieves information about the current user.

        Performs a GET request to the /whoami endpoint to obtain
        information about the authenticated user.

        Returns:
            MRRResponse[dict] — response with user information:
            - success: True if the request succeeded
            - data: Dictionary with userid and username fields
            - error: Error information if success=False

        Example:
            >>> response = await client.whoami()
            >>> if response.success:
            ...     print(f"User: {response.data['username']}")
            ... else:
            ...     print(f"Error: {response.error.message}")
        """
        return await self._http_client.request(method="GET", endpoint="/whoami")

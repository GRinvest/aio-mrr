"""Base sub-client for the aio-mrr library.

This module provides the base class for all sub-clients with HTTPClient
dependency injection. Sub-clients inherit from BaseSubClient and receive the HTTP client
through the constructor, delegating session management, retry, timeouts, and authentication to it.

Author: GRinvest / SibNeuroTech
License: MIT
"""

from __future__ import annotations

from aio_mrr.http.http_client import HTTPClient


class BaseSubClient:
    """Base class for all sub-clients.

    This class provides the common structure for all library sub-clients,
    receiving HTTPClient via dependency injection. All subclasses should
    use self._http to perform HTTP requests.
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initializes the base sub-client.

        Args:
            http_client: HTTPClient instance for performing requests.
        """
        self._http: HTTPClient = http_client

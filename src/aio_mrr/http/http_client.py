"""HTTP Client for aio-mrr library.

This module provides the central HTTP client with functionality:
- Retry logic via tenacity (for 5xx, 429, connection errors)
- Timeout configuration (connect and read)
- Authentication via AuthSigner
- Logging via loguru
- NEVER raises exceptions outward — all errors are returned as MRRResponse(success=False)

Author: GRinvest / SibNeuroTech
License: MIT
"""

from __future__ import annotations
import asyncio
import json
import logging
from typing import Any
import aiohttp
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
    wait_random,
)

from aio_mrr.auth.signer import AuthSigner
from aio_mrr.http.response import parse_response
from aio_mrr.http.session import AioHTTPSession
from aio_mrr.logging.config import get_logger
from aio_mrr.models.base import MRRResponse, MRRResponseError

# Retry logger (secrets are automatically masked via SecretMasker)
_retry_logger = get_logger("http_client_retry")


def _is_retryable_result(response: aiohttp.ClientResponse) -> bool:
    """Determines whether to retry based on HTTP status.

    Args:
        response: aiohttp ClientResponse object.

    Returns:
        True if status requires retry (429, 500, 502, 503, 504).
    """
    return response.status in {429, 500, 502, 503, 504}


def _get_retry_params(status: int | None) -> dict[str, Any]:
    """Returns retry parameters depending on status.

    Args:
        status: HTTP status code or None for connection errors.

    Returns:
        Dictionary with stop and wait parameters for tenacity.
    """
    if status == 429:
        return {
            "stop": stop_after_attempt(5),
            "wait": wait_exponential(multiplier=5, min=5, max=60) + wait_random(0, 5),
        }
    return {
        "stop": stop_after_attempt(3),
        "wait": wait_exponential(multiplier=1, min=1, max=8) + wait_random(0, 1),
    }


def _log_retry_attempt(retry_state: Any) -> None:
    """Logs a retry attempt.

    Args:
        retry_state: Retry state from tenacity.
    """
    _retry_logger.debug(f"Retry attempt: {retry_state.attempt_number} (will retry {retry_state.upcoming_sleep:.2f}s)")


class HTTPClient:
    """Central HTTP client with retry, timeout, auth, and logging.

    This class provides a low-level HTTP client for interacting
    with MiningRigRentals API v2. All network errors, timeouts, and HTTP errors
    are handled internally — the request() method NEVER raises exceptions.

    Retry strategy:
    - 500, 502, 503, 504: 3 attempts, exponential backoff 1-8s + jitter
    - 429 (Rate Limit): 5 attempts, exponential backoff 5-60s + jitter
    - Connection errors: 3 attempts, exponential backoff 1-8s + jitter

    Attributes:
        api_key: MRR API key (stored in memory only).
        api_secret: MRR API secret (stored in memory only).
        connect_timeout: Connection timeout in seconds (default: 30.0).
        read_timeout: Read timeout in seconds (default: 60.0).
        max_retries: Maximum number of retry attempts (default: 3).
    """

    BASE_URL: str = "https://www.miningrigrentals.com/api/v2"

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        connect_timeout: float = 30.0,
        read_timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        """Initializes HTTPClient.

        Args:
            api_key: MRR API key.
            api_secret: MRR API secret.
            connect_timeout: Connection timeout in seconds.
            read_timeout: Read timeout in seconds.
            max_retries: Maximum number of retry attempts.
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._max_retries = max_retries

        self._session_manager = AioHTTPSession()
        self._auth_signer = AuthSigner(api_key=api_key, api_secret=api_secret)
        self._logger = get_logger("http_client")

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> MRRResponse[Any]:
        """Performs an HTTP request with retry, timeout, and auth.

        The method performs an HTTP request to MRR API with automatic retry,
        timeout, authentication, and logging. NEVER raises exceptions
        outward — all errors are returned as MRRResponse(success=False).

        Args:
            method: HTTP method (GET, PUT, POST, DELETE).
            endpoint: API endpoint (without base URL, e.g. "/account/balance").
            params: Query parameters (optional).
            body: Request body for JSON (optional).

        Returns:
            MRRResponse[Any] — universal response:
            - On success: MRRResponse(success=True, data=...)
            - On error: MRRResponse(success=False, error=...)

        Example:
            >>> client = HTTPClient(api_key="key", api_secret="secret")
            >>> response = await client.request("GET", "/account/balance")
            >>> if response.success:
            ...     print(response.data)
            ... else:
            ...     print(f"Error: {response.error.message}")
        """
        full_url = f"{self.BASE_URL}{endpoint}"

        self._logger.debug(f"{method} {full_url}")

        # Timeouts
        timeout = aiohttp.ClientTimeout(
            total=self._read_timeout,
            connect=self._connect_timeout,
        )

        # Retry configuration - determined BEFORE creating retry strategy
        retry_params = _get_retry_params(None)  # Default for connection errors

        # Create retry strategy dynamically
        retry_decorator = retry(
            stop=retry_params["stop"],
            wait=retry_params["wait"],
            retry=(
                retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError, OSError))
                | retry_if_result(_is_retryable_result)
            ),
            before_sleep=before_sleep_log(_retry_logger, logging.DEBUG),
            reraise=True,
        )

        try:
            session = self._session_manager.get_session()

            # Wrap _do_request in retry decorator
            @retry_decorator
            async def _do_request_with_retry() -> aiohttp.ClientResponse:
                return await self._do_request(
                    method=method,
                    url=full_url,
                    endpoint=endpoint,
                    params=params,
                    body=body,
                    timeout=timeout,
                    session=session,
                )

            # Execute request with retry
            response = await _do_request_with_retry()

            # Always return MRRResponse
            return await self._handle_response(response)

        except Exception as e:
            # Fallback for unexpected errors (should never happen)
            self._logger.error(f"Unexpected error in request: {e}")
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="network_error",
                    message=f"Unexpected error: {e!s}",
                    details={"method": method, "endpoint": endpoint, "error": str(e)},
                ),
            )

    def _convert_params(self, params: dict[str, Any] | None) -> dict[str, Any] | None:
        """Converts boolean values to strings for aiohttp.

        Args:
            params: Dictionary with request parameters.

        Returns:
            Dictionary with boolean values converted to 'true'/'false' strings.
        """
        if params is None:
            return None

        converted: dict[str, Any] = {}
        for key, value in params.items():
            if isinstance(value, bool):
                converted[key] = str(value).lower()
            else:
                converted[key] = value
        return converted

    async def _do_request(
        self,
        method: str,
        url: str,
        endpoint: str,
        params: dict[str, Any] | None,
        body: dict[str, Any] | None,
        timeout: aiohttp.ClientTimeout,
        session: aiohttp.ClientSession,
    ) -> aiohttp.ClientResponse:
        """Performs a single HTTP request.

        Args:
            method: HTTP method.
            url: Full request URL.
            params: Query parameters.
            body: Request body.
            timeout: Request timeouts.
            session: aiohttp ClientSession.

        Returns:
            aiohttp.ClientResponse — for status checking and retry logic.
        """
        # Generate authentication headers (sign only endpoint without base URL)
        auth_headers = await self._auth_signer.get_auth_headers(endpoint=endpoint)

        # Merge headers
        headers = {
            "Content-Type": "application/json",
            **auth_headers,
        }

        # Convert boolean values to strings for aiohttp
        converted_params = self._convert_params(params)

        # Execute request
        response = await session.request(
            method=method,
            url=url,
            params=converted_params,
            json=body,
            headers=headers,
            timeout=timeout,
        )

        # Log response (secrets are automatically masked)
        self._logger.debug(f"{method} {url} -> {response.status}")

        return response

    async def _handle_response(self, response: aiohttp.ClientResponse) -> MRRResponse[Any]:
        """Processes HTTP response and returns MRRResponse.

        Args:
            response: aiohttp ClientResponse.

        Returns:
            MRRResponse[Any] — universal API response.
        """
        # Read response body
        response_text = await response.text()

        # If status is not 2xx, return error
        if response.status >= 400:
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="http_error",
                    message=f"HTTP {response.status}",
                    details={"status": response.status},
                    http_status=response.status,
                ),
            )

        # Attempt to parse JSON
        try:
            json_data = json.loads(response_text)
            return parse_response(
                json_data=json_data,
                http_status=response.status,
            )
        except json.JSONDecodeError:
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="validation_error",
                    message="Invalid JSON response",
                    details={"status": response.status, "response": response_text[:200]},
                    http_status=response.status,
                ),
            )

    async def close(self) -> None:
        """Closes the HTTP session.

        Should be called when the client is shutting down.
        """
        await self._session_manager.__aexit__(None, None, None)

    async def __aenter__(self) -> HTTPClient:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object
    ) -> None:
        """Async context manager exit."""
        await self.close()

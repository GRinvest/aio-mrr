"""HTTP Response parsing for aio-mrr library.

This module provides functionality for parsing JSON responses from MRR API
into typed MRRResponse objects.

Includes:
- parse_response: Standalone function for parsing API responses
- ResponseParser: Class-based parser with extensible configuration

Author: GRinvest / SibNeuroTech
License: MIT
"""

from __future__ import annotations
import json
from typing import Any, Generic, TypeVar

from aio_mrr.models.base import MRRResponse, MRRResponseError

T = TypeVar("T")


def parse_response(
    json_data: dict[str, Any],
    http_status: int | None = None,
    retry_count: int = 0,
) -> MRRResponse[Any]:
    """Parse a raw JSON response from MRR API.

    This function handles both successful responses and API errors according
    to the MRR API contract:
    - Success: {"success": true, "data": { ... }}
    - Error: {"success": false, "data": {"message": "..."}}

    Args:
        json_data: Parsed JSON data from API response.
        http_status: HTTP status code (optional).
        retry_count: Number of retry attempts made (default 0).

    Returns:
        MRRResponse[Any]: Parsed response with success/error status and data.

    Examples:
        >>> # Successful response
        >>> data = {"success": True, "data": {"balance": "0.1"}}
        >>> response = parse_response(data, http_status=200)
        >>> response.success
        True
        >>> response.data
        {'balance': '0.1'}

        >>> # Error response
        >>> data = {"success": False, "data": {"message": "Invalid API key"}}
        >>> response = parse_response(data, http_status=401)
        >>> response.success
        False
        >>> response.error.message
        'Invalid API key'
    """
    success = json_data.get("success", False)
    raw_data = json_data.get("data")

    if success:
        return MRRResponse(
            success=True,
            data=raw_data,
            error=None,
            http_status=http_status,
            retry_count=retry_count,
        )
    else:
        # Parse error from data field
        error_data = raw_data if isinstance(raw_data, dict) else {}
        error_message = error_data.get("message", "Unknown API error")

        error = MRRResponseError(
            code="api_error",
            message=error_message,
            details=error_data if error_data else None,
            http_status=http_status,
        )

        return MRRResponse(
            success=False,
            data=None,
            error=error,
            http_status=http_status,
            retry_count=retry_count,
        )


class ResponseParser(Generic[T]):
    """Parser for MRR API responses with type support.

    This class provides a configurable parser for converting raw JSON responses
    into typed MRRResponse objects. It handles:
    - Successful responses with typed data
    - API errors with detailed error information
    - Invalid JSON as validation errors

    Attributes:
        http_status: HTTP status code from the response (optional).
        retry_count: Number of retry attempts made (default 0).

    Examples:
        >>> parser = ResponseParser[int]()
        >>> data = {"success": True, "data": 42}
        >>> response = parser.parse(data)
        >>> response.success
        True
        >>> response.data
        42
    """

    def __init__(
        self,
        http_status: int | None = None,
        retry_count: int = 0,
    ) -> None:
        """Initialize the response parser.

        Args:
            http_status: HTTP status code from the response (optional).
            retry_count: Number of retry attempts made (default 0).
        """
        self.http_status = http_status
        self.retry_count = retry_count

    def parse(self, json_data: dict[str, Any]) -> MRRResponse[T]:
        """Parse a raw JSON response from MRR API.

        Args:
            json_data: Parsed JSON data from API response.

        Returns:
            MRRResponse[T]: Parsed response with success/error status and data.
        """
        return parse_response(
            json_data,
            http_status=self.http_status,
            retry_count=self.retry_count,
        )

    @staticmethod
    def from_json_string(
        json_string: str,
        http_status: int | None = None,
        retry_count: int = 0,
    ) -> MRRResponse[Any]:
        """Parse a JSON string response from MRR API.

        This static method handles JSON parsing errors and returns an
        appropriate MRRResponse with error details.

        Args:
            json_string: Raw JSON string from API response.
            http_status: HTTP status code from the response (optional).
            retry_count: Number of retry attempts made (default 0).

        Returns:
            MRRResponse[Any]: Parsed response or error response if JSON is invalid.

        Examples:
            >>> # Valid JSON
            >>> response = ResponseParser.from_json_string('{"success": true, "data": {}}')
            >>> response.success
            True

            >>> # Invalid JSON
            >>> response = ResponseParser.from_json_string('not valid json')
            >>> response.success
            False
            >>> response.error.code
            'validation_error'
        """
        try:
            json_data = json.loads(json_string)
            if not isinstance(json_data, dict):
                return MRRResponse(
                    success=False,
                    data=None,
                    error=MRRResponseError(
                        code="validation_error",
                        message="Invalid response format: expected JSON object",
                        details={"received_type": type(json_data).__name__},
                        http_status=http_status,
                    ),
                    http_status=http_status,
                    retry_count=retry_count,
                )
            return parse_response(json_data, http_status=http_status, retry_count=retry_count)
        except json.JSONDecodeError as e:
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="validation_error",
                    message="Invalid JSON response",
                    details={
                        "error": str(e),
                        "pos": e.pos,
                        "lineno": e.lineno,
                        "colno": e.colno,
                    },
                    http_status=http_status,
                ),
                http_status=http_status,
                retry_count=retry_count,
            )

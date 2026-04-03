"""Exception hierarchy for the aio-mrr library.

These exceptions are intended for internal use and for optional
try/except in the parent application. All errors in the library are returned
as MRRResponse(success=False, error=...), but exceptions can be useful
for debugging and specific handling.
"""

from typing import Any


class MRRBaseError(Exception):
    """Base class for all aio-mrr exceptions."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """
        Args:
            message: Human-readable error description.
            details: Additional error data.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class MRRNetworkError(MRRBaseError):
    """Exception for network errors (aiohttp, connection errors)."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        """
        Args:
            message: Human-readable error description.
            details: Additional error data.
            host: Host that failed to connect.
            port: Port that failed to connect.
        """
        error_details = details or {}
        if host is not None:
            error_details["host"] = host
        if port is not None:
            error_details["port"] = port
        super().__init__(message, error_details)


class MRRAPIError(MRRBaseError):
    """Exception for MRR API errors (HTTP status >= 400)."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        http_status: int | None = None,
        error_code: str | None = None,
    ) -> None:
        """
        Args:
            message: Human-readable error description.
            details: Additional error data.
            http_status: HTTP status code of the response.
            error_code: Error code from the API.
        """
        error_details = details or {}
        if http_status is not None:
            error_details["http_status"] = http_status
        if error_code is not None:
            error_details["error_code"] = error_code
        super().__init__(message, error_details)
        self.http_status = http_status
        self.error_code = error_code


class MRRValidationError(MRRBaseError):
    """Exception for Pydantic validation errors."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        model_name: str | None = None,
        field: str | None = None,
    ) -> None:
        """
        Args:
            message: Human-readable error description.
            details: Additional error data.
            model_name: Pydantic model name.
            field: Field that failed validation.
        """
        error_details = details or {}
        if model_name is not None:
            error_details["model_name"] = model_name
        if field is not None:
            error_details["field"] = field
        super().__init__(message, error_details)
        self.model_name = model_name
        self.field = field


class MRRTimeoutError(MRRNetworkError):
    """Exception for timeout errors."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        timeout_type: str | None = None,
        timeout_value: float | None = None,
    ) -> None:
        """
        Args:
            message: Human-readable error description.
            details: Additional error data.
            timeout_type: Type of timeout ('connect' or 'read').
            timeout_value: Timeout value in seconds.
        """
        error_details = details or {}
        if timeout_type is not None:
            error_details["timeout_type"] = timeout_type
        if timeout_value is not None:
            error_details["timeout_value"] = timeout_value
        super().__init__(message, error_details)
        self.timeout_type = timeout_type
        self.timeout_value = timeout_value

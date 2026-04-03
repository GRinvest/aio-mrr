"""Base Pydantic models for the aio-mrr library.

This module contains:
- Base BaseModel class with extra='ignore' for resilience to MRR API changes.
- MRRResponseError - model for error details.
- MRRResponse - universal generic Result object for API responses.

Author: GRinvest / SibNeuroTech
License: MIT
"""

from __future__ import annotations
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseMRRModel(BaseModel):
    """Base model for all aio-mrr models.

    Uses extra='ignore' for resilience to MRR API changes (BETA).
    All models inherit from this class.
    """

    model_config = ConfigDict(extra="ignore")


class MRRResponseError(BaseMRRModel):
    """Error details in API response.

    Attributes:
        code: Error code (e.g., "network_error", "api_error",
              "validation_error", "timeout").
        message: Human-readable error description.
        details: Additional error data (optional).
        http_status: HTTP status code if applicable (optional).
    """

    code: str
    message: str
    details: dict[str, Any] | None = None
    http_status: int | None = None


class MRRResponse(BaseMRRModel, Generic[T]):
    """Universal response from the aio-mrr library.

    Wrapper around MiningRigRentals API responses with typing support.

    Attributes:
        success: Flag indicating request success.
        data: Response data (optional, depends on success).
        error: Error details on failure (optional).
        http_status: HTTP status code of the response (optional).
        retry_count: Number of retry attempts (default 0).
    """

    success: bool
    data: T | None = None
    error: MRRResponseError | None = None
    http_status: int | None = None
    retry_count: int = 0

"""Exceptions for the aio-mrr library.

This module exports all exceptions for convenient importing:

    from aio_mrr.exceptions import MRRBaseError, MRRNetworkError

Or directly from aio_mrr:

    from aio_mrr import MRRBaseError
"""

from aio_mrr.exceptions.errors import (
    MRRAPIError,
    MRRBaseError,
    MRRNetworkError,
    MRRTimeoutError,
    MRRValidationError,
)

__all__ = [
    "MRRAPIError",
    "MRRBaseError",
    "MRRNetworkError",
    "MRRTimeoutError",
    "MRRValidationError",
]

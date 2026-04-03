"""Исключения для библиотеки aio-mrr.

Этот модуль экспортирует все исключения для удобства импорта:

    from aio_mrr.exceptions import MRRBaseError, MRRNetworkError

Или напрямую из aio_mrr:

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

"""Logger configuration module for aio-mrr.

This module provides isolated logger configuration using loguru with
secret masking capabilities.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from loguru import logger

from .masker import SecretMasker

if TYPE_CHECKING:
    from typing import Any


# Initialize secret masker
_masker: SecretMasker = SecretMasker()


def get_logger(name: str) -> Any:
    """Creates an isolated logger with secret masking.

    Each logger is isolated via name binding. Secrets are automatically
    masked in output messages via patch().

    Args:
        name: Logger name (e.g., module or component).

    Returns:
        Logger with bound name and secret masking.

    Examples:
        >>> logger = get_logger("http_client")
        >>> logger.info("Request with x-api-key: secret123")
        # Output: Request with x-api-key: ***
    """
    # Create logger with bound name and patch for masking
    # patch is applied to each message before logging
    bound_logger = logger.bind(name=name).patch(
        lambda record: record["extra"].update(_masked_message=masker_mask_func(record["message"]))
    )

    return bound_logger


def masker_mask_func(message: str) -> str:
    """Function for masking the message.

    Args:
        message: Original message.

    Returns:
        Masked message.
    """
    return _masker.mask(message)

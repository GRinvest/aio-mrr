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


# Инициализация маскировщика секретов
_masker: SecretMasker = SecretMasker()


def get_logger(name: str) -> Any:
    """Создаёт изолированный логгер с маскированием секретов.

    Каждый логгер изолирован через привязку имени. Секреты автоматически
    маскируются в выходных сообщениях через patch().

    Args:
        name: Имя логгера (например, модуля или компонента).

    Returns:
        Логгер с привязанным именем и маскированием секретов.

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
    """Функция для маскирования сообщения.

    Args:
        message: Исходное сообщение.

    Returns:
        Замаскированное сообщение.
    """
    return _masker.mask(message)

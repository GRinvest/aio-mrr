"""Sub-clients layer for aio-mrr library.

This module provides business logic sub-clients including:
- BaseSubClient — базовый класс для dependency injection
- InfoClient, AccountClient, RigClient, etc. — специализированные клиенты
"""

from aio_mrr.subclients.base import BaseSubClient

__all__ = ["BaseSubClient"]

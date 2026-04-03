"""Sub-clients layer for aio-mrr library.

This module provides business logic sub-clients including:
- BaseSubClient — base class for dependency injection
- InfoClient, AccountClient, RigClient, etc. — specialized clients
"""

from aio_mrr.subclients.base import BaseSubClient

__all__ = ["BaseSubClient"]

"""Client layer for aio-mrr library.

This module provides the main facade client including:
- MRRClient — главный фасад с единой точкой входа
"""

from aio_mrr.client.client import MRRClient

__all__ = ["MRRClient"]

"""Logging module for aio-mrr.

This module provides isolated logging configuration with secret masking.

Exports:
    get_logger: Function to create isolated loggers with secret masking.
    SecretMasker: Class for masking sensitive information in logs.
"""

from .config import get_logger
from .masker import SecretMasker

__all__ = ["SecretMasker", "get_logger"]

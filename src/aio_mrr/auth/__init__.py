"""Authentication module for MRR API.

This module contains components for HMAC authentication:
- NonceGenerator: thread-safe monotonic nonce generator
- AuthSigner: HMAC SHA1 signature generator (implemented in step 4)
"""

from aio_mrr.auth.nonce import NonceGenerator

__all__ = ["NonceGenerator"]

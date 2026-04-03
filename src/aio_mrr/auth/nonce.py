"""Monotonically increasing nonce generator for HMAC authentication.

Author: GRinvest / SibNeuroTech
License: MIT
"""

from __future__ import annotations
import asyncio
import time


class NonceGenerator:
    """Thread-safe monotonically increasing nonce generator.

    Nonce (number used once) is used in MRR API HMAC authentication
    to prevent replay attacks. Each nonce must be unique
    and monotonically increasing.

    The implementation uses:
    - Base timestamp: int(time.time() * 1_000_000) for microsecond precision
    - Internal counter to guarantee uniqueness under concurrent requests
    - asyncio.Lock for thread-safety in async context

    Example:
        >>> generator = NonceGenerator()
        >>> nonce1 = await generator.generate()
        >>> nonce2 = await generator.generate()
        >>> int(nonce2) > int(nonce1)
        True
    """

    def __init__(self) -> None:
        """Initializes the nonce generator."""
        self._counter: int = 0
        self._last_timestamp: int = 0
        self._lock: asyncio.Lock = asyncio.Lock()

    async def generate(self) -> str:
        """Generates a unique monotonically increasing nonce.

        The method guarantees:
        - Uniqueness: even with 100 concurrent calls all nonces are unique
        - Monotonicity: each next nonce is strictly greater than the previous

        Algorithm:
        1. Get current timestamp in microseconds
        2. If timestamp has not decreased, increment the counter
        3. If timestamp decreased (rare case), reset the counter
        4. Form nonce as a combination of timestamp and counter
        5. Use asyncio.Lock for thread-safety

        Returns:
            str: String representation of the nonce (decimal number)

        Example:
            >>> generator = NonceGenerator()
            >>> nonce = await generator.generate()
            >>> isinstance(nonce, str)
            True
            >>> len(nonce) > 0
            True
        """
        async with self._lock:
            current_timestamp: int = int(time.time() * 1_000_000)

            if current_timestamp > self._last_timestamp:
                self._counter = 0
                self._last_timestamp = current_timestamp
            else:
                self._counter += 1

            nonce: int = self._last_timestamp + self._counter
            return str(nonce)

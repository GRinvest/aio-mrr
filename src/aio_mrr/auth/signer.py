"""HMAC SHA1 signature generator for MRR API authentication.

Author: GRinvest / SibNeuroTech
License: MIT
"""

from __future__ import annotations
import hashlib
import hmac

from aio_mrr.auth.nonce import NonceGenerator


class AuthSigner:
    """HMAC SHA1 signature generator for MRR API authentication.

    MRR API uses HMAC SHA1 for request authentication. This class
    generates the necessary headers for signed requests:
    - x-api-key: User's API key
    - x-api-nonce: Unique nonce (number used once)
    - x-api-sign: HMAC SHA1 signature

    The string to sign is formed as: {api_key}{nonce}{endpoint}
    where endpoint is the full path including query string (without trailing slash).

    Example:
        >>> signer = AuthSigner(api_key="test_key", api_secret="test_secret")
        >>> headers = await signer.get_auth_headers("/account/balance")
        >>> "x-api-key" in headers
        True
        >>> "x-api-nonce" in headers
        True
        >>> "x-api-sign" in headers
        True
    """

    def __init__(self, api_key: str, api_secret: str) -> None:
        """Initializes the signature generator.

        Args:
            api_key: API key for MRR API authentication.
            api_secret: API secret for generating HMAC signatures.
        """
        self._api_key: str = api_key
        self._api_secret: str = api_secret
        self._nonce_generator: NonceGenerator = NonceGenerator()

    async def get_auth_headers(self, endpoint: str) -> dict[str, str]:
        """Generates authentication headers for MRR API requests.

        The method creates all necessary headers for a signed request:
        1. Generates a unique nonce via NonceGenerator
        2. Forms the string to sign: {api_key}{nonce}{endpoint}
        3. Computes HMAC SHA1 signature from the string
        4. Returns dict with headers x-api-key, x-api-nonce, x-api-sign

        Args:
            endpoint: Full endpoint path including query string.
                     Examples:
                     - "/account/balance"
                     - "/rig?status=enabled"
                     - "/info/algos?currency=BTC"
                     Important: endpoint should not have a trailing slash.

        Returns:
            dict[str, str]: Dictionary with authentication headers:
                - "x-api-key": API key
                - "x-api-nonce": Generated nonce
                - "x-api-sign": HMAC SHA1 signature (hex string)

        Example:
            >>> signer = AuthSigner("key", "secret")
            >>> headers = await signer.get_auth_headers("/account")
            >>> headers["x-api-key"]
            "key"
            >>> "x-api-sign" in headers
            True
        """
        nonce: str = await self._nonce_generator.generate()

        sign_string: str = f"{self._api_key}{nonce}{endpoint}"

        signature: str = hmac.new(
            self._api_secret.encode(),
            sign_string.encode(),
            hashlib.sha1,
        ).hexdigest()

        return {
            "x-api-key": self._api_key,
            "x-api-nonce": nonce,
            "x-api-sign": signature,
        }

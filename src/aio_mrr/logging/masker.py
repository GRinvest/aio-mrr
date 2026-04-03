"""Masks secrets in text logs.

Uses regular expressions to detect and mask:
- API keys (x-api-key, api_key, apikey)
- API signatures (x-api-sign, api_sign, apisign)
- Nonce (x-api-nonce, api_nonce, apinode)
- HMAC signatures and secrets
"""

from __future__ import annotations
import re
from typing import Final


class SecretMasker:
    """Masks secrets in text logs.

    Uses regular expressions to detect and mask:
    - API keys (x-api-key, api_key, apikey)
    - API signatures (x-api-sign, api_sign, apisign)
    - Nonce (x-api-nonce, api_nonce, apinode)
    - HMAC signatures and secrets
    """

    # Patterns for masking secrets
    SECRET_PATTERNS: Final[list[re.Pattern[str]]] = [
        # API keys: x-api-key: value, api_key=value, "x-api-key": "value" (JSON)
        re.compile(
            r'(?i)["\']?(x-api-key|api_key|apikey|api-key)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)["\']?',
            re.IGNORECASE,
        ),
        # API signatures: x-api-sign: value, api_sign=value, "x-api-sign": "value" (JSON)
        re.compile(
            r'(?i)["\']?(x-api-sign|api_sign|apisign|api-sign)["\']?\s*[:=]\s*["\']?([a-fA-F0-9]+)["\']?',
            re.IGNORECASE,
        ),
        # Nonce: x-api-nonce: value, api_nonce=value, "x-api-nonce": "value" (JSON)
        re.compile(
            r'(?i)["\']?(x-api-nonce|api_nonce|apinode|api-nonce)["\']?\s*[:=]\s*["\']?(\d+)["\']?',
            re.IGNORECASE,
        ),
        # HMAC signatures (64 hex characters - SHA256)
        re.compile(r"\b([a-fA-F0-9]{64})\b"),
        # HMAC signatures (40 hex characters - SHA1)
        re.compile(r"\b([a-fA-F0-9]{40})\b"),
        # Secrets in format "secret": "value"
        re.compile(
            r'(?i)["\']?(secret|api_secret|apisecret)["\']?\s*[:=]\s*["\']?([^,"\']+)["\']?',
            re.IGNORECASE,
        ),
    ]

    # Replacement for masking
    MASK_REPLACEMENT: Final[str] = "***"

    def mask(self, text: str) -> str:
        """Masks secrets in text.

        Args:
            text: Text to mask.

        Returns:
            Text with masked secrets.

        Examples:
            >>> masker = SecretMasker()
            >>> masker.mask("x-api-key: abc123")
            'x-api-key: ***'
            >>> masker.mask("x-api-sign: def456")
            'x-api-sign: ***'
            >>> masker.mask("api_key=mykey&api_secret=myservice")
            'api_key=***&api_secret=***'
        """
        masked_text = text

        for pattern in self.SECRET_PATTERNS:
            masked_text = pattern.sub(self._replace_match, masked_text)

        return masked_text

    def _replace_match(self, match: re.Match[str]) -> str:
        """Replaces a match with a masked value.

        Args:
            match: Regular expression match object.

        Returns:
            Masked string with preserved structure.
        """
        # Check if there is a secret value in the match (group 2 or 3)
        if match.lastindex and match.lastindex >= 2:
            # Preserve key/name and separator, replace value
            key_part = match.group(1) if match.group(1) else ""
            # Find separator ( : or = ) in the original match
            full_match = match.group(0)
            sep_match = re.search(r"[:=]\s*", full_match)
            if sep_match:
                separator = sep_match.group(0)
                return f"{key_part}{separator}{self.MASK_REPLACEMENT}"
            return f"{key_part}{self.MASK_REPLACEMENT}"

        # For simple hex patterns, replace the entire match
        return self.MASK_REPLACEMENT

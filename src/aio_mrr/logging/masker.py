"""Secret masking module for loguru.

This module provides the SecretMasker class for masking sensitive information
in log messages, such as API keys, signatures, and nonces.
"""

from __future__ import annotations
import re
from typing import Final


class SecretMasker:
    """Маскирует секреты в текстовых логах.

    Использует регулярные выражения для обнаружения и маскирования:
    - API-ключей (x-api-key, api_key, apikey)
    - API-подписей (x-api-sign, api_sign, apisign)
    - Nonce (x-api-nonce, api_nonce, apinode)
    - HMAC-подписей и секретов
    """

    # Паттерны для маскирования секретов
    SECRET_PATTERNS: Final[list[re.Pattern[str]]] = [
        # API ключи: x-api-key: value, api_key=value, "x-api-key": "value" (JSON)
        re.compile(
            r'(?i)["\']?(x-api-key|api_key|apikey|api-key)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)["\']?',
            re.IGNORECASE,
        ),
        # API подписи: x-api-sign: value, api_sign=value, "x-api-sign": "value" (JSON)
        re.compile(
            r'(?i)["\']?(x-api-sign|api_sign|apisign|api-sign)["\']?\s*[:=]\s*["\']?([a-fA-F0-9]+)["\']?',
            re.IGNORECASE,
        ),
        # Nonce: x-api-nonce: value, api_nonce=value, "x-api-nonce": "value" (JSON)
        re.compile(
            r'(?i)["\']?(x-api-nonce|api_nonce|apinode|api-nonce)["\']?\s*[:=]\s*["\']?(\d+)["\']?',
            re.IGNORECASE,
        ),
        # HMAC подписи (64 hex символов - SHA256)
        re.compile(r"\b([a-fA-F0-9]{64})\b"),
        # HMAC подписи (40 hex символов - SHA1)
        re.compile(r"\b([a-fA-F0-9]{40})\b"),
        # Секреты в формате "secret": "value"
        re.compile(
            r'(?i)["\']?(secret|api_secret|apisecret)["\']?\s*[:=]\s*["\']?([^,"\']+)["\']?',
            re.IGNORECASE,
        ),
    ]

    # Замена для маскирования
    MASK_REPLACEMENT: Final[str] = "***"

    def mask(self, text: str) -> str:
        """Маскирует секреты в тексте.

        Args:
            text: Текст для маскирования.

        Returns:
            Текст с замаскированными секретами.

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
        """Заменяет совпадение на маскированное значение.

        Args:
            match: Объект совпадения регулярного выражения.

        Returns:
            Замаскированная строка с сохранением структуры.
        """
        # Проверяем, есть ли в совпадении секретное значение (группа 2 или 3)
        if match.lastindex and match.lastindex >= 2:
            # Сохраняем ключ/название и разделитель, заменяем значение
            key_part = match.group(1) if match.group(1) else ""
            # Находим разделитель ( : или = ) в оригинальном совпадении
            full_match = match.group(0)
            sep_match = re.search(r"[:=]\s*", full_match)
            if sep_match:
                separator = sep_match.group(0)
                return f"{key_part}{separator}{self.MASK_REPLACEMENT}"
            return f"{key_part}{self.MASK_REPLACEMENT}"

        # Для простых hex-паттернов заменяем всё совпадение
        return self.MASK_REPLACEMENT

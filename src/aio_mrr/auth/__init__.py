"""Модуль аутентификации для MRR API.

Этот модуль содержит компоненты для HMAC-аутентификации:
- NonceGenerator: thread-safe генератор монотонных nonce
- AuthSigner: генератор HMAC SHA1 подписей (реализуется в шаге 4)
"""

from aio_mrr.auth.nonce import NonceGenerator

__all__ = ["NonceGenerator"]

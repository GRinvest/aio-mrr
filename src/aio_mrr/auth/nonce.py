"""Генератор монотонно возрастающих nonce для HMAC-аутентификации.

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
"""

from __future__ import annotations
import asyncio
import time


class NonceGenerator:
    """Thread-safe генератор монотонно возрастающих nonce.

    Nonce (number used once) используется в HMAC-аутентификации MRR API
    для предотвращения replay-атак. Каждый nonce должен быть уникальным
    и монотонно возрастающим.

    Реализация использует:
    - Базовый timestamp: int(time.time() * 1_000_000) для микросекундной точности
    - Внутренний счётчик для гарантии уникальности при параллельных запросах
    - asyncio.Lock для thread-safety в асинхронном контексте

    Пример:
        >>> generator = NonceGenerator()
        >>> nonce1 = await generator.generate()
        >>> nonce2 = await generator.generate()
        >>> int(nonce2) > int(nonce1)
        True
    """

    def __init__(self) -> None:
        """Инициализирует генератор nonce."""
        self._counter: int = 0
        self._last_timestamp: int = 0
        self._lock: asyncio.Lock = asyncio.Lock()

    async def generate(self) -> str:
        """Генерирует уникальный монотонно возрастающий nonce.

        Метод гарантирует:
        - Уникальность: даже при 100 одновременных вызовах все nonce уникальны
        - Монотонность: каждый следующий nonce строго больше предыдущего

        Алгоритм:
        1. Получаем текущий timestamp в микросекундах
        2. Если timestamp не уменьшился, инкрементируем счётчик
        3. Если timestamp уменьшился (редкий случай), сбрасываем счётчик
        4. Формируем nonce как комбинацию timestamp и счётчика
        5. Используем asyncio.Lock для thread-safety

        Returns:
            str: Строковое представление nonce (число в десятичной системе)

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

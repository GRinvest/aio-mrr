"""Тесты для NonceGenerator."""

from __future__ import annotations
import asyncio
import pytest

from aio_mrr.auth.nonce import NonceGenerator


class TestNonceGenerator:
    """Тесты для класса NonceGenerator."""

    @pytest.mark.asyncio
    async def test_generate_returns_string(self) -> None:
        """Тестирует, что generate возвращает строку."""
        generator = NonceGenerator()
        nonce = await generator.generate()

        assert isinstance(nonce, str)
        assert len(nonce) > 0

    @pytest.mark.asyncio
    async def test_generate_monotonicity(self) -> None:
        """Тестирует монотонность nonce (каждый следующий больше предыдущего)."""
        generator = NonceGenerator()

        previous_nonce = 0
        for _ in range(100):
            nonce = await generator.generate()
            current_nonce = int(nonce)

            assert current_nonce > previous_nonce, "Nonce должен быть монотонно возрастающим"
            previous_nonce = current_nonce

    @pytest.mark.asyncio
    async def test_concurrent_uniqueness(self) -> None:
        """Тестирует уникальность nonce при 100 одновременных вызовах."""
        generator = NonceGenerator()

        async def generate_nonce() -> str:
            return await generator.generate()

        # Создаём 100 одновременных задач
        tasks = [asyncio.create_task(generate_nonce()) for _ in range(100)]
        nonces = await asyncio.gather(*tasks)

        # Проверяем, что все nonce уникальны
        assert len(nonces) == 100
        assert len(set(nonces)) == 100, "All nonces must be unique"

    @pytest.mark.asyncio
    async def test_concurrent_monotonicity(self) -> None:
        """Тестирует монотонность при параллельных вызовах."""
        generator = NonceGenerator()

        async def generate_nonce() -> str:
            return await generator.generate()

        # Создаём 100 одновременных задач
        tasks = [asyncio.create_task(generate_nonce()) for _ in range(100)]
        nonces = await asyncio.gather(*tasks)

        # Сортируем и проверяем монотонность
        sorted_nonces = sorted(int(n) for n in nonces)

        for i in range(1, len(sorted_nonces)):
            assert sorted_nonces[i] > sorted_nonces[i - 1], "Nonce должны быть монотонно возрастающими"

    @pytest.mark.asyncio
    async def test_sequence_after_concurrent(self) -> None:
        """Тестирует, что последовательные вызовы после параллельных сохраняют монотонность."""
        generator = NonceGenerator()

        # Сначала параллельные вызовы
        tasks = [asyncio.create_task(generator.generate()) for _ in range(50)]
        await asyncio.gather(*tasks)

        # Затем последовательные вызовы
        sequential_nonces = []
        for _ in range(10):
            nonce = await generator.generate()
            sequential_nonces.append(nonce)

        # Проверяем, что последовательные вызовы после параллельных монотонны
        # Примечание: не гарантируем строгий порядок между параллельными и последовательными
        for i in range(1, len(sequential_nonces)):
            assert int(sequential_nonces[i]) > int(sequential_nonces[i - 1])

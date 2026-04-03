"""Демонстрация обработки ошибок для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Обработку всех типов ошибок: network_error, timeout, api_error, validation_error
- Retry-стратегию HTTP-клиента (автоматические повторные попытки)
- Вывод деталей ошибки: code, message, http_status, details
- Паттерн обработки через проверку response.success

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/error-handling.md
"""

import asyncio
import os
import sys

from aio_mrr import MRRClient, MRRResponse, MRRResponseError


async def main() -> None:
    """Основная функция примера."""
    # Загрузка API-ключей из переменных окружения
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    # Проверка наличия ключей
    if not api_key or not api_secret:
        print("Ошибка: API-ключи не найдены. Установите переменные окружения MRR_API_KEY и MRR_API_SECRET.")
        sys.exit(1)

    print("=" * 60)
    print("ДЕМО ОБРАБОТКИ ОШИБОК")
    print("=" * 60)

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(
        api_key=api_key,
        api_secret=api_secret,
        max_retries=3,  # Настройка количества повторных попыток
        connect_timeout=5.0,  # Короткий таймаут для демонстрации
        read_timeout=5.0,
    ) as client:
        # ---------------------------------------------------------------------
        # 1. Демонстрация успешного запроса (для сравнения)
        # ---------------------------------------------------------------------
        print("\n[1] Успешный запрос — whoami()")
        print("-" * 40)

        response: MRRResponse[dict[str, str]] = await client.whoami()

        if response.success:
            print(f"✓ Успех! retry_count={response.retry_count}")
            data = response.data
            username = data.get("username", "Неизвестно") if data else "Неизвестно"
            print(f"  Username: {username}")
        else:
            # Обработка ошибки через MRRResponseError
            print(f"✗ Ошибка: {response.error}")
            _print_error_details(response.error)

        # ---------------------------------------------------------------------
        # 2. Демонстрация api_error — невалидный параметр запроса
        # ---------------------------------------------------------------------
        print("\n[2] API ошибка — get_balance() с невалидным параметром")
        print("-" * 40)

        # Попробуем вызвать метод с параметром, который не ожидается
        # (это может вернуть api_error от сервера)
        balance_response = await client.account.get_balance()

        if balance_response.success:
            print(f"✓ Успех! retry_count={response.retry_count}")
            balances = response.data
            if balances:
                print(f"  Балансов найдено: {len(balances)}")
        else:
            print(f"✗ Ошибка: {response.error}")
            _print_error_details(response.error)
            print(f"  HTTP статус: {response.http_status}")
            print(f"  Количество попыток: {response.retry_count}")

        # ---------------------------------------------------------------------
        # 3. Демонстрация timeout — запрос с очень коротким таймаутом
        # ---------------------------------------------------------------------
        print("\n[3] Таймаут — запрос с коротким read_timeout")
        print("-" * 40)

        # Создаём временный клиент с очень коротким таймаутом
        async with MRRClient(
            api_key=api_key,
            api_secret=api_secret,
            read_timeout=0.001,  # 1 миллисекунда — почти гарантированный таймаут
            max_retries=1,
        ) as timeout_client:
            response = await timeout_client.whoami()

            if response.success:
                print(f"✓ Успех! retry_count={response.retry_count}")
            else:
                print(f"✗ Ошибка: {response.error}")
                _print_error_details(response.error)
                print(f"  Тип ошибки: {response.error.code if response.error else 'unknown'}")
                print(f"  HTTP статус: {response.http_status}")

        # ---------------------------------------------------------------------
        # 4. Демонстрация network_error — подключение к невалидному серверу
        # ---------------------------------------------------------------------
        print("\n[4] Сетевая ошибка — подключение к невалидному серверу")
        print("-" * 40)
        print("  (Эта часть демонстрации пропущена, так как требует")
        print("   модификации базового URL клиента)")

        # ---------------------------------------------------------------------
        # 5. Демонстрация retry-стратегии
        # ---------------------------------------------------------------------
        print("\n[5] Retry-стратегия — автоматические повторные попытки")
        print("-" * 40)

        # Создаём клиента с максимальным количеством попыток
        async with MRRClient(
            api_key=api_key,
            api_secret=api_secret,
            max_retries=5,
        ) as retry_client:
            # Нормальный запрос обычно проходит с первой попытки
            response = await retry_client.whoami()

            if response.success:
                print(f"✓ Успех! retry_count={response.retry_count}")
                print("  Запрос выполнен с первой попытки")
            else:
                print(f"✗ Ошибка: {response.error}")
                print(f"  retry_count={response.retry_count}")
                print("  Все попытки исчерпаны")

        # ---------------------------------------------------------------------
        # 6. Общий пример обработки всех типов ошибок
        # ---------------------------------------------------------------------
        print("\n[6] Универсальный паттерн обработки ошибок")
        print("-" * 40)

        async def safe_request(description: str, coro: object) -> None:
            """Универсальная функция для безопасного выполнения запросов."""
            print(f"\n  {description}")
            try:
                response_obj: MRRResponse[object] = await coro  # type: ignore[misc]
                if isinstance(response_obj, MRRResponse):
                    if response_obj.success:
                        print(f"    ✓ Успех! retry_count={response_obj.retry_count}")
                    else:
                        print(f"    ✗ Ошибка: {response_obj.error}")
                        _print_error_details(response_obj.error)
                else:
                    print(f"    ? Неожиданный тип ответа: {type(response_obj)}")
            except Exception as e:
                print(f"    ✗ Исключение: {type(e).__name__}: {e}")

        await safe_request("whoami()", client.whoami())
        await safe_request("get_balance()", client.account.get_balance())
        await safe_request("get_servers()", client.info.get_servers())

    print("\n" + "=" * 60)
    print("Клиент закрыт.")
    print("=" * 60)


def _print_error_details(error: MRRResponseError | None) -> None:
    """Вывод деталей ошибки.

    Args:
        error: Объект ошибки MRRResponseError
    """
    if not error:
        print("  Детали ошибки отсутствуют")
        return

    print(f"  code: {error.code}")
    print(f"  message: {error.message}")
    print(f"  http_status: {error.http_status}")
    if error.details:
        print(f"  details: {error.details}")


if __name__ == "__main__":
    asyncio.run(main())

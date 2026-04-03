"""Пример быстрого старта для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Загрузку API-ключей из переменных окружения
- Инициализацию клиента через контекстный менеджер
- Проверку аутентификации через whoami()
- Получение баланса аккаунта

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/authentication.md, docs/error-handling.md
"""

import asyncio
import os
import sys

from aio_mrr import MRRClient, MRRResponse


async def main() -> None:
    """Основная функция примера."""
    # Загрузка API-ключей из переменных окружения
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    # Проверка наличия ключей
    if not api_key or not api_secret:
        print("Ошибка: API-ключи не найдены. Установите переменные окружения MRR_API_KEY и MRR_API_SECRET.")
        sys.exit(1)

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # Проверка аутентификации
        print("Проверка аутентификации...")
        response: MRRResponse[dict[str, str]] = await client.whoami()

        if not response.success:
            print(f"Ошибка: {response.error}")
            return

        # Вывод информации об аккаунте
        data = response.data
        username = data.get("username", "Неизвестно") if data else "Неизвестно"
        print(f"Успешно аутентифицирован как: {username}")

        # Получение баланса аккаунта
        print("\nПолучение баланса...")
        balance_response = await client.account.get_balance()

        if not balance_response.success:
            print(f"Ошибка: {balance_response.error}")
            return

        # Вывод баланса по валютам
        balances = balance_response.data
        if balances:
            print("\nБалансы по валютам:")
            for currency, balance_info in balances.items():
                confirmed = balance_info.confirmed
                pending = balance_info.pending
                unconfirmed = balance_info.unconfirmed
                print(f"  {currency}: подтверждённый={confirmed}, ожидающий={pending}, неподтверждённый={unconfirmed}")
        else:
            print("Баланс отсутствует")

    print("\nКлиент закрыт.")


if __name__ == "__main__":
    asyncio.run(main())

"""Пример работы с аккаунтом для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Загрузку API-ключей из переменных окружения
- Инициализацию клиента через контекстный менеджер
- Получение информации об аккаунте (профиль, настройки)
- Получение баланса по валютам (подтверждённый, ожидающий, неподтверждённый)
- Получение истории транзакций
- Получение статусов валют

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/account.md
"""

import asyncio
import os
import sys

from aio_mrr import (
    AccountInfo,
    BalanceInfo,
    CurrencyStatus,
    MRRClient,
    MRRResponse,
    TransactionsList,
)


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
        # Получение информации об аккаунте
        print("Получение информации об аккаунте...")
        account_response: MRRResponse[AccountInfo] = await client.account.get_account()

        if not account_response.success:
            print(f"Ошибка: {account_response.error}")
            return

        # Вывод информации об аккаунте
        account_info = account_response.data
        print(f"  Username: {account_info.username}")
        print(f"  Email: {account_info.email}")
        print("  Настройки:")
        print(f"    - Режим живых данных: {account_info.settings.live_data}")
        print(f"    - Публичный профиль: {account_info.settings.public_profile}")
        print(f"    - Двухфакторная аутентификация: {account_info.settings.two_factor_auth}")
        print("  Уведомления:")
        print(f"    - О комментариях аренды: {account_info.notifications.rental_comm}")
        print(f"    - О новых арендах: {account_info.notifications.new_rental}")
        print(f"    - Об оффлайне: {account_info.notifications.offline}")
        print(f"    - О новостях: {account_info.notifications.news}")
        print(f"    - О депозитах: {account_info.notifications.deposit}")

        # Получение баланса аккаунта
        print("\nПолучение баланса...")
        balance_response: MRRResponse[dict[str, BalanceInfo]] = await client.account.get_balance()

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

        # Получение истории транзакций
        print("\nПолучение истории транзакций...")
        transactions_response: MRRResponse[TransactionsList] = await client.account.get_transactions()

        if not transactions_response.success:
            print(f"Ошибка: {transactions_response.error}")
            return

        # Вывод последних транзакций
        transactions_list = transactions_response.data
        print(f"Всего транзакций: {transactions_list.total}, возвращено: {transactions_list.returned}")
        if transactions_list.transactions:
            print("\nПоследние транзакции:")
            for tx in transactions_list.transactions[:10]:  # Отображаем максимум 10
                print(f"  ID: {tx.id}")
                print(f"    Тип: {tx.type}")
                print(f"    Валюта: {tx.currency or 'N/A'}")
                print(f"    Сумма: {tx.amount}")
                print(f"    Дата: {tx.when}")
                print(f"    Статус: {tx.status}")
                print(f"    Риг: {tx.rig or 'N/A'}")
                print(f"    Аренда: {tx.rental or 'N/A'}")
                print()
        else:
            print("Транзакции отсутствуют")

        # Получение статусов валют
        print("\nПолучение статусов валют...")
        currencies_response: MRRResponse[list[CurrencyStatus]] = await client.account.get_currencies()

        if not currencies_response.success:
            print(f"Ошибка: {currencies_response.error}")
            return

        # Вывод статусов валют
        currencies = currencies_response.data
        if currencies:
            print("\nСтатусы валют:")
            for currency in currencies:
                status = "включена" if currency.enabled else "отключена"
                print(f"  {currency.name}: {status}")
        else:
            print("Валюты отсутствуют")

    print("\nКлиент закрыт.")


if __name__ == "__main__":
    asyncio.run(main())

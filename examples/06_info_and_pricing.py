"""Пример получения информации о серверах, алгоритмах и ценах для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Загрузку API-ключей из переменных окружения
- Инициализацию клиента через контекстный менеджер
- Получение списка серверов MRR через get_servers()
- Получение всех алгоритмов майнинга через get_algos()
- Получение информации о конкретном алгоритме через get_algo()
- Получение доступных валют оплаты через get_currencies()
- Получение курсов конвертации и рыночных цен через get_pricing()

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/info.md, docs/api-reference/pricing.md
"""

import asyncio
import os
import sys

from aio_mrr import (
    AlgoInfo,
    CurrencyInfo,
    MRRClient,
    MRRResponse,
    PricingInfo,
    ServersList,
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
        # Получение списка серверов MRR
        print("Получение списка серверов...")
        servers_response: MRRResponse[ServersList] = await client.info.get_servers()

        if not servers_response.success:
            print(f"Ошибка: {servers_response.error}")
            return

        # Вывод информации о серверах
        servers_list = servers_response.data
        if servers_list and servers_list.servers:
            print("\nСерверы MRR:")
            for server in servers_list.servers:
                print(f"  ID: {server.id}")
                print(f"    Название: {server.name}")
                print(f"    Регион: {server.region}")
                port = server.port or "N/A"
                ethereum_port = server.ethereum_port or "N/A"
                print(f"    Порт: {port}")
                print(f"    Порт Ethereum: {ethereum_port}")
                print()
        else:
            print("Серверы отсутствуют")

        # Получение всех алгоритмов майнинга
        print("Получение всех алгоритмов майнинга...")
        algos_response: MRRResponse[list[AlgoInfo]] = await client.info.get_algos()

        if not algos_response.success:
            print(f"Ошибка: {algos_response.error}")
            return

        # Вывод информации об алгоритмах
        algos = algos_response.data
        if algos:
            print(f"\nВсего алгоритмов: {len(algos)}")
            print("\nАлгоритмы майнинга:")
            for algo in algos[:10]:  # Отображаем первые 10 алгоритмов
                print(f"  Название: {algo.name}")
                print(f"    Отображаемое имя: {algo.display}")
                suggested_price = algo.suggested_price
                price_amount = suggested_price.amount
                price_currency = suggested_price.currency
                price_unit = suggested_price.unit
                print(f"    Рекомендуемая цена: {price_amount} {price_currency} за {price_unit}")
                stats = algo.stats
                print(f"    Доступно: {stats.available.hash.nice} ({stats.available.rigs} ригов)")
                print(f"    Арендовано: {stats.rented.hash.nice} ({stats.rented.rigs} ригов)")
                lowest_price = stats.prices.lowest.amount
                last_price = stats.prices.last.amount
                print(f"    Цены: мин={lowest_price}, последняя={last_price}")
                print()
        else:
            print("Алгоритмы отсутствуют")

        # Получение информации о конкретном алгоритме (kawpow)
        print("Получение информации об алгоритме kawpow...")
        kawpow_response: MRRResponse[AlgoInfo] = await client.info.get_algo(name="kawpow")

        if not kawpow_response.success:
            print(f"Ошибка: {kawpow_response.error}")
            return

        # Вывод информации об алгоритме kawpow
        kawpow_algo = kawpow_response.data
        if kawpow_algo:
            print("\nИнформация об алгоритме:")
            print(f"  Название: {kawpow_algo.name}")
            print(f"  Отображаемое имя: {kawpow_algo.display}")
            suggested_price = kawpow_algo.suggested_price
            price_amount = suggested_price.amount
            price_currency = suggested_price.currency
            price_unit = suggested_price.unit
            print(f"  Рекомендуемая цена: {price_amount} {price_currency} за {price_unit}")
            stats = kawpow_algo.stats
            print(f"  Доступно: {stats.available.hash.nice} ({stats.available.rigs} ригов)")
            print(f"  Арендовано: {stats.rented.hash.nice} ({stats.rented.rigs} ригов)")
            print("  Цены:")
            lowest_amount = stats.prices.lowest.amount
            lowest_currency = stats.prices.lowest.currency
            print(f"    мин: {lowest_amount} {lowest_currency}")
            last_10_amount = stats.prices.last_10.amount
            last_10_currency = stats.prices.last_10.currency
            print(f"    Последние 10: {last_10_amount} {last_10_currency}")
            last_amount = stats.prices.last.amount
            last_currency = stats.prices.last.currency
            print(f"    Последняя: {last_amount} {last_currency}")
        else:
            print("Информация об алгоритме отсутствует")

        # Получение доступных валют оплаты
        print("\nПолучение доступных валют оплаты...")
        currencies_response: MRRResponse[list[CurrencyInfo]] = await client.info.get_currencies()

        if not currencies_response.success:
            print(f"Ошибка: {currencies_response.error}")
            return

        # Вывод информации о валютах
        currencies = currencies_response.data
        if currencies:
            print("\nДоступные валюты:")
            for currency in currencies:
                status = "включена" if currency.enabled else "отключена"
                print(f"  {currency.name}: {status}, комиссия: {currency.txfee}")
        else:
            print("Валюты отсутствуют")

        # Получение курсов конвертации и рыночных цен
        print("\nПолучение курсов конвертации и рыночных цен...")
        pricing_response: MRRResponse[PricingInfo] = await client.pricing.get_pricing()

        if not pricing_response.success:
            print(f"Ошибка: {pricing_response.error}")
            return

        # Вывод информации о ценах
        pricing_info = pricing_response.data
        if pricing_info:
            print("\nКурсы конвертации:")
            conversion_rates = pricing_info.conversion_rates
            print(f"  LTC: {conversion_rates.LTC}")
            print(f"  ETH: {conversion_rates.ETH}")
            print(f"  BCH: {conversion_rates.BCH}")
            print(f"  DOGE: {conversion_rates.DOGE}")

            print("\nРыночные цены по алгоритмам:")
            market_rates = pricing_info.market_rates
            # Отображаем цены для нескольких популярных алгоритмов
            algo_names = ["kawpow", "ethash", "autolykosv2", "scrypt", "sha256"]
            for algo_name in algo_names:
                if hasattr(market_rates, algo_name):
                    algo_rates = getattr(market_rates, algo_name)
                    print(f"  {algo_name}:")
                    print(f"    BTC: {algo_rates.BTC}")
                    print(f"    LTC: {algo_rates.LTC}")
                    print(f"    ETH: {algo_rates.ETH}")
                    print(f"    BCH: {algo_rates.BCH}")
                    print(f"    DOGE: {algo_rates.DOGE}")
        else:
            print("Информация о ценах отсутствует")

    print("\nКлиент закрыт.")


if __name__ == "__main__":
    asyncio.run(main())

"""Пример расширенного поиска ригов для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Поиск ригов с множеством фильтров через search_rigs()
- Получение графика хешрейта ригов через get_rig_graph()
- Получение активных тредов ригов через get_rig_threads()
- Получение информации о портах ригов через get_rig_ports()

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/rigs.md
"""

import asyncio
import os
import sys

from aio_mrr import (
    MRRClient,
    MRRResponse,
    RigGraphData,
    RigInfo,
    RigPortInfo,
    RigThreadInfo,
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

    # Получение ID ригов для дальнейших запросов (из переменных окружения или заглушки)
    rig_ids_str = os.environ.get("MRR_RIG_IDS", "12345,12346")
    rig_ids = [int(rig_id.strip()) for rig_id in rig_ids_str.split(",") if rig_id.strip()]

    print("=" * 60)
    print("ПРИМЕР РАСШИРЕННОГО ПОИСКА РИГОВ")
    print("=" * 60)

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # ---------------------------------------------------------------------
        # 1. Поиск ригов с фильтрами через search_rigs()
        # ---------------------------------------------------------------------
        print("\n[1] Поиск ригов с фильтрами (kawpow)")
        print("-" * 40)

        # Поиск с множеством фильтров (минимум 5):
        # - type: алгоритм майнинга
        # - hash_min: минимальный хешрейт
        # - price_max: максимальная цена
        # - minhours_min: минимальное минимальное время аренды
        # - maxhours_max: максимальное максимальное время аренды
        # - online: только онлайн риги
        # - rented: только доступные для аренды
        search_response: MRRResponse[list[RigInfo]] = await client.rig.search_rigs(
            type="kawpow",  # Фильтр 1: алгоритм
            hash_min=50,  # Фильтр 2: минимальный хешрейт (MH/s)
            price_max=0.01,  # Фильтр 3: максимальная цена (BTC/час)
            minhours_min=1,  # Фильтр 4: минимальное minHours >= 1
            maxhours_max=48,  # Фильтр 5: максимальное maxHours <= 48
            offline=False,  # Фильтр 6: только онлайн риги
            rented=False,  # Фильтр 7: только доступные (не арендованные)
            count=10,  # Лимит результатов
        )

        if not search_response.success:
            print(f"Ошибка при поиске ригов: {search_response.error}")
            return

        search_results = search_response.data
        if search_results:
            print(f"Найдено ригов: {len(search_results)}")
            for i, rig in enumerate(search_results[:5], 1):  # Показываем первые 5
                print(f"\n  [{i}] Риг ID: {rig.id}")
                print(f"      Название: {rig.name}")
                print(f"      Статус: {rig.status}")
                print(f"      Сервер: {rig.server}")
                if rig.hash:
                    hash_value = rig.hash.hash
                    hash_type = rig.hash.type
                    print(f"      Хешрейт: {hash_value} {hash_type}")
                if rig.price:
                    for currency, price_info in rig.price.items():
                        if price_info.price:
                            print(f"      Цена ({currency}): {price_info.price} BTC/час")
                print(f"      Онлайн: {rig.online}, Арендован: {rig.rented}")
        else:
            print("Риги не найдены")

        # ---------------------------------------------------------------------
        # 2. Получение графика хешрейта через get_rig_graph()
        # ---------------------------------------------------------------------
        print("\n[2] Получение графика хешрейта")
        print("-" * 40)

        if rig_ids:
            graph_response: MRRResponse[RigGraphData] = await client.rig.get_rig_graph(
                ids=rig_ids,
                hours=24.0,  # График за последние 24 часа
                deflate=False,
            )

            if not graph_response.success:
                print(f"Ошибка при получении графика: {graph_response.error}")
            else:
                graph_data = graph_response.data
                if graph_data:
                    rigid = graph_data.rigid or "не указано"
                    print(f"График для rig: {rigid}")
                    if graph_data.chartdata:
                        chartdata = graph_data.chartdata
                        time_start = chartdata.get("time_start", "не указано")
                        time_end = chartdata.get("time_end", "не указано")
                        bars = chartdata.get("bars", "")
                        print(f"  Начало: {time_start}")
                        print(f"  Конец: {time_end}")
                        # bars — это строка с данными в формате "[ts,val],[ts,val],..."
                        bar_count = bars.count("],[") + 1 if bars else 0
                        print(f"  Точек данных: {bar_count}")
        else:
            print("Пропуск получения графика (нет ID ригов)")

        # ---------------------------------------------------------------------
        # 3. Получение активных тредов через get_rig_threads()
        # ---------------------------------------------------------------------
        print("\n[3] Получение активных тредов ригов")
        print("-" * 40)

        if rig_ids:
            threads_response: MRRResponse[list[RigThreadInfo]] = await client.rig.get_rig_threads(
                ids=rig_ids,
            )

            if not threads_response.success:
                print(f"Ошибка при получении тредов: {threads_response.error}")
            else:
                threads = threads_response.data
                if threads:
                    print(f"Групп ригов с тредами: {len(threads)}")
                    for thread_group in threads[:5]:  # Показываем первые 5
                        print(f"\n  Риг ID: {thread_group.rigid}")
                        print(f"    Доступ: {thread_group.access}")
                        print(f"    Тредов: {len(thread_group.threads)}")
                        for detail in thread_group.threads[:3]:  # Первые 3 треда
                            print(f"      Worker: {detail.worker or 'N/A'}, Статус: {detail.status or 'N/A'}")
                            if detail.hashrate:
                                print(f"      Хешрейт: {detail.hashrate}")
                else:
                    print("Активные треды отсутствуют")
        else:
            print("Пропуск получения тредов (нет ID ригов)")

        # ---------------------------------------------------------------------
        # 4. Получение информации о портах через get_rig_ports()
        # ---------------------------------------------------------------------
        print("\n[4] Получение информации о портах ригов")
        print("-" * 40)

        if rig_ids:
            ports_response: MRRResponse[RigPortInfo] = await client.rig.get_rig_ports(
                ids=rig_ids,
            )

            if not ports_response.success:
                print(f"Ошибка при получении информации о портах: {ports_response.error}")
            else:
                port_info = ports_response.data
                if port_info:
                    print(f"Риг ID: {port_info.rigid or 'N/A'}")
                    print(f"Порт сервера: {port_info.port}")
                    print(f"Сервер: {port_info.server or 'N/A'}")
                    print(f"Worker: {port_info.worker or 'N/A'}")
                    print("Используйте этот порт для подключения стратума")
        else:
            print("Пропуск получения информации о портах (нет ID ригов)")

        # ---------------------------------------------------------------------
        # 5. Поиск с дополнительными фильтрами
        # ---------------------------------------------------------------------
        print("\n[5] Поиск с дополнительными фильтрами (scrypt)")
        print("-" * 40)

        search_response_2: MRRResponse[list[RigInfo]] = await client.rig.search_rigs(
            type="scrypt",  # Алгоритм
            price_min=0.001,  # Минимальная цена
            price_max=0.005,  # Максимальная цена
            rpi_min=2,  # Минимальный RPI (соотношение цены к хешрейту)
            rpi_max=10,  # Максимальный RPI
            hash_type="scrypt",  # Тип хешрейта
            region_type="EU",  # Регион
            expdiff=1.0,  # Ожидаемая сложность
        )

        if not search_response_2.success:
            print(f"Ошибка при поиске: {search_response_2.error}")
        else:
            results_2 = search_response_2.data
            print(f"Найдено ригов (scrypt): {len(results_2) if results_2 else 0}")
            if results_2:
                for rig in results_2[:3]:
                    print(f"  ID: {rig.id}, Название: {rig.name}, Цена: {rig.price_type}")

    print("\n" + "=" * 60)
    print("Клиент закрыт.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

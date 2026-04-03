"""Пример управления пулами для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Получение всех сохранённых пулов через get_pools()
- Создание нового пула через create_pool()
- Получение пулов по ID через get_pools_by_ids()
- Тестирование подключения к пулу через test_pool()
- Обновление пулов через update_pools()
- Удаление пулов через delete_pools()

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/account.md
"""

import asyncio
import os
import sys

from aio_mrr import (
    MRRClient,
    MRRResponse,
    Pool,
    PoolCreateBody,
    PoolCreateResponse,
    PoolTestBody,
    PoolTestResult,
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

    # Получение данных пула из переменных окружения
    pool_type = os.environ.get("MRR_POOL_TYPE", "stratum+tcp")
    pool_name = os.environ.get("MRR_POOL_NAME", "Example Pool")
    pool_host = os.environ.get("MRR_POOL_HOST", "pool.example.com")
    pool_port = int(os.environ.get("MRR_POOL_PORT", "3333"))
    pool_user = os.environ.get("MRR_POOL_USER", "worker1")
    pool_pass = os.environ.get("MRR_POOL_PASS", "x")
    pool_notes = os.environ.get("MRR_POOL_NOTES", "Example pool for demonstration")

    print("=" * 60)
    print("ПРИМЕР УПРАВЛЕНИЯ ПУЛАМИ")
    print("=" * 60)

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # ---------------------------------------------------------------------
        # 1. Получение всех сохранённых пулов через get_pools()
        # ---------------------------------------------------------------------
        print("\n[1] Получение всех сохранённых пулов")
        print("-" * 40)

        get_pools_response: MRRResponse[list[Pool]] = await client.account.get_pools()

        if not get_pools_response.success:
            print(f"Ошибка при получении пулов: {get_pools_response.error}")
            return

        pools = get_pools_response.data
        if pools:
            print(f"Найдено пулов: {len(pools)}")
            for pool in pools:
                print(f"\n  ID: {pool.id}")
                print(f"    Название: {pool.name}")
                print(f"    Тип: {pool.type}")
                print(f"    Хост: {pool.host}:{pool.port}")
                print(f"    User: {pool.user}")
                if pool.notes:
                    print(f"    Заметки: {pool.notes}")
                if pool.algo:
                    print(f"    Алгоритм: {pool.algo.name}")
        else:
            print("Сохранённые пулы отсутствуют")

        # ---------------------------------------------------------------------
        # 2. Создание нового пула через create_pool()
        # ---------------------------------------------------------------------
        print(f"\n[2] Создание нового пула: {pool_name}")
        print("-" * 40)

        create_body = PoolCreateBody(
            type=pool_type,
            name=pool_name,
            host=pool_host,
            port=pool_port,
            user=pool_user,
            **{"pass": pool_pass},
            notes=pool_notes,
        )

        create_response: MRRResponse[PoolCreateResponse] = await client.account.create_pool(body=create_body)

        if not create_response.success:
            print(f"Ошибка при создании пула: {create_response.error}")
            return

        create_data = create_response.data
        new_pool_id = create_data.id if create_data else None
        print(f"Пул успешно создан! ID: {new_pool_id}")

        # ---------------------------------------------------------------------
        # 3. Получение пулов по ID через get_pools_by_ids()
        # ---------------------------------------------------------------------
        print("\n[3] Получение пулов по ID")
        print("-" * 40)

        if new_pool_id:
            # Получаем только что созданный пул
            get_by_ids_response: MRRResponse[list[Pool]] = await client.account.get_pools_by_ids(ids=[new_pool_id])

            if not get_by_ids_response.success:
                print(f"Ошибка при получении пулов по ID: {get_by_ids_response.error}")
            else:
                found_pools = get_by_ids_response.data
                if found_pools:
                    print(f"Найдено пулов: {len(found_pools)}")
                    for pool in found_pools:
                        print(f"\n  ID: {pool.id}")
                        print(f"    Название: {pool.name}")
                        print(f"    Хост: {pool.host}:{pool.port}")
                else:
                    print("Пулы по указанным ID не найдены")
        else:
            print("Пропуск получения пулов по ID (нет ID созданного пула)")

        # ---------------------------------------------------------------------
        # 4. Тестирование подключения к пулу через test_pool()
        # ---------------------------------------------------------------------
        print("\n[4] Тестирование подключения к пулу")
        print("-" * 40)

        test_body = PoolTestBody(
            method="simple",
            type=pool_type,
            host=pool_host,
            port=pool_port,
            user=pool_user,
            **{"pass": pool_pass},
        )

        test_response: MRRResponse[PoolTestResult] = await client.account.test_pool(body=test_body)

        if not test_response.success:
            print(f"Ошибка при тестировании пула: {test_response.error}")
        else:
            test_result = test_response.data
            if test_result:
                print(f"Результаты теста ({len(test_result.result)} проверок):")
                for item in test_result.result:
                    status = "✓" if item.connection else "✗"
                    print(f"  {status} {item.dest}:")
                    print(f"    Соединение: {item.connection}")
                    print(f"    Время выполнения: {item.executiontime}s")
                    if item.protocol:
                        print(f"    Протокол: {item.protocol}")
                    if item.sub is not None:
                        print(f"    Sub: {item.sub}")
                    if item.auth is not None:
                        print(f"    Auth: {item.auth}")
                    if item.diff is not None:
                        print(f"    Diff: {item.diff}")
                if test_result.error:
                    print(f"Ошибки: {test_result.error}")

        # ---------------------------------------------------------------------
        # 5. Обновление пулов через update_pools()
        # ---------------------------------------------------------------------
        print("\n[5] Обновление пулов")
        print("-" * 40)

        if new_pool_id:
            # Обновляем заметки созданного пула
            update_body = {
                "notes": f"{pool_notes} (обновлено)",
            }

            update_response: MRRResponse[None] = await client.account.update_pools(
                ids=[new_pool_id],
                body=update_body,
            )

            if not update_response.success:
                print(f"Ошибка при обновлении пула: {update_response.error}")
            else:
                print("Пулы успешно обновлены!")

                # Проверяем обновление
                verify_response: MRRResponse[list[Pool]] = await client.account.get_pools_by_ids(ids=[new_pool_id])
                if verify_response.success and verify_response.data:
                    updated_pool = verify_response.data[0]
                    print(f"Новые заметки: {updated_pool.notes}")
        else:
            print("Пропуск обновления пулов (нет ID созданного пула)")

        # ---------------------------------------------------------------------
        # 6. Удаление пулов через delete_pools()
        # ---------------------------------------------------------------------
        print("\n[6] Удаление пулов")
        print("-" * 40)

        if new_pool_id:
            delete_response: MRRResponse[None] = await client.account.delete_pools(ids=[new_pool_id])

            if not delete_response.success:
                print(f"Ошибка при удалении пула: {delete_response.error}")
            else:
                print(f"Пулы успешно удалены! ID: {new_pool_id}")
        else:
            print("Пропуск удаления пулов (нет ID созданного пула)")

    print("\n" + "=" * 60)
    print("Клиент закрыт.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

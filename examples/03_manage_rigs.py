"""Пример управления ригами для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Загрузку API-ключей из переменных окружения
- Инициализацию клиента через контекстный менеджер
- Получение списка своих ригов через get_mining_rigs()
- Получение ригов по ID через get_rigs()
- Создание нового рига через create_rig()
- Удаление ригов через delete_rigs()

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/rigs.md
"""

import asyncio
import os
import sys

from aio_mrr import MRRClient, MRRResponse, RigCreateBody, RigInfo


async def main() -> None:
    """Основная функция примера."""
    # Загрузка API-ключей из переменных окружения
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    # Проверка наличия ключей
    if not api_key or not api_secret:
        print("Ошибка: API-ключи не найдены. Установите переменные окружения MRR_API_KEY и MRR_API_SECRET.")
        sys.exit(1)

    # Получение параметров для создания рига из переменных окружения
    # Если переменные не установлены, будут использованы значения по умолчанию
    rig_name = os.environ.get("MRR_RIG_NAME", "Example Rig")
    rig_server = os.environ.get("MRR_RIG_SERVER", "EU-01")
    rig_hashrate = float(os.environ.get("MRR_RIG_HASHRATE", "50.0"))
    rig_algorithm = os.environ.get("MRR_RIG_ALGO", "kawpow")

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # 1. Получение списка своих ригов через get_mining_rigs()
        print("Получение списка своих ригов...")
        mining_rigs_response: MRRResponse[list[RigInfo]] = await client.rig.get_mining_rigs()

        if not mining_rigs_response.success:
            print(f"Ошибка при получении ригов: {mining_rigs_response.error}")
            return

        mining_rigs = mining_rigs_response.data
        if mining_rigs:
            print(f"\nНайдено ригов: {len(mining_rigs)}")
            for rig in mining_rigs:
                # rig.status can be str or dict, handle both cases
                status_display = (
                    rig.status
                    if isinstance(rig.status, str)
                    else (rig.status.get("status") if isinstance(rig.status, dict) else "N/A")
                )
                print(f"  ID: {rig.id}, Имя: {rig.name}, Статус: {status_display}")
        else:
            print("Ваши риги отсутствуют")

        # 2. Получение ригов по ID через get_rigs()
        # Используем ID ригов из предыдущего запроса (если есть)
        if mining_rigs:
            rig_ids = [rig.id for rig in mining_rigs[:3]]  # Берём первые 3 рига
            print(f"\nПолучение информации о ригах по ID: {rig_ids}...")
            rigs_by_id_response: MRRResponse[list[RigInfo]] = await client.rig.get_rigs(ids=rig_ids)

            if not rigs_by_id_response.success:
                print(f"Ошибка при получении ригов по ID: {rigs_by_id_response.error}")
                return

            rigs_by_id = rigs_by_id_response.data
            if rigs_by_id:
                print(f"\nПолучено {len(rigs_by_id)} ригов по ID:")
                for rig in rigs_by_id:
                    # rig.status can be str or dict, handle both cases
                    status_display = (
                        rig.status
                        if isinstance(rig.status, str)
                        else (rig.status.get("status") if isinstance(rig.status, dict) else "N/A")
                    )
                    print(f"  ID: {rig.id}, Имя: {rig.name}")
                    print(f"    Сервер: {rig.server}, Статус: {status_display}")
                    if rig.hash:
                        print(f"    Хешрейт: {rig.hash.hash} {rig.hash.type}")
        else:
            print("\nПропуск получения ригов по ID (нет ригов для запроса)")

        # 3. Создание нового рига через create_rig()
        print(f"\nСоздание нового рига: {rig_name}...")
        rig_create_body = RigCreateBody(
            name=rig_name,
            description="Риг, созданный через пример кода aio-mrr",
            server=rig_server,
            price_btc_enabled=True,
            price_btc_price=0.001,
            minhours=1.0,
            maxhours=24.0,
            extensions=True,
            hash_hash=rig_hashrate,
            hash_type=rig_algorithm,
            ndevices=1,
        )

        create_response: MRRResponse[dict[str, object]] = await client.rig.create_rig(body=rig_create_body)

        if not create_response.success:
            print(f"Ошибка при создании рига: {create_response.error}")
            return

        # Получаем ID созданного рига
        create_data = create_response.data
        if create_data and "id" in create_data:
            new_rig_id = int(create_data["id"])
            print(f"Риг успешно создан! ID: {new_rig_id}")

            # 4. Удаление созданного рига через delete_rigs()
            print(f"Удаление созданного рига (ID: {new_rig_id})...")
            delete_response: MRRResponse[None] = await client.rig.delete_rigs(ids=[new_rig_id])

            if not delete_response.success:
                print(f"Ошибка при удалении рига: {delete_response.error}")
                return

            print("Риг успешно удалён!")
        else:
            print("Ошибка: не удалось получить ID созданного рига")

    print("\nКлиент закрыт.")


if __name__ == "__main__":
    asyncio.run(main())

"""Пример управления профилями для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Получение всех пул-профилей через get_profiles()
- Создание нового профиля через create_profile()
- Получение профиля по ID через get_profile()
- Обновление профиля через update_profile()
- Обновление приоритета профиля через update_profile_priority()
- Удаление профиля через delete_profile()

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
    Profile,
    ProfileCreateBody,
    ProfileCreateResponse,
    ProfileDeleteResponse,
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

    # Получение данных профиля из переменных окружения
    profile_name = os.environ.get("MRR_PROFILE_NAME", "Example Profile")
    profile_algo = os.environ.get("MRR_PROFILE_ALGO", "kawpow")

    print("=" * 60)
    print("ПРИМЕР УПРАВЛЕНИЯ ПРОФИЛЯМИ")
    print("=" * 60)

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # ---------------------------------------------------------------------
        # 1. Получение всех пул-профилей через get_profiles()
        # ---------------------------------------------------------------------
        print("\n[1] Получение всех пул-профилей")
        print("-" * 40)

        get_profiles_response: MRRResponse[list[Profile]] = await client.account.get_profiles()

        if not get_profiles_response.success:
            print(f"Ошибка при получении профилей: {get_profiles_response.error}")
            return

        profiles = get_profiles_response.data
        if profiles:
            print(f"Найдено профилей: {len(profiles)}")
            for profile in profiles:
                print(f"\n  ID: {profile.id}")
                print(f"    Название: {profile.name}")
                print(f"    Алгоритм: {profile.algo.name}")
                print(
                    f"    Рекомендуемая цена: {profile.algo.suggested_price.amount} "
                    f"{profile.algo.suggested_price.currency}"
                )
                print(f"    Пулов в профиле: {len(profile.pools)}")
                for pool in profile.pools:
                    print(f"      - {pool.type}://{pool.host}:{pool.port} (приоритет: {pool.priority})")
        else:
            print("Профили отсутствуют")

        # ---------------------------------------------------------------------
        # 2. Создание нового профиля через create_profile()
        # ---------------------------------------------------------------------
        print(f"\n[2] Создание нового профиля: {profile_name}")
        print("-" * 40)

        create_body = ProfileCreateBody(
            name=profile_name,
            algo=profile_algo,
        )

        create_response: MRRResponse[ProfileCreateResponse] = await client.account.create_profile(body=create_body)

        if not create_response.success:
            print(f"Ошибка при создании профиля: {create_response.error}")
            return

        create_data = create_response.data
        new_profile_id = create_data.pid if create_data else None
        print(f"Профиль успешно создан! ID: {new_profile_id}")

        # ---------------------------------------------------------------------
        # 3. Получение профиля по ID через get_profile()
        # ---------------------------------------------------------------------
        print("\n[3] Получение профиля по ID")
        print("-" * 40)

        if new_profile_id:
            get_profile_response: MRRResponse[Profile] = await client.account.get_profile(pid=int(new_profile_id))

            if not get_profile_response.success:
                print(f"Ошибка при получении профиля: {get_profile_response.error}")
            else:
                profile_info = get_profile_response.data
                if profile_info:
                    print(f"ID: {profile_info.id}")
                    print(f"Название: {profile_info.name}")
                    print(f"Алгоритм: {profile_info.algo.name}")
                    print(f"Дисплей: {profile_info.algo.display}")
                    print(
                        f"Рекомендуемая цена: {profile_info.algo.suggested_price.amount} "
                        f"{profile_info.algo.suggested_price.currency} "
                        f"за {profile_info.algo.suggested_price.unit}"
                    )
                    print(f"Пулов в профиле: {len(profile_info.pools)}")
                    for pool in profile_info.pools:
                        print(f"  - {pool.type}://{pool.host}:{pool.port}")
                        print(f"    User: {pool.user}, Priority: {pool.priority}")
                        print(f"    Статус: {pool.status}")
                else:
                    print("Профиль не найден")
        else:
            print("Пропуск получения профиля по ID (нет ID созданного профиля)")

        # ---------------------------------------------------------------------
        # 4. Обновление профиля через update_profile()
        # ---------------------------------------------------------------------
        print("\n[4] Обновление профиля")
        print("-" * 40)

        if new_profile_id:
            # Для обновления профиля нужно указать poolid и priority
            # Сначала получим список пулов
            pools_response: MRRResponse[list[Pool]] = await client.account.get_pools()

            if pools_response.success and pools_response.data:
                # Используем первый доступный пул
                pool_to_add = pools_response.data[0]
                poolid = pool_to_add.id

                update_response: MRRResponse[None] = await client.account.update_profile(
                    pid=int(new_profile_id),
                    poolid=poolid,
                    priority=1,
                )

                if not update_response.success:
                    print(f"Ошибка при обновлении профиля: {update_response.error}")
                else:
                    print(f"Профиль успешно обновлён! Добавлен пул ID: {poolid} с приоритетом 1")
            else:
                print("Нет доступных пулов для добавления в профиль")
        else:
            print("Пропуск обновления профиля (нет ID созданного профиля)")

        # ---------------------------------------------------------------------
        # 5. Обновление приоритета профиля через update_profile_priority()
        # ---------------------------------------------------------------------
        print("\n[5] Обновление приоритета пула в профиле")
        print("-" * 40)

        if new_profile_id:
            # Получаем пул для обновления приоритета
            pools_response_2: MRRResponse[list[Pool]] = await client.account.get_pools()

            if pools_response_2.success and pools_response_2.data:
                pool_to_update = pools_response_2.data[0]
                poolid = pool_to_update.id

                # Устанавливаем приоритет (0-4, где 0 - самый высокий)
                new_priority = 2

                priority_response: MRRResponse[None] = await client.account.update_profile_priority(
                    pid=int(new_profile_id),
                    priority=new_priority,
                    poolid=poolid,
                )

                if not priority_response.success:
                    print(f"Ошибка при обновлении приоритета: {priority_response.error}")
                else:
                    print(f"Приоритет успешно обновлён! Пул ID: {poolid}, Приоритет: {new_priority}")
            else:
                print("Нет доступных пулов для обновления приоритета")
        else:
            print("Пропуск обновления приоритета (нет ID созданного профиля)")

        # ---------------------------------------------------------------------
        # 6. Удаление профиля через delete_profile()
        # ---------------------------------------------------------------------
        print("\n[6] Удаление профиля")
        print("-" * 40)

        if new_profile_id:
            delete_response: MRRResponse[ProfileDeleteResponse] = await client.account.delete_profile(
                pid=int(new_profile_id)
            )

            if not delete_response.success:
                print(f"Ошибка при удалении профиля: {delete_response.error}")
            else:
                delete_data = delete_response.data
                if delete_data:
                    print("Профиль успешно удалён!")
                    print(f"  ID: {delete_data.id}")
                    print(f"  Успех: {delete_data.success}")
                    print(f"  Сообщение: {delete_data.message}")
        else:
            print("Пропуск удаления профиля (нет ID созданного профиля)")

    print("\n" + "=" * 60)
    print("Клиент закрыт.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

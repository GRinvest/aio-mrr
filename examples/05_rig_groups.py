"""Пример управления группами ригов для библиотеки aio-mrr.

Этот скрипт демонстрирует:
- Загрузку API-ключей из переменных окружения
- Инициализацию клиента через контекстный менеджер
- Получение списка групп ригов через get_list()
- Создание новой группы через create()
- Получение группы по ID через get_by_id()
- Обновление группы через update()
- Добавление ригов в группу через add_rigs()
- Удаление ригов из группы через remove_rigs()
- Удаление группы через delete()

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/rig-groups.md
"""

import asyncio
import os
import sys

from aio_mrr import (
    MRRClient,
    MRRResponse,
    RigGroupCreateBody,
    RigGroupInfo,
    RigGroupUpdateBody,
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

    # Получение параметров для создания группы из переменных окружения
    group_name = os.environ.get("MRR_GROUP_NAME", "Example Rig Group")
    group_rental_limit = int(os.environ.get("MRR_GROUP_RENTAL_LIMIT", "5"))

    # Получение ID ригов для добавления в группу (из переменных окружения или использовать заглушки)
    rig_ids_str = os.environ.get("MRR_RIG_IDS", "12345,12346")
    rig_ids = [int(rig_id.strip()) for rig_id in rig_ids_str.split(",") if rig_id.strip()]

    # Инициализация клиента через контекстный менеджер
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # 1. Получение списка групп ригов через get_list()
        print("Получение списка групп ригов...")
        groups_list_response: MRRResponse[list[RigGroupInfo]] = await client.riggroup.get_list()

        if not groups_list_response.success:
            print(f"Ошибка при получении списка групп: {groups_list_response.error}")
            return

        groups_list = groups_list_response.data
        if groups_list:
            print(f"\nНайдено групп: {len(groups_list)}")
            for group in groups_list:
                print(f"  ID: {group.id}, Название: {group.name}, Активна: {group.enabled}")
                print(f"    Лимит аренд: {group.rental_limit}, Ригов в группе: {len(group.rigs)}")
                if group.algo:
                    print(f"    Алгоритм: {group.algo}")
        else:
            print("Группы ригов отсутствуют")

        # 2. Создание новой группы через create()
        print(f"\nСоздание новой группы: {group_name}...")
        create_body = RigGroupCreateBody(
            name=group_name,
            enabled=True,
            rental_limit=group_rental_limit,
        )

        create_response: MRRResponse[dict[str, object]] = await client.riggroup.create(body=create_body)

        if not create_response.success:
            print(f"Ошибка при создании группы: {create_response.error}")
            return

        # Получаем ID созданной группы
        create_data = create_response.data
        if create_data and "id" in create_data:
            new_group_id = int(create_data["id"])
            print(f"Группа успешно создана! ID: {new_group_id}")
        else:
            print("Ошибка: не удалось получить ID созданной группы")
            return

        # 3. Получение группы по ID через get_by_id()
        print(f"\nПолучение информации о группе по ID: {new_group_id}...")
        get_by_id_response: MRRResponse[RigGroupInfo] = await client.riggroup.get_by_id(id=new_group_id)

        if not get_by_id_response.success:
            print(f"Ошибка при получении группы по ID: {get_by_id_response.error}")
            # Пробуем удалить созданную группу даже при ошибке получения
            await client.riggroup.delete(id=new_group_id)
            return

        group_info = get_by_id_response.data
        print(f"Название группы: {group_info.name}")
        print(f"Статус: {'Активна' if group_info.enabled else 'Неактивна'}")
        print(f"Лимит аренд: {group_info.rental_limit}")
        print(f"Ригов в группе: {len(group_info.rigs)}")
        if group_info.algo:
            print(f"Алгоритм: {group_info.algo}")

        # 4. Обновление группы через update()
        print(f"\nОбновление группы (ID: {new_group_id})...")
        update_body = RigGroupUpdateBody(
            name=f"{group_name} (Обновлено)",
            rental_limit=group_rental_limit + 5,
        )

        update_response: MRRResponse[None] = await client.riggroup.update(id=new_group_id, body=update_body)

        if not update_response.success:
            print(f"Ошибка при обновлении группы: {update_response.error}")
            # Пробуем удалить созданную группу даже при ошибке обновления
            await client.riggroup.delete(id=new_group_id)
            return

        print("Группа успешно обновлена!")

        # 5. Добавление ригов в группу через add_rigs()
        if rig_ids:
            print(f"\nДобавление ригов {rig_ids} в группу (ID: {new_group_id})...")
            add_rigs_response: MRRResponse[dict[str, object]] = await client.riggroup.add_rigs(
                id=new_group_id,
                rig_ids=rig_ids,
            )

            if not add_rigs_response.success:
                print(f"Ошибка при добавлении ригов в группу: {add_rigs_response.error}")
            else:
                add_data = add_rigs_response.data
                if add_data and "rigs" in add_data:
                    rigs_in_group = add_data["rigs"]
                    print(f"Риги успешно добавлены! Текущие риги в группе: {rigs_in_group}")
                else:
                    print("Риги добавлены, но не удалось получить список ригов в группе")
        else:
            print("\nПропуск добавления ригов (нет ID ригов для добавления)")

        # 6. Удаление ригов из группы через remove_rigs()
        if rig_ids:
            print(f"\nУдаление ригов {rig_ids} из группы (ID: {new_group_id})...")
            remove_rigs_response: MRRResponse[dict[str, object]] = await client.riggroup.remove_rigs(
                id=new_group_id,
                rig_ids=rig_ids,
            )

            if not remove_rigs_response.success:
                print(f"Ошибка при удалении ригов из группы: {remove_rigs_response.error}")
            else:
                remove_data = remove_rigs_response.data
                if remove_data and "rigs" in remove_data:
                    remaining_rigs = remove_data["rigs"]
                    print(f"Риги успешно удалены! Оставшиеся риги в группе: {remaining_rigs}")
                else:
                    print("Риги удалены, но не удалось получить список ригов в группе")
        else:
            print("\nПропуск удаления ригов (нет ID ригов для удаления)")

        # 7. Удаление группы через delete()
        print(f"\nУдаление группы (ID: {new_group_id})...")
        delete_response: MRRResponse[dict[str, object]] = await client.riggroup.delete(id=new_group_id)

        if not delete_response.success:
            print(f"Ошибка при удалении группы: {delete_response.error}")
            return

        delete_data = delete_response.data
        if delete_data and "message" in delete_data:
            print(f"Группа успешно удалена! Сообщение: {delete_data['message']}")
        else:
            print("Группа успешно удалена!")

    print("\nКлиент закрыт.")


if __name__ == "__main__":
    asyncio.run(main())

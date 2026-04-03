"""Пример работы с арендами (Rentals API).

Этот скрипт демонстрирует:
- Получение списка аренд
- Создание новой аренды
- Получение аренды по ID
- Продление аренды
- Получение лога аренды
- Получение сообщений аренды

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
См.: docs/api-reference/rentals.md
"""

from __future__ import annotations
import asyncio
import os
import sys

from aio_mrr import MRRClient, RentalCreateBody, RentalInfo


async def main() -> None:
    """Основная функция примера работы с арендами."""
    # Загрузка API-ключей из переменных окружения
    # ВАЖНО: NE хардкодить ключи в коде!
    api_key: str | None = os.environ.get("MRR_API_KEY")
    api_secret: str | None = os.environ.get("MRR_API_SECRET")

    # Проверка наличия ключей
    if not api_key or not api_secret:
        print("Ошибка: API-ключи не найдены в переменных окружения")
        print("Установите MRR_API_KEY и MRR_API_SECRET")
        sys.exit(1)

    # Инициализация клиента c контекстным менеджером
    async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
        # 1. Получение списка аренд
        print("=== Получение списка аренд ===")
        response = await client.rental.get_list(params={"type": "renter", "history": False})

        if not response.success:
            print(f"Ошибка при получении списка аренд: {response.error}")
            return

        rentals: list[RentalInfo] = response.data
        print(f"Найдено активных аренд: {len(rentals)}")

        # Сохраняем ID первой аренды для дальнейших операций
        rental_id: int | None = None
        if rentals:
            rental_id = int(rentals[0].id)
            print(f"Первая аренда ID: {rental_id}, статус: {rentals[0].status}")
        else:
            print("Нет активных аренд, создадим новую...")

        # 2. Создание новой аренды (если нет активных)
        created_rental_id: int | None = rental_id

        if rental_id is None:
            # Получаем ID рига для аренды (можно установить через env)
            rig_id_str: str | None = os.environ.get("MRR_RIG_ID")
            if not rig_id_str:
                print("Ошибка: MRR_RIG_ID не установлен в переменных окружения")
                print("Создание аренды невозможно без ID рига")
                return

            rig_id: int = int(rig_id_str)

            # Получаем ID профиля (можно установить через env)
            profile_id_str: str | None = os.environ.get("MRR_PROFILE_ID")
            if not profile_id_str:
                print("Ошибка: MRR_PROFILE_ID не установлен в переменных окружения")
                print("Создание аренды невозможно без ID профиля")
                return

            profile_id: int = int(profile_id_str)

            # Получаем длительность аренды в часах (по умолчанию 24 часа)
            length_str: str | None = os.environ.get("MRR_RENTAL_LENGTH", "24")
            length: float = float(length_str)

            # Создаем тело запроса для аренды
            body = RentalCreateBody(
                rig=rig_id,
                length=length,
                profile=profile_id,
                currency="BTC",
            )

            print("\n=== Создание аренды ===")
            print(f"Риг ID: {rig_id}, Длительность: {length} часов, Профиль: {profile_id}")

            response = await client.rental.create(body=body)

            if not response.success:
                print(f"Ошибка при создании аренды: {response.error}")
                return

            # Получаем ID созданной аренды
            created_data: dict[str, object] = response.data
            created_rental_id = int(created_data["id"])
            print(f"Аренда создана c ID: {created_rental_id}")

        # 3. Получение аренды по ID
        if created_rental_id is not None:
            print(f"\n=== Получение аренды по ID: {created_rental_id} ===")
            response = await client.rental.get_by_ids(ids=[created_rental_id])

            if not response.success:
                print(f"Ошибка при получении аренды: {response.error}")
                return

            rental: RentalInfo = response.data
            print(f"Аренда ID: {rental.id}")
            print(f"Риг ID: {rental.rig_id}")
            print(f"Риг имя: {rental.rig_name or 'N/A'}")
            print(f"Статус: {rental.status}")
            print(f"Начало: {rental.started}")
            print(f"Конец: {rental.ends}")
            print(f"Длительность: {rental.length} часов")
            print(f"Валюта: {rental.currency}")

        # 4. Продление аренды
        if created_rental_id is not None:
            # Часы для продления (по умолчанию 1 час)
            extend_hours_str: str | None = os.environ.get("MRR_EXTEND_HOURS", "1")
            extend_hours: float = float(extend_hours_str)

            print(f"\n=== Продление аренды ID: {created_rental_id} ===")
            print(f"Продление на {extend_hours} часов")

            response = await client.rental.extend(ids=[created_rental_id], length=extend_hours)

            if not response.success:
                print(f"Ошибка при продлении аренды: {response.error}")
                return

            print("Аренда успешно продлена")

        # 5. Получение лога аренды
        if created_rental_id is not None:
            print(f"\n=== Лог аренды ID: {created_rental_id} ===")
            response = await client.rental.get_log(ids=[created_rental_id])

            if not response.success:
                print(f"Ошибка при получении лога: {response.error}")
                return

            log_entries = response.data
            print(f"Записей в логе: {len(log_entries)}")

            for entry in log_entries[:5]:  # Показываем первые 5 записей
                print(f"  [{entry.time}] {entry.message}")

        # 6. Получение сообщений аренды
        if created_rental_id is not None:
            print(f"\n=== Сообщения аренды ID: {created_rental_id} ===")
            response = await client.rental.get_message(ids=[created_rental_id])

            if not response.success:
                print(f"Ошибка при получении сообщений: {response.error}")
                return

            messages = response.data
            print(f"Сообщений: {len(messages)}")

            for msg in messages:
                print(f"  [{msg.time}] {msg.user}: {msg.message}")


if __name__ == "__main__":
    # Запуск асинхронной основной функции
    asyncio.run(main())

# aio-mrr Documentation

Асинхронная библиотека для работы с MiningRigRentals API v2.

## Описание

`aio-mrr` — это современный асинхронный клиент для интеграции с MiningRigRentals API v2. Библиотека предоставляет типизированный интерфейс ко всем 56 публичным методам API, используя современные возможности Python 3.12+.

Ключевая особенность библиотеки — полное отсутствие исключений: все ответы оборачиваются в универсальный тип `MRRResponse[T]`, что упрощает обработку ошибок и делает код более предсказуемым.

## Ключевые особенности

- **async/await** — полностью асинхронный API на базе `aiohttp`
- **Pydantic v2** — строгая типизация всех ответов через Pydantic-модели
- **Retry-стратегия** — автоматические повторные запросы при ошибках сети и rate limiting (через `tenacity`)
- **HMAC-SHA1 аутентификация** — безопасная подпись запросов с маскированием секретов
- **Connection pooling** — эффективное управление соединениями для высоконагруженных сценариев
- **Result pattern** — паттерн Result вместо исключений для обработки ошибок

## Требования

- **Python**: 3.12+
- **Зависимости**:
  - `aiohttp>=3.13.0` — асинхронный HTTP-клиент
  - `pydantic>=2.12.0` — валидация и типизация данных
  - `tenacity>=9.1.0` — стратегия повторных попыток
  - `loguru>=0.7.0` — логирование

## Установка

### Стабильная версия

```bash
pip install aio-mrr
```

### Разработка

Для разработки и тестирования установите пакет в режиме редактирования с дополнительными зависимостями:

```bash
pip install -e ".[dev]"
```

---

## Быстрый старт

!!! tip "Быстрый старт"

    Минимальный пример инициализации клиента и выполнения запроса:

    ```python
    import os
    import asyncio
    from aio_mrr import MRRClient

    async def main():
        # Загрузка ключей из переменных окружения
        api_key = os.environ.get("MRR_API_KEY")
        api_secret = os.environ.get("MRR_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("Необходимо установить MRR_API_KEY и MRR_API_SECRET")

        # Инициализация клиента с контекстным менеджером
        async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
            # Проверка аутентификации
            response = await client.whoami()
            if not response.success:
                print(f"Ошибка аутентификации: {response.error}")
                return

            print(f"Вход как: {response.data}")

            # Получение баланса
            balance = await client.account.get_balance()
            if balance.success:
                print(f"Баланс: {balance.data}")

    asyncio.run(main())
    ```

    См. также: [`examples/01_quickstart.py`](examples/01_quickstart.py)

---

## Таблица содержимого

### Начало работы

- **[Установка и аутентификация](authentication.md)** — получение API-ключей, инициализация клиента, HMAC-SHA1 аутентификация
- **[Обработка ошибок](error-handling.md)** — паттерн Result, типы ошибок, retry-стратегия
- **[Модели данных](models.md)** — полное описание всех Pydantic-моделей библиотеки

### Справочник API

- **[Аккаунт и профили](api-reference/account.md)** — 16 методов управления аккаунтом, пулами и профилями
- **[Риги](api-reference/rigs.md)** — 15 методов управления ригами (CRUD, поиск, графики)
- **[Аренды](api-reference/rentals.md)** — 12 методов управления арендами (создание, продление, логи)
- **[Группы ригов](api-reference/rig-groups.md)** — 7 методов управления группами ригов
- **[Информация](api-reference/info.md)** — 4 метода получения информации о серверах и алгоритмах
- **[Ценообразование](api-reference/pricing.md)** — 1 метод получения курсов конвертации и рыночных цен

---

## Примеры

В репозитории представлены 10 готовых примеров для различных сценариев использования:

| Файл | Описание |
| --- | --- |
| [`examples/01_quickstart.py`](examples/01_quickstart.py) | Базовая инициализация, whoami, баланс |
| [`examples/02_account_balance.py`](examples/02_account_balance.py) | Профиль, баланс, транзакции |
| [`examples/03_manage_rigs.py`](examples/03_manage_rigs.py) | Получение, создание, удаление ригов |
| [`examples/04_create_rental.py`](examples/04_create_rental.py) | Создание аренды, продление, логи |
| [`examples/05_rig_groups.py`](examples/05_rig_groups.py) | CRUD групп ригов, добавление/удаление |
| [`examples/06_info_and_pricing.py`](examples/06_info_and_pricing.py) | Серверы, алгоритмы, курсы, цены |
| [`examples/07_error_handling_demo.py`](examples/07_error_handling_demo.py) | Демонстрация всех типов ошибок |
| [`examples/08_advanced_search.py`](examples/08_advanced_search.py) | Поиск ригов с фильтрами |
| [`examples/09_pool_management.py`](examples/09_pool_management.py) | CRUD пулов, тестирование пулов |
| [`examples/10_profile_management.py`](examples/10_profile_management.py) | CRUD профилей, приоритеты |

!!! note "Примечание"

    Все примеры используют переменные окружения для хранения API-ключей. Не храните ключи в коде!

    ```bash
    export MRR_API_KEY="your_api_key"
    export MRR_API_SECRET="your_api_secret"
    ```

---

## Безопасность

- **НЕ храните API-ключи в коде** — всегда используйте переменные окружения
- Библиотека автоматически маскирует секреты в логах через `SecretMasker`
- Проверьте наличие ключей перед запуском: `if not api_key: raise ValueError(...)`

---

## Ссылки

- Исходный код: [GitHub](https://github.com/GRinvest/aio-mrr)
- Репозиторий примеров: [examples/](https://github.com/GRinvest/aio-mrr/tree/main/examples/)
- MiningRigRentals API: [https://miningrigrentals.com](https://miningrigrentals.com)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

# aio-mrr

**Асинхронная библиотека для MiningRigRentals API v2**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black)](https://github.com/astral-sh/ruff)

## 📖 Описание

`aio-mrr` — это асинхронный Python-клиент для [MiningRigRentals API v2](https://miningrigrentals.com/), построенный на основе `aiohttp` и `pydantic`. Библиотека предоставляет типизированный интерфейс ко всем методам API с автоматической обработкой ошибок, retry-логикой и HMAC-SHA1 аутентификацией.

## ✨ Особенности

- **async/await** — полностью асинхронный API
- **Pydantic модели** — автоматическая валидация и типизация ответов
- **Retry-логика** — автоматические повторные попытки при ошибках сети
- **HMAC-SHA1 аутентификация** — безопасная работа с API
- **Connection pooling** — эффективное управление соединениями
- **Маскирование секретов** — защита API-ключей при логировании

## 📦 Установка

```bash
pip install aio-mrr
```

Для разработки:

```bash
pip install -e ".[dev]"
```

## 🚀 Быстрый старт

```python
import asyncio
from aio_mrr import MRRClient

async def main():
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    
    async with MRRClient(api_key, api_secret) as client:
        # Проверка аутентификации
        response = await client.whoami()
        if response.success:
            print(f"Logged in as: {response.data['username']}")
        
        # Получение баланса
        balance = await client.account.get_balance()
        if balance.success:
            print(f"Balance: {balance.data}")

asyncio.run(main())
```

## 📚 Документация

Полная документация доступна на [GitHub Pages](https://GRinvest.github.io/aio-mrr/):

- [Установка и аутентификация](https://GRinvest.github.io/aio-mrr/authentication/)
- [Обработка ошибок](https://GRinvest.github.io/aio-mrr/error-handling/)
- [Модели данных](https://GRinvest.github.io/aio-mrr/models/)
- [Справочник API](https://GRinvest.github.io/aio-mrr/api-reference/account/)

## 💡 Примеры

Примеры использования доступны в папке [`examples/`](examples/):

- [`01_quickstart.py`](examples/01_quickstart.py) — базовая инициализация и простой запрос
- [`02_account_balance.py`](examples/02_account_balance.py) — работа с аккаунтом
- [`03_manage_rigs.py`](examples/03_manage_rigs.py) — управление ригами
- [`04_create_rental.py`](examples/04_create_rental.py) — создание аренд
- [`05_rig_groups.py`](examples/05_rig_groups.py) — управление группами ригов
- [`06_info_and_pricing.py`](examples/06_info_and_pricing.py) — информация и цены
- [`07_error_handling_demo.py`](examples/07_error_handling_demo.py) — обработка ошибок
- [`08_advanced_search.py`](examples/08_advanced_search.py) — продвинутый поиск
- [`09_pool_management.py`](examples/09_pool_management.py) — управление пулами
- [`10_profile_management.py`](examples/10_profile_management.py) — управление профилями

## 🔧 Требования

- Python 3.12+
- aiohttp >= 3.13.0
- pydantic >= 2.12.0
- tenacity >= 9.1.0
- loguru >= 0.7.0

## 📝 API Coverage

Библиотека покрывает все 55 публичных методов MiningRigRentals API v2:

| Subclient | Методы | Описание |
|-----------|--------|----------|
| Client | 1 | Проверка аутентификации |
| AccountClient | 16 | Аккаунт, баланс, пулы, профили |
| InfoClient | 4 | Серверы, алгоритмы, валюты |
| PricingClient | 1 | Курсы конвертации и цены |
| RigClient | 15 | Управление ригами |
| RentalClient | 12 | Управление арендами |
| RigGroupClient | 7 | Группы ригов |

## 🤝 Вклад

Приветствуются pull requests! Пожалуйста, создавайте issue для обсуждения изменений перед тем как делать PR.

## 📄 Лицензия

[MIT License](LICENSE.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

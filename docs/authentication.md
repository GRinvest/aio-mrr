# Аутентификация и инициализация клиента

## Получение API-ключей

Для работы с библиотекой `aio-mrr` необходимы API-ключи от аккаунта MiningRigRentals.

### Где найти API-ключи

1. Войдите в свой аккаунт на [MiningRigRentals.com](https://www.miningrigrentals.com)
2. Перейдите в **Личный кабинет** → **API Keys** (в верхнем меню)
3. Нажмите **Create New API Key**
4. Задайте имя ключа (например, "aio-mrr integration")
5. Скопируйте и сохраните:
   - **API Key** (публичный идентификатор)
   - **API Secret** (секретный ключ — покажите только один раз!)

> !!! warning "Безопасность"
> Никогда не делитесь своим API Secret и не загружайте его в публичные репозитории.

---

## Инициализация MRRClient

Класс `MRRClient` — основной входной пункт для работы с API.

### Параметры конструктора

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `api_key` | `str` | **Да** | Публичный API-ключ из личного кабинета MRR |
| `api_secret` | `str` | **Да** | Секретный API-ключ из личного кабинета MRR |
| `connect_timeout` | `float` | Нет | Таймаут подключения (по умолчанию: `30.0` секунд) |
| `read_timeout` | `float` | Нет | Таймаут чтения ответа (по умолчанию: `60.0` секунд) |
| `max_retries` | `int` | Нет | Максимальное количество повторных попыток при ошибках сети (по умолчанию: `3`) |

### Пример с контекстным менеджером (рекомендуется)

Контекстный менеджер автоматически управляет жизненным циклом клиента — открывает и закрывает соединение.

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    # Загрузка ключей из переменных окружения (НИКОГДА не хардкодить!)
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API-ключи не найдены. Установите переменные окружения MRR_API_KEY и MRR_API_SECRET")

    # Использование контекстного менеджера
    async with MRRClient(
        api_key=api_key,
        api_secret=api_secret,
        connect_timeout=30.0,
        read_timeout=60.0,
        max_retries=3
    ) as client:
        # Все запросы выполняются внутри блока
        response = await client.whoami()
        if response.success:
            print(f"Успешно аутентифицирован: {response.data}")
        else:
            print(f"Ошибка: {response.error}")

asyncio.run(main())
```

### Пример без контекстного менеджера

Если вам нужен больший контроль над жизненным циклом клиента:

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API-ключи не найдены")

    # Создание клиента вручную
    client = MRRClient(
        api_key=api_key,
        api_secret=api_secret
    )

    try:
        # Выполнение запросов
        response = await client.whoami()
        if response.success:
            print(f"Пользователь: {response.data}")
    finally:
        # ВАЖНО: всегда закрывайте клиент вручную
        await client.close()

asyncio.run(main())
```

---

## HMAC-SHA1 аутентификация

Библиотека использует HMAC-SHA1 для подписи запросов. Это обеспечивает целостность и аутентичность данных.

### Как это работает

Для каждого запроса к API библиотека автоматически генерирует следующие заголовки:

| Заголовок | Описание | Пример |
|-----------|----------|--------|
| `x-api-key` | Публичный API-ключ | `x-api-key: "abc123..."` |
| `x-api-nonce` | Уникальный номер запроса (timestamp + случайное число) | `x-api-nonce: "1712345678901_xyz"` |
| `x-api-sign` | HMAC-SHA1 подпись тела запроса | `x-api-sign: "sha1=..."` |

### Процесс подписи

1. Генерируется **nonce** (уникальный идентификатор запроса)
2. Формируется строка для подписи: `method + path + nonce + body`
3. Вычисляется **HMAC-SHA1** хэш с использованием `api_secret`
4. Подпись добавляется в заголовок `x-api-sign`

> !!! note
> Вам не нужно manually подписывать запросы — библиотека делает это автоматически.

---

## Метод `whoami()`

Метод `whoami()` — базовый способ проверки аутентификации.

### Сигнатура

```python
async def whoami() -> MRRResponse[dict[str, str]]
```

### Возвращаемое значение

При успешной аутентификации метод возвращает словарь с информацией об аккаунте:

```python
{
    "username": "your_username",
    "user_id": "12345"
}
```

### Пример использования

```python
response = await client.whoami()

if response.success:
    username = response.data["username"]
    print(f"Добро пожаловать, {username}!")
else:
    print(f"Ошибка аутентификации: {response.error.message}")
```

---

## Безопасность

### ⚠️ Никогда не хардкодите API-ключи

**НЕПРАВИЛЬНО:**
```python
# ❌ НИКОГДА так не делайте!
client = MRRClient(
    api_key="your_real_api_key",
    api_secret="your_real_api_secret"
)
```

**ПРАВИЛЬНО:**
```python
# ✅ Используйте переменные окружения
import os

api_key = os.environ.get("MRR_API_KEY")
api_secret = os.environ.get("MRR_API_SECRET")

client = MRRClient(
    api_key=api_key,
    api_secret=api_secret
)
```

### Настройка переменных окружения

#### Linux / macOS:
```bash
export MRR_API_KEY="your_api_key_here"
export MRR_API_SECRET="your_api_secret_here"
```

#### Windows (PowerShell):
```powershell
$env:MRR_API_KEY="your_api_key_here"
$env:MRR_API_SECRET="your_api_secret_here"
```

#### Windows (CMD):
```cmd
set MRR_API_KEY=your_api_key_here
set MRR_API_SECRET=your_api_secret_here
```

> !!! tip "Совет"
> Добавьте `.env` в `.gitignore`, если используете локальный файл с переменными окружения для тестирования.

---

## См. также

- [Пример быстрого старта](../examples/01_quickstart.py) — базовая инициализация и первый запрос
- [Обработка ошибок](./error-handling.md) — как обрабатывать ошибки API
- [Главная страница](./index.md) — оглавление документации

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

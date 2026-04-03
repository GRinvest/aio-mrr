# Обработка ошибок

## Архитектурное решение

Библиотека `aio-mrr` использует **паттерн Result** для обработки ошибок. Все методы возвращают обёртку `MRRResponse[T]`, которая содержит результат выполнения запроса.

> **Важно:** Библиотека **НЕ выбрасывает исключения** наружу. Все ошибки (сетевые, таймауты, ошибки API, ошибки валидации) возвращаются через структуру `MRRResponse`.

Это позволяет:
- Явно обрабатывать ошибки без try/except блоков
- Получать типизированные данные при успехе
- Получать детализированную информацию об ошибке при неудаче
- Отслеживать количество повторных попыток (retry)

---

## Структура MRRResponse[T]

Универсальная обёртка ответа для всех методов библиотеки:

```python
from typing import Generic, TypeVar, Any

T = TypeVar('T')

class MRRResponse(BaseMRRModel, Generic[T]):
    """Универсальная обёртка ответа API."""
    
    success: bool              # True если запрос успешен, False при ошибке
    data: T | None             # Типизированные данные (None при ошибке)
    error: MRRResponseError | None  # Объект ошибки (None при успехе)
    http_status: int | None    # HTTP статус-код ответа
    retry_count: int           # Количество повторных попыток (0 если не было retry)
```

### Поля MRRResponse

| Поле | Тип | Описание |
|------|-----|----------|
| `success` | `bool` | Флаг успеха: `True` при успешном запросе, `False` при ошибке |
| `data` | `T \| None` | Типизированные данные ответа. При успехе содержит результат, при ошибке — `None` |
| `error` | `MRRResponseError \| None` | Объект ошибки. При успехе — `None`, при ошибке — детальная информация |
| `http_status` | `int \| None` | HTTP статус-код ответа (200, 401, 429, 500 и т.д.) |
| `retry_count` | `int` | Количество выполненных повторных попыток (0 если запрос выполнен с первой попытки) |

---

## Структура MRRResponseError

Объект ошибки содержит детальную информацию о произошедшей ошибке:

```python
class MRRResponseError(BaseMRRModel):
    """Детали ошибки."""
    
    code: str                          # Тип ошибки (см. ниже)
    message: str                       # Человекочитаемое описание ошибки
    details: dict[str, Any] | None     # Дополнительные данные об ошибке
    http_status: int | None            # HTTP статус-код (если применимо)
```

### Поля MRRResponseError

| Поле | Тип | Описание |
|------|-----|----------|
| `code` | `str` | Код типа ошибки: `"network_error"`, `"timeout"`, `"api_error"`, `"validation_error"` |
| `message` | `str` | Человекочитаемое описание ошибки |
| `details` | `dict[str, Any] \| None` | Дополнительные данные (например, детали исключения или валидации) |
| `http_status` | `int \| None` | HTTP статус-код, если ошибка связана с HTTP-ответом |

---

## Типы ошибок

Библиотека определяет 4 типа ошибок. Каждый тип имеет уникальный код в поле `error.code`.

### 1. Network Error (`"network_error"`)

**Описание:** Ошибка сети — невозможность установить соединение с сервером MRR.

**Причины:**
- DNS-ошибка (не найден хост)
- Connection refused (сервер не отвечает)
- Прокси недоступен
- Нет интернет-соединения

**Пример ошибки:**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "network_error",
        "message": "Failed to establish connection: Name or service not known",
        "details": {"host": "api.miningrigrentals.com", "port": 443},
        "http_status": None
    },
    "http_status": None,
    "retry_count": 3
}
```

**Пример обработки:**
```python
from aio_mrr import MRRClient

async def check_connection():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.whoami()
        
        if not response.success:
            if response.error and response.error.code == "network_error":
                print(f"❌ Ошибка сети: {response.error.message}")
                print(f"   Попыток: {response.retry_count}")
                return
            
            print(f"❌ Ошибка: {response.error}")
            return
        
        print(f"✅ Подключение успешно: {response.data}")
```

---

### 2. Timeout (`"timeout"`)

**Описание:** Запрос превысил установленное время ожидания.

**Причины:**
- Сервер не отвечает в течение таймаута
- Медленное интернет-соединение
- Перегрузка сервера MRR

**Пример ошибки:**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "timeout",
        "message": "Request timed out after 60.0 seconds",
        "details": {"timeout": 60.0, "endpoint": "/api/v2/account"},
        "http_status": None
    },
    "http_status": None,
    "retry_count": 3
}
```

**Пример обработки:**
```python
async def get_account():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_account()
        
        if not response.success:
            if response.error and response.error.code == "timeout":
                print(f"⏱️ Таймаут запроса: {response.error.message}")
                print(f"   Попробуйте увеличить connect_timeout/read_timeout")
                return
            
            print(f"❌ Ошибка: {response.error}")
            return
        
        print(f"✅ Данные аккаунта: {response.data.username}")
```

---

### 3. API Error (`"api_error"`)

**Описание:** Ошибка, возвращённая API MRR (статусы 4xx, 5xx).

**Причины:**
- Неверный API-ключ (401)
- Недостаточно прав (403)
- Ресурс не найден (404)
- Частые запросы — rate limit (429)
- Ошибка сервера MRR (500, 502, 503, 504)
- Неверные параметры запроса (400)

**Пример ошибки:**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "api_error",
        "message": "Invalid API key",
        "details": {"endpoint": "/api/v2/account/whoami"},
        "http_status": 401
    },
    "http_status": 401,
    "retry_count": 0
}
```

**Пример обработки:**
```python
async def get_balance():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()
        
        if not response.success:
            if response.error and response.error.code == "api_error":
                status = response.error.http_status
                
                if status == 401:
                    print("🔐 Ошибка аутентификации: проверьте API-ключи")
                elif status == 403:
                    print("🚫 Доступ запрещён: проверьте права API-ключа")
                elif status == 404:
                    print("📭 Ресурс не найден")
                elif status == 429:
                    print("⏳ Слишком много запросов: подождите и повторите")
                elif status and status >= 500:
                    print(f"🔧 Ошибка сервера MRR (HTTP {status}): повторите позже")
                else:
                    print(f"❌ API ошибка (HTTP {status}): {response.error.message}")
                return
            
            print(f"❌ Ошибка: {response.error}")
            return
        
        print(f"✅ Баланс: {response.data}")
```

---

### 4. Validation Error (`"validation_error"`)

**Описание:** Ошибка валидации Pydantic при парсинге ответа API.

**Причины:**
- API вернул неожиданный формат данных
- Отсутствуют обязательные поля
- Несоответствие типов данных

**Пример ошибки:**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "validation_error",
        "message": "Validation error: field 'username' required but not found",
        "details": {"errors": [{"loc": ("username",), "msg": "field required"}]},
        "http_status": 200
    },
    "http_status": 200,
    "retry_count": 0
}
```

**Пример обработки:**
```python
async def get_rigs():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.rig.get_mining_rigs(type="gpu")
        
        if not response.success:
            if response.error and response.error.code == "validation_error":
                print("🔧 Ошибка валидации: API вернул неожиданный формат данных")
                print(f"   {response.error.message}")
                print("   Возможно, API MRR изменил формат ответа")
                return
            
            print(f"❌ Ошибка: {response.error}")
            return
        
        print(f"✅ Найдено ригов: {len(response.data)}")
```

---

## Паттерн обработки результата

Рекомендуемый паттерн обработки ответов во всех примерах:

```python
from aio_mrr import MRRClient

async def main():
    async with MRRClient(api_key="...", api_secret="...") as client:
        # 1. Вызов метода
        response = await client.account.get_balance()
        
        # 2. Проверка успеха
        if not response.success:
            # 3. Обработка ошибки
            print(f"Ошибка: {response.error}")
            return
        
        # 4. Работа с данными
        print(f"Баланс: {response.data}")
```

### Универсальный обработчик ошибок

```python
from aio_mrr import MRRClient, MRRResponse

def handle_error(response: MRRResponse) -> bool:
    """
    Универсальная обработка ошибки.
    Возвращает True если ошибка обработана, False если нужно пробросить дальше.
    """
    if response.success:
        return True
    
    if response.error:
        error = response.error
        
        # Сетевые ошибки
        if error.code == "network_error":
            print(f"❌ Сеть: {error.message}")
            return True
        
        # Таймауты
        if error.code == "timeout":
            print(f"⏱️ Таймаут: {error.message}")
            return True
        
        # API ошибки
        if error.code == "api_error":
            status = error.http_status
            if status == 401:
                print("🔐 Неверный API-ключ")
            elif status == 429:
                print(f"⏳ Rate limit (HTTP {status}): retry_count={response.retry_count}")
            elif status and status >= 500:
                print(f"🔧 Сервер MRR (HTTP {status}): retry_count={response.retry_count}")
            else:
                print(f"❌ API ошибка (HTTP {status}): {error.message}")
            return True
        
        # Валидация
        if error.code == "validation_error":
            print(f"🔧 Валидация: {error.message}")
            return True
    
    # Неизвестная ошибка
    print(f"❌ Неизвестная ошибка: {response.error}")
    return False

async def main():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()
        
        if not handle_error(response):
            return
        
        print(f"✅ Баланс: {response.data}")
```

---

## Retry-стратегия HTTP-клиента

Библиотека автоматически повторяет запросы при временных ошибках. Стратегия retry зависит от типа ошибки:

### Retry-политика

| Тип ошибки | Коды | Кол-во попыток | Backoff | Jitter |
|------------|------|----------------|---------|--------|
| Rate limit (429) | 429 | 5 | 5-60s (exponential) | ✅ Да |
| Server errors | 500, 502, 503, 504 | 3 | 1-8s (exponential) | ✅ Да |
| Connection errors | DNS, connection refused | 3 | 1-8s (exponential) | ✅ Да |
| Timeout | aiohttp.ServerTimeoutError | 3 | 1-8s (exponential) | ✅ Да |
| API errors (4xx) | 400, 401, 403, 404 и др. | 0 | — | — |

### Exponential Backoff + Jitter

**Exponential backoff:** Время ожидания увеличивается экспоненциально между попытками.

**Jitter:** Случайная добавка к времени ожидания для предотвращения "thundering herd".

#### Пример для 429 (Rate Limit):
```
Попытка 1: 0s (первый запрос)
Попытка 2: ~5s  (5 + jitter)
Попытка 3: ~10s (10 + jitter)
Попытка 4: ~20s (20 + jitter)
Попытка 5: ~40s (40 + jitter)
Попытка 6: ~60s (60 + jitter) — макс. время
```

#### Пример для 500/Connection errors:
```
Попытка 1: 0s (первый запрос)
Попытка 2: ~1s  (1 + jitter)
Попытка 3: ~2s  (2 + jitter)
Попытка 4: ~4s  (4 + jitter)
Попытка 5: ~8s  (8 + jitter) — макс. время
```

### Проверка retry в ответе

```python
async def check_retry():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()
        
        if not response.success:
            if response.error and response.error.code == "api_error":
                status = response.error.http_status
                
                if status == 429:
                    print(f"⏳ Rate limit! Было выполнено {response.retry_count} повторных попыток")
                    print(f"   Подождите и повторите запрос позже")
                elif status and status >= 500:
                    print(f"🔧 Серверная ошибка (HTTP {status})")
                    print(f"   Попыток retry: {response.retry_count}")
                    if response.retry_count >= 3:
                        print(f"   Достигнут максимум попыток — подождите и повторите позже")
```

---

## Примеры кода

### Полный пример обработки всех типов ошибок

Пример демонстрирует:
- Обработку `network_error`
- Обработку `timeout`
- Обработку `api_error` (401, 429, 500)
- Обработку `validation_error`
- Проверку `retry_count` при повторных попытках

---

## Ссылки

- [« На главную](./index.md)

- [Аутентификация](./authentication.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

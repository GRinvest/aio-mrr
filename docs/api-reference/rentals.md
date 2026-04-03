# RentalClient — Справочник API

Справочник всех методов `RentalClient` для работы с арендами майнинг-установок на MiningRigRentals: создание аренд, управление пулами, продление, получение статистики, графических данных и логов.

## Обзор

`RentalClient` предоставляет методы для:
- Получения списка аренд с фильтрацией
- Создания и управления арендами
- Применения профилей пулов к арендам
- Управления пулами аренд
- Продления аренды
- Получения графических данных, логов и сообщений

---

## Методы

### 1. `get_list(params)`

Получает список аренд с возможностью фильтрации и пагинации.

**Сигнатура:**
```python
async def get_list(params: dict[str, Any] | None = None) -> MRRResponse[list[RentalInfo]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `params` | `dict[str, Any] \| None` | Нет | Query параметры для фильтрации. По умолчанию возвращает все аренды. |

**Параметры фильтрации:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `type` | `str \| None` | Нет | `'owner'` или `'renter'` — фильтр по роли |
| `algo` | `str \| None` | Нет | Фильтр по алгоритму майнинга |
| `history` | `bool \| None` | Нет | `true` = завершённые аренды, `false` = активные |
| `rig` | `int \| None` | Нет | Фильтр по rig ID |
| `start` | `int \| None` | Нет | Старт пагинации (по умолчанию 0) |
| `limit` | `int \| None` | Нет | Лимит записей (по умолчанию 100) |
| `currency` | `str \| None` | Нет | Валюта оплаты: `BTC`, `LTC`, `ETH`, `DOGE`, `BCH` |

**Возвращает:**
- `MRRResponse[list[RentalInfo]]` — ответ со списком аренд
  - При успехе: `MRRResponse(success=True, data=[RentalInfo, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `RentalInfo`:**
- `id` — идентификатор аренды
- `rig_id` — идентификатор рига
- `rig_name` — название рига (опционально)
- `owner` — владелец рига
- `renter` — арендатор
- `status` — статус аренды
- `started` — время начала
- `ends` — время окончания
- `length` — длительность в часах
- `currency` — валюта оплаты
- `rate` — информация о ставке (`RateInfo`)
- `hash` — информация о хешрейте (`RentalHashInfo`)
- `cost` — стоимость аренды (`RentalCostInfo`)

**Пример использования:**
```python
# Получить активные аренды как арендатор
response = await client.rental.get_list(params={"type": "renter", "history": False})
if response.success:
    for rental in response.data:
        print(f"Rental {rental.id}: {rental.status}, ends: {rental.ends}")
else:
    print(f"Error: {response.error.message}")

# Получить завершённые аренды с пагинацией
response = await client.rental.get_list(params={"type": "owner", "history": True, "start": 0, "limit": 10})
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 2. `get_by_ids(ids)`

Получает информацию об аренде по ID.

**Сигнатура:**
```python
async def get_by_ids(ids: list[int]) -> MRRResponse[RentalInfo]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для получения (используется первый ID) |

**Возвращает:**
- `MRRResponse[RentalInfo]` — ответ с информацией об аренде
  - При успехе: `MRRResponse(success=True, data=RentalInfo)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! note
    Если передан список из нескольких ID, используется только первый ID для получения информации об аренде.

**Пример использования:**
```python
response = await client.rental.get_by_ids(ids=[54321])
if response.success:
    rental = response.data
    print(f"Rental ID: {rental.id}")
    print(f"Rig ID: {rental.rig_id}")
    print(f"Status: {rental.status}")
    print(f"Owner: {rental.owner}")
    print(f"Renter: {rental.renter}")
    print(f"Currency: {rental.currency}")
    print(f"Length: {rental.length} hours")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 3. `create(body)`

Создаёт новую аренду.

**Сигнатура:**
```python
async def create(body: RentalCreateBody) -> MRRResponse[dict[str, Any]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `body` | `RentalCreateBody` | Да | Тело запроса с параметрами создания аренды |

**Параметры `RentalCreateBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `rig` | `int` | Да | ID рига для аренды |
| `length` | `float` | Да | Длительность аренды в часах |
| `profile` | `int` | Да | ID профиля пула для использования |
| `currency` | `str \| None` | Нет | Валюта оплаты (по умолчанию `BTC`) |
| `rate_type` | `str \| None` | Нет | Тип хеша (по умолчанию `'mh'`) |
| `rate_price` | `float \| None` | Нет | Цена за единицу хеша в день |

**Возвращает:**
- `MRRResponse[dict[str, Any]]` — ответ с ID созданной аренды и стоимостью
  - При успехе: `MRRResponse(success=True, data={"id": "54321", "cost": "0.02000000"})`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Пример использования:**
```python
from aio_mrr.models.rental.request import RentalCreateBody

body = RentalCreateBody(
    rig=12345,
    length=24.0,
    profile=678,
    currency="BTC",
    rate_type="mh",
    rate_price=0.005
)
response = await client.rental.create(body)
if response.success:
    print(f"Rental created with ID: {response.data['id']}")
    print(f"Cost: {response.data['cost']}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 4. `update_profile(ids, profile)`

Применяет профиль пула к арендам.

**Сигнатура:**
```python
async def update_profile(ids: list[int], profile: int) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для обновления |
| `profile` | `int` | Да | ID профиля для применения |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! note
    Профиль пула определяет набор пулов с приоритетами, которые будут использоваться для майнинга на аренде.

**Пример использования:**
```python
# Применить профиль к одной аренде
response = await client.rental.update_profile(ids=[54321], profile=678)
if response.success:
    print("Profile applied successfully")
else:
    print(f"Error: {response.error.message}")

# Применить профиль к нескольким арендам
response = await client.rental.update_profile(ids=[54321, 54322, 54323], profile=678)
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 5. `get_pools(ids)`

Получает пулы, назначенные арендам.

**Сигнатура:**
```python
async def get_pools(ids: list[int]) -> MRRResponse[list[Pool]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для получения пулов |

**Возвращает:**
- `MRRResponse[list[Pool]]` — ответ со списком пулов
  - При успехе: `MRRResponse(success=True, data=[Pool, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `Pool`:**
- `id` — идентификатор пула
- `type` — алгоритм (sha256, scrypt, x11 и т.д.)
- `name` — название пула
- `host` — хост пула
- `port` — порт пула
- `user` — имя пользователя/worker
- `password` — пароль
- `notes` — заметки (опционально)
- `algo` — информация об алгоритме (опционально)

**Пример использования:**
```python
response = await client.rental.get_pools(ids=[54321])
if response.success:
    for pool in response.data:
        print(f"Pool: {pool.name}")
        print(f"  Type: {pool.type}")
        print(f"  Host: {pool.host}:{pool.port}")
        print(f"  User: {pool.user}")
        if pool.notes:
            print(f"  Notes: {pool.notes}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 6. `update_pool(ids, body)`

Добавляет или заменяет пул на арендах.

**Сигнатура:**
```python
async def update_pool(ids: list[int], body: RentalPoolBody) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для обновления |
| `body` | `RentalPoolBody` | Да | Тело запроса с данными пула |

**Параметры `RentalPoolBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `host` | `str` | Да | Хост пула |
| `port` | `int` | Да | Порт пула |
| `user` | `str` | Да | Имя worker |
| `password` | `str` | Да | Пароль worker |
| `priority` | `int \| None` | Нет | Приоритет пула (0-4) |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! note
    Если пул с таким приоритетом уже существует, он будет заменён. Приоритет 0 имеет наивысшее значение.

**Пример использования:**
```python
from aio_mrr.models.rental.request import RentalPoolBody

body = RentalPoolBody(
    host="pool.example.com",
    port=3333,
    user="worker1",
    password="password",
    priority=0
)
response = await client.rental.update_pool(ids=[54321], body=body)
if response.success:
    print("Pool updated successfully")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 7. `delete_pool(ids)`

Удаляет пул с аренд.

**Сигнатура:**
```python
async def delete_pool(ids: list[int]) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для удаления пула |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! warning
    Удаление пула может привести к остановке майнинга, если не назначен пул с другим приоритетом.

**Пример использования:**
```python
response = await client.rental.delete_pool(ids=[54321])
if response.success:
    print("Pool deleted successfully")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 8. `extend(ids, length, getcost)`

Покупает продление аренды.

**Сигнатура:**
```python
async def extend(ids: list[int], length: float, getcost: bool | None = None) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для продления |
| `length` | `float` | Да | Часы для продления |
| `getcost` | `bool \| None` | Нет | Если `True`, симулирует продление и возвращает стоимость без фактического списания |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! tip
    Используйте `getcost=True` для предварительного расчёта стоимости продления перед фактическим продлением.

**Пример использования:**
```python
# Продление аренды
response = await client.rental.extend(ids=[54321], length=12.0)
if response.success:
    print("Rental extended successfully")
else:
    print(f"Error: {response.error.message}")

# Симуляция стоимости продления
response = await client.rental.extend(ids=[54321], length=12.0, getcost=True)
if response.success:
    print("Cost simulation completed")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 9. `get_graph(ids, hours, interval)`

Получает графические данные аренды (исторический хешрейт, простои).

**Сигнатура:**
```python
async def get_graph(ids: list[int], hours: float | None = None, interval: str | None = None) -> MRRResponse[GraphData]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд (используется первый ID) |
| `hours` | `float \| None` | Нет | Часы данных (максимум 2 недели = 336 часов). По умолчанию 168 (7 дней). |
| `interval` | `str \| None` | Нет | Интервал данных. По умолчанию `None`. |

**Возвращает:**
- `MRRResponse[GraphData]` — ответ с графическими данными
  - При успехе: `MRRResponse(success=True, data=GraphData)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `GraphData`:**
- `hashrate_data` — список точек данных хешрейта (`list[GraphDataPoint] | None`)
- `downtime_data` — список точек данных простоев (`list[GraphDataPoint] | None`)
- `hours` — количество часов данных (`float | None`)

**Что содержит `GraphDataPoint`:**
- `time` — временная метка (`str | None`)
- `hashrate` — значение хешрейта (`float | None`)
- `downtime` — статус простоя (`bool | None`)

**Пример использования:**
```python
# Получить последние 24 часа данных
response = await client.rental.get_graph(ids=[54321], hours=24)
if response.success:
    graph = response.data
    print(f"Hours of data: {graph.hours}")
    print(f"Hashrate points: {len(graph.hashrate_data or [])}")
    print(f"Downtime points: {len(graph.downtime_data or [])}")
    
    # Вывод последних 5 точек хешрейта
    for point in (graph.hashrate_data or [])[-5:]:
        print(f"  {point.time}: {point.hashrate}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 10. `get_log(ids)`

Получает журнал активности аренды.

**Сигнатура:**
```python
async def get_log(ids: list[int]) -> MRRResponse[list[RentalLogEntry]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для получения логов (используется первый ID) |

**Возвращает:**
- `MRRResponse[list[RentalLogEntry]]` — ответ со списком записей лога
  - При успехе: `MRRResponse(success=True, data=[RentalLogEntry, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `RentalLogEntry`:**
- `time` — временная метка записи
- `message` — сообщение события

**Пример использования:**
```python
response = await client.rental.get_log(ids=[54321])
if response.success:
    for log_entry in response.data:
        print(f"{log_entry.time}: {log_entry.message}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 11. `get_message(ids)`

Получает сообщения аренды.

**Сигнатура:**
```python
async def get_message(ids: list[int]) -> MRRResponse[list[RentalMessage]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для получения сообщений (используется первый ID) |

**Возвращает:**
- `MRRResponse[list[RentalMessage]]` — ответ со списком сообщений
  - При успехе: `MRRResponse(success=True, data=[RentalMessage, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `RentalMessage`:**
- `time` — временная метка сообщения
- `user` — имя пользователя, отправившего сообщение
- `message` — текст сообщения

**Пример использования:**
```python
response = await client.rental.get_message(ids=[54321])
if response.success:
    for msg in response.data:
        print(f"{msg.time} [{msg.user}]: {msg.message}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 12. `send_message(ids, message)`

Отправляет сообщение аренде.

**Сигнатура:**
```python
async def send_message(ids: list[int], message: str) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список ID аренд для отправки сообщения (используется первый ID) |
| `message` | `str` | Да | Текст сообщения |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! note
    Сообщения видны как владельцу рига, так и арендатору. Используйте их для коммуникации по поводу аренды.

**Пример использования:**
```python
response = await client.rental.send_message(
    ids=[54321],
    message="Please check the rig status. Hashrate is lower than expected."
)
if response.success:
    print("Message sent successfully")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

## Сводная таблица методов

| # | Метод | Описание | Возвращает | Пример |
|---|-------|----------|------------|--------|
| 1 | `get_list(params)` | Список аренд | `MRRResponse[list[RentalInfo]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 2 | `get_by_ids(ids)` | Аренда по ID | `MRRResponse[RentalInfo]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 3 | `create(body)` | Создать аренду | `MRRResponse[dict[str, Any]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 4 | `update_profile(ids, profile)` | Применить профиль | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 5 | `get_pools(ids)` | Пулы аренд | `MRRResponse[list[Pool]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 6 | `update_pool(ids, body)` | Обновить пул | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 7 | `delete_pool(ids)` | Удалить пул | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 8 | `extend(ids, length, getcost)` | Продлить аренду | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 9 | `get_graph(ids, hours, interval)` | График хешрейта | `MRRResponse[GraphData]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 10 | `get_log(ids)` | Лог аренды | `MRRResponse[list[RentalLogEntry]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 11 | `get_message(ids)` | Сообщения аренды | `MRRResponse[list[RentalMessage]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 12 | `send_message(ids, message)` | Отправить сообщение | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |

---

## Дополнительные ресурсы

- [Главная страница](../../index.md)
- [Обработка ошибок](../error-handling.md)
- [Модели данных](../models.md)
- [Аутентификация](../authentication.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

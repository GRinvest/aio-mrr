# AccountClient — Справочник API

Справочник всех методов `AccountClient` для работы с аккаунтом MiningRigRentals: управление балансом, транзакциями, профилями пулов, сохранёнными пулами и статусами валют.

## Обзор

`AccountClient` предоставляет методы для:
- Получения информации об аккаунте и балансах
- Просмотра истории транзакций
- CRUD операций с профилями пулов
- CRUD операций с сохранёнными пулами
- Тестирования подключения к пулам
- Просмотра статусов валют

---

## Методы

### 1. `get_account()`

Получает детальную информацию об аккаунте пользователя.

**Сигнатура:**
```python
async def get_account(self) -> MRRResponse[AccountInfo]
```

**Возвращает:**
- `MRRResponse[AccountInfo]` — ответ с информацией об аккаунте
  - При успехе: `MRRResponse(success=True, data=AccountInfo)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `AccountInfo`:**
- `username` — имя пользователя
- `email` — email адрес
- `withdraw` — адреса для вывода средств по валютам
- `deposit` — адреса для депозитов по валютам
- `notifications` — настройки уведомлений
- `settings` — настройки аккаунта

**Пример использования:**
```python
response = await client.account.get_account()
if response.success:
    print(f"Username: {response.data.username}")
    print(f"Email: {response.data.email}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

### 2. `get_balance()`

Получает балансы аккаунта по всем валютам.

**Сигнатура:**
```python
async def get_balance(self) -> MRRResponse[dict[str, BalanceInfo]]
```

**Возвращает:**
- `MRRResponse[dict[str, BalanceInfo]]` — ответ с балансами по валютам
  - При успехе: `MRRResponse(success=True, data={"BTC": BalanceInfo, "LTC": BalanceInfo, ...})`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `BalanceInfo`:**
- `confirmed` — подтверждённый баланс (строка)
- `pending` — ожидающий баланс (float)
- `unconfirmed` — неподтверждённый баланс (строка)

!!! note
    Балансы обновляются в реальном времени при поступлениях средств.

**Пример использования:**
```python
response = await client.account.get_balance()
if response.success:
    for currency, balance in response.data.items():
        print(f"{currency}: confirmed={balance.confirmed}, pending={balance.pending}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/01_quickstart.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/01_quickstart.py)

---

### 3. `get_transactions()`

Получает историю транзакций аккаунта с возможностью фильтрации.

**Сигнатура:**
```python
async def get_transactions(params: TransactionsQueryParams | None = None) -> MRRResponse[TransactionsList]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `params` | `TransactionsQueryParams \| None` | Нет | Параметры фильтрации. По умолчанию возвращает все транзакции (limit=100). |

**Параметры `TransactionsQueryParams`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `start` | `int \| None` | Нет | Старт пагинации (по умолчанию 0) |
| `limit` | `int \| None` | Нет | Лимит записей (по умолчанию 100) |
| `algo` | `str \| None` | Нет | Фильтр по алгоритму |
| `type` | `str \| None` | Нет | Тип транзакции (credit, payout, referral, deposit, payment, credit/refund, debit/refund, rental fee) |
| `rig` | `int \| None` | Нет | Фильтр по rig ID |
| `rental` | `int \| None` | Нет | Фильтр по rental ID |
| `txid` | `str \| None` | Нет | Фильтр по txid |
| `time_greater_eq` | `str \| None` | Нет | Время >= (Unix timestamp) |
| `time_less_eq` | `str \| None` | Нет | Время <= (Unix timestamp) |

**Возвращает:**
- `MRRResponse[TransactionsList]` — ответ со списком транзакций
  - При успехе: `MRRResponse(success=True, data=TransactionsList)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `TransactionsList`:**
- `total` — общее количество транзакций (строка)
- `returned` — количество возвращённых записей
- `start` — стартовая позиция
- `limit` — лимит записей
- `transactions` — список `Transaction` объектов

**Пример использования:**
```python
# Получить последние 10 кредитов
params = TransactionsQueryParams(type="credit", limit=10)
response = await client.account.get_transactions(params)
if response.success:
    for tx in response.data.transactions:
        print(f"{tx.type}: {tx.amount} ({tx.when})")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

### 4. `get_profiles()`

Получает список всех профилей пулов или фильтрует по алгоритму.

**Сигнатура:**
```python
async def get_profiles(algo: str | None = None) -> MRRResponse[list[Profile]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `algo` | `str \| None` | Нет | Фильтр по алгоритму (например, "scrypt", "sha256"). По умолчанию возвращает все профили. |

**Возвращает:**
- `MRRResponse[list[Profile]]` — ответ со списком профилей
  - При успехе: `MRRResponse(success=True, data=[Profile, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `Profile`:**
- `id` — идентификатор профиля
- `name` — название профиля
- `algo` — информация об алгоритме (`AlgoProfileInfo`)
- `pools` — список пулов (`list[PoolProfileInfo]`) с приоритетами

**Пример использования:**
```python
# Получить все профили
response = await client.account.get_profiles()
if response.success:
    for profile in response.data:
        print(f"{profile.name}: {len(profile.pools)} пулов")
        for pool in profile.pools:
            print(f"  - {pool.host}:{pool.port} (priority {pool.priority})")

# Получить профили только для scrypt
response = await client.account.get_profiles(algo="scrypt")
```

**Ссылка на пример:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 5. `create_profile()`

Создаёт новый профиль пула для указанного алгоритма.

**Сигнатура:**
```python
async def create_profile(body: ProfileCreateBody) -> MRRResponse[ProfileCreateResponse]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `body` | `ProfileCreateBody` | Да | Тело запроса с названием и алгоритмом профиля |

**Параметры `ProfileCreateBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `name` | `str` | Да | Название профиля |
| `algo` | `str` | Да | Алгоритм профиля (например, "scrypt", "sha256") |

**Возвращает:**
- `MRRResponse[ProfileCreateResponse]` — ответ с ID созданного профиля
  - При успехе: `MRRResponse(success=True, data=ProfileCreateResponse)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `ProfileCreateResponse`:**
- `pid` — идентификатор созданного профиля (строка)

**Пример использования:**
```python
body = ProfileCreateBody(name="My Scrypt Profile", algo="scrypt")
response = await client.account.create_profile(body)
if response.success:
    print(f"Profile created with ID: {response.data.pid}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 6. `get_profile()`

Получает конкретный профиль пула по ID.

**Сигнатура:**
```python
async def get_profile(pid: int) -> MRRResponse[Profile]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `pid` | `int` | Да | Идентификатор профиля |

**Возвращает:**
- `MRRResponse[Profile]` — ответ с информацией о профиле
  - При успехе: `MRRResponse(success=True, data=Profile)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Пример использования:**
```python
response = await client.account.get_profile(pid=40073)
if response.success:
    profile = response.data
    print(f"Profile: {profile.name}")
    print(f"Algorithm: {profile.algo.display}")
    for pool in profile.pools:
        print(f"  - {pool.host}:{pool.port} (priority {pool.priority}, status {pool.status})")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 7. `update_profile()`

Добавляет или заменяет пул в профиле с указанием приоритета.

**Сигнатура:**
```python
async def update_profile(pid: int, poolid: int, priority: int | None = None) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `pid` | `int` | Да | Идентификатор профиля |
| `poolid` | `int` | Да | Идентификатор пула для добавления |
| `priority` | `int \| None` | Нет | Приоритет пула (0-4). Если не указан, пул добавляется на первый доступный приоритет. |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! note
    Приоритет 0 имеет наивысшее значение. Пулы с более низкими номерами приоритетов обрабатываются первыми.

**Пример использования:**
```python
# Добавить пул на приоритет 0
response = await client.account.update_profile(pid=40073, poolid=98708, priority=0)
if response.success:
    print("Pool added to profile at priority 0")
else:
    print(f"Error: {response.error.message}")

# Добавить пул без указания приоритета (автовыбор)
response = await client.account.update_profile(pid=40073, poolid=98708)
```

**Ссылка на пример:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 8. `update_profile_priority()`

Добавляет пул на конкретную позицию приоритета в профиле.

**Сигнатура:**
```python
async def update_profile_priority(pid: int, priority: int, poolid: int) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `pid` | `int` | Да | Идентификатор профиля |
| `priority` | `int` | Да | Приоритет пула (0-4) |
| `poolid` | `int` | Да | Идентификатор пула для добавления |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! warning
    Приоритет должен быть в диапазоне 0-4. Значения вне этого диапазона вызовут ошибку API.

**Пример использования:**
```python
response = await client.account.update_profile_priority(pid=41818, priority=0, poolid=98708)
if response.success:
    print("Pool added at priority 0")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 9. `delete_profile()`

Удаляет профиль пула по ID.

**Сигнатура:**
```python
async def delete_profile(pid: int) -> MRRResponse[ProfileDeleteResponse]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `pid` | `int` | Да | Идентификатор профиля для удаления |

**Возвращает:**
- `MRRResponse[ProfileDeleteResponse]` — ответ о результате удаления
  - При успехе: `MRRResponse(success=True, data=ProfileDeleteResponse)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `ProfileDeleteResponse`:**
- `id` — идентификатор удалённого профиля
- `success` — статус успешности удаления
- `message` — сообщение о результате

**Пример использования:**
```python
response = await client.account.delete_profile(pid=42281)
if response.success:
    print(f"Deleted: {response.data.message}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 10. `get_pools()`

Получает список всех сохранённых пулов аккаунта.

**Сигнатура:**
```python
async def get_pools(self) -> MRRResponse[list[Pool]]
```

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
response = await client.account.get_pools()
if response.success:
    for pool in response.data:
        print(f"{pool.name}: {pool.type}://{pool.host}:{pool.port}")
        if pool.notes:
            print(f"  Notes: {pool.notes}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 11. `get_pools_by_ids()`

Получает конкретные пулы по списку их идентификаторов.

**Сигнатура:**
```python
async def get_pools_by_ids(ids: list[int]) -> MRRResponse[list[Pool]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список идентификаторов пулов |

**Возвращает:**
- `MRRResponse[list[Pool]]` — ответ со списком пулов
  - При успехе: `MRRResponse(success=True, data=[Pool, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! note
    Пулы разделяются точкой с запятой в URL запроса (`/account/pool/12345;12346`).

**Пример использования:**
```python
response = await client.account.get_pools_by_ids(ids=[12345, 12346])
if response.success:
    for pool in response.data:
        print(f"ID: {pool.id}, Type: {pool.type}, Name: {pool.name}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 12. `create_pool()`

Создаёт новый сохранённый пул.

**Сигнатура:**
```python
async def create_pool(body: PoolCreateBody) -> MRRResponse[PoolCreateResponse]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `body` | `PoolCreateBody` | Да | Тело запроса с параметрами пула |

**Параметры `PoolCreateBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `type` | `str` | Да | Алгоритм пула (sha256, scrypt, x11 и т.д.) |
| `name` | `str` | Да | Название для идентификации пула |
| `host` | `str` | Да | Хост пула |
| `port` | `int` | Да | Порт пула |
| `user` | `str` | Да | Имя worker |
| `password` | `str \| None` | Нет | Пароль worker |
| `notes` | `str \| None` | Нет | Заметки к пулу |

**Возвращает:**
- `MRRResponse[PoolCreateResponse]` — ответ с ID созданного пула
  - При успехе: `MRRResponse(success=True, data=PoolCreateResponse)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `PoolCreateResponse`:**
- `id` — идентификатор созданного пула (int)

**Пример использования:**
```python
body = PoolCreateBody(
    type="scrypt",
    name="My Primary Pool",
    host="pool.example.com",
    port=3333,
    user="worker1",
    password="pass123",
    notes="Main pool for scrypt mining"
)
response = await client.account.create_pool(body)
if response.success:
    print(f"Pool created with ID: {response.data.id}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 13. `update_pools()`

Обновляет параметры существующих пулов по списку их идентификаторов.

**Сигнатура:**
```python
async def update_pools(ids: list[int], body: dict[str, Any]) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список идентификаторов пулов для обновления |
| `body` | `dict[str, Any]` | Да | Тело запроса с новыми параметрами пулов |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Допустимые поля в `body`:**
- `name` — новое название пула
- `host` — новый хост
- `port` — новый порт
- `user` — новое имя пользователя
- `password` — новый пароль
- `notes` — новые заметки

!!! note
    Можно обновить только нужные поля. Не указанные поля останутся без изменений.

**Пример использования:**
```python
# Обновить название и хост
body = {"name": "Updated Pool Name", "host": "new.pool.com"}
response = await client.account.update_pools(ids=[12345], body=body)
if response.success:
    print("Pool updated")
else:
    print(f"Error: {response.error.message}")

# Пакетное обновление нескольких пулов
response = await client.account.update_pools(ids=[12345, 12346], body={"notes": "Updated notes"})
```

**Ссылка на пример:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 14. `delete_pools()`

Удаляет сохранённые пулы по списку их идентификаторов.

**Сигнатура:**
```python
async def delete_pools(ids: list[int]) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `ids` | `list[int]` | Да | Список идентификаторов пулов для удаления |

**Возвращает:**
- `MRRResponse[None]` — ответ о результате
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! warning
    Удаление пулов необратимо. Убедитесь, что пулы не используются в активных профилях или арендах.

**Пример использования:**
```python
response = await client.account.delete_pools(ids=[12345, 12346])
if response.success:
    print("Pools deleted successfully")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 15. `test_pool()`

Тестирует подключение к пулу с разных серверов MRR.

**Сигнатура:**
```python
async def test_pool(body: PoolTestBody) -> MRRResponse[PoolTestResult]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `body` | `PoolTestBody` | Да | Тело запроса с параметрами теста |

**Параметры `PoolTestBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `method` | `str` | Да | Метод теста: `"simple"` (только подключение) или `"full"` (с аутентификацией) |
| `extramethod` | `str \| None` | Нет | Для ethhash: `[esm0,esm1,esm2,esm3]`. По умолчанию `esm0`. |
| `type` | `str \| None` | Нет | Алгоритм (scrypt, sha256, x11). Требуется для `full` метода. |
| `host` | `str \| None` | Нет | Хост пула (может включать порт) |
| `port` | `int \| None` | Нет | Порт пула. Требуется если нет в `host`. |
| `user` | `str \| None` | Нет | Имя пользователя. Требуется для `full` метода. |
| `password` | `str \| None` | Нет | Пароль. Требуется для `full` метода. |
| `source` | `str \| None` | Нет | Сервер MRR для теста. По умолчанию `us-central01`. |

**Возвращает:**
- `MRRResponse[PoolTestResult]` — ответ с результатами тестов
  - При успехе: `MRRResponse(success=True, data=PoolTestResult)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `PoolTestResult`:**
- `result` — список `PoolTestResultItem` с результатами тестов с разных серверов
- `error` — список ошибок (если есть)

**Что содержит `PoolTestResultItem`:**
- `source` — сервер MRR, с которого проводился тест
- `dest` — адрес пула (host:port)
- `error` — описание ошибки (пустая строка при успехе)
- `connection` — успешно ли подключение
- `executiontime` — время выполнения теста (секунды)
- `protocol` — протокол (stratum и т.д.)
- `sub` — успешно ли подписка
- `auth` — успешно ли аутентификация
- `diff` — полученная сложность
- `xnonce` — поддержка xnonce
- `ssl` — использование SSL

!!! note
    - **Simple тест**: проверяет только подключение к порту пула.
    - **Full тест**: проверяет подключение, подписку, аутентификацию и получение работы.

**Пример использования:**
```python
# Простой тест (только подключение)
body = PoolTestBody(method="simple", host="de.minexmr.com:4444")
response = await client.account.test_pool(body)
if response.success:
    for item in response.data.result:
        status = "OK" if item.connection else f"FAILED: {item.error}"
        print(f"{item.source} -> {item.dest}: {status} ({item.executiontime}s)")

# Полный тест (с аутентификацией)
body = PoolTestBody(
    method="full",
    type="cryptonote",
    host="de.minexmr.com",
    port=4444,
    user="test",
    password="x"
)
response = await client.account.test_pool(body)
if response.success:
    result = response.data.result[0]
    print(f"Connection: {result.connection}")
    print(f"Auth: {result.auth}")
    print(f"Work: {result.work}")
    print(f"Diff: {result.diff}")
```

**Ссылка на пример:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 16. `get_currencies()`

Получает список валют с статусом включённости для аккаунта.

**Сигнатура:**
```python
async def get_currencies(self) -> MRRResponse[list[CurrencyStatus]]
```

**Возвращает:**
- `MRRResponse[list[CurrencyStatus]]` — ответ со списком валют
  - При успехе: `MRRResponse(success=True, data=[CurrencyStatus, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `CurrencyStatus`:**
- `name` — название валюты (BTC, LTC, ETH, DOGE, BCH)
- `enabled` — статус включённости для аккаунта

**Пример использования:**
```python
response = await client.account.get_currencies()
if response.success:
    print("Available currencies:")
    for currency in response.data:
        status = "enabled" if currency.enabled else "disabled"
        print(f"  - {currency.name}: {status}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

## Сводная таблица методов

| # | Метод | Описание | Возвращает | Пример |
|---|-------|----------|------------|--------|
| 1 | `get_account()` | Информация об аккаунте | `MRRResponse[AccountInfo]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |
| 2 | `get_balance()` | Балансы по валютам | `MRRResponse[dict[str, BalanceInfo]]` | [01_quickstart.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/01_quickstart.py) |
| 3 | `get_transactions(params)` | История транзакций | `MRRResponse[TransactionsList]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |
| 4 | `get_profiles(algo)` | Все профили пулов | `MRRResponse[list[Profile]]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 5 | `create_profile(body)` | Создать профиль | `MRRResponse[ProfileCreateResponse]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 6 | `get_profile(pid)` | Профиль по ID | `MRRResponse[Profile]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 7 | `update_profile(pid, poolid, priority)` | Добавить/заменить пул в профиле | `MRRResponse[None]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 8 | `update_profile_priority(pid, priority, poolid)` | Установить приоритет пула | `MRRResponse[None]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 9 | `delete_profile(pid)` | Удалить профиль | `MRRResponse[ProfileDeleteResponse]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 10 | `get_pools()` | Все сохранённые пулы | `MRRResponse[list[Pool]]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 11 | `get_pools_by_ids(ids)` | Пулы по ID | `MRRResponse[list[Pool]]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 12 | `create_pool(body)` | Создать пул | `MRRResponse[PoolCreateResponse]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 13 | `update_pools(ids, body)` | Обновить пулы | `MRRResponse[None]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 14 | `delete_pools(ids)` | Удалить пулы | `MRRResponse[None]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 15 | `test_pool(body)` | Тест пула | `MRRResponse[PoolTestResult]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 16 | `get_currencies()` | Статусы валют | `MRRResponse[list[CurrencyStatus]]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |

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

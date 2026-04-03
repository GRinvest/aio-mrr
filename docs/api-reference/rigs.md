# Справочник RigClient

Этот справочник содержит полную документацию всех 15 методов `RigClient` для работы с майнинг-ригами (rigs).

> **Навигация:** [« На главную](../../index.md)

---

## Содержание

1. [Поиск ригов](#search_rigs)
2. [Получение своих ригов](#get_mining_rigs)
3. [Получение ригов по ID](#get_rigs)
4. [Создание рига](#create_rig)
5. [Пакетное обновление ригов](#batch_update_rigs)
6. [Удаление ригов](#delete_rigs)
7. [Продление ригов](#extend_rigs)
8. [Пакетное продление ригов](#batch_extend_rigs)
9. [Применение профиля к ригам](#update_rig_profile)
10. [Получение пулов ригов](#get_rig_pools)
11. [Обновление пула ригов](#update_rig_pool)
12. [Удаление пула ригов](#delete_rig_pool)
13. [Получение порта рига](#get_rig_ports)
14. [Получение тредов ригов](#get_rig_threads)
15. [Получение графика ригов](#get_rig_graph)

---

## search_rigs

Ищет rig'ы по алгоритму с фильтрацией и сортировкой.

Аналогично основной странице списка rig'ов на сайте MRR.

### Сигнатура

```python
async def search_rigs(
    type: str,
    currency: str | None = None,
    minhours_min: int | None = None,
    minhours_max: int | None = None,
    maxhours_min: int | None = None,
    maxhours_max: int | None = None,
    rpi_min: int | None = None,
    rpi_max: int | None = None,
    hash_min: int | None = None,
    hash_max: int | None = None,
    hash_type: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    price_type: str | None = None,
    offline: bool | None = None,
    rented: bool | None = None,
    region_type: str | None = None,
    expdiff: float | None = None,
    count: int | None = None,
    islive: str | None = None,
    xnonce: str | None = None,
    offset: int | None = None,
    orderby: str | None = None,
    orderdir: str | None = None,
) -> MRRResponse[list[RigInfo]]
```

### Аргументы

#### Обязательный параметр

| Параметр | Тип | Описание |
|----------|-----|----------|
| `type` | `str` | Алгоритм: `sha256`, `scrypt`, `x11`, `kawpow` и т.д. |

#### Параметры ценообразования

| Параметр | Тип | Описание |
|----------|-----|----------|
| `currency` | `str \| None` | Валюта: `BTC`, `LTC`, `ETH`, `DOGE`, `BCH`. По умолчанию `BTC`. |
| `price_min` | `float \| None` | Минимальная цена. |
| `price_max` | `float \| None` | Максимальная цена. |
| `price_type` | `str \| None` | Тип хеша для цены (например, `mh`, `gh`). |

#### Параметры времени

| Параметр | Тип | Описание |
|----------|-----|----------|
| `minhours_min` | `int \| None` | Минимальное количество часов (нижняя граница). |
| `minhours_max` | `int \| None` | Максимальное количество часов (верхняя граница). |
| `maxhours_min` | `int \| None` | Минимальное максимальное время. |
| `maxhours_max` | `int \| None` | Максимальное максимальное время. |

#### Параметры хешрейта

| Параметр | Тип | Описание |
|----------|-----|----------|
| `hash_min` | `int \| None` | Минимальный хешрейт. |
| `hash_max` | `int \| None` | Максимальный хешрейт. |
| `hash_type` | `str \| None` | Тип: `hash`, `kh`, `mh`, `gh`, `th`, `ph`, `eh`. По умолчанию `mh`. |

#### Параметры производительности (RPI)

| Параметр | Тип | Описание |
|----------|-----|----------|
| `rpi_min` | `int \| None` | Минимальный RPI (0-100). |
| `rpi_max` | `int \| None` | Максимальный RPI (0-100). |

#### Статус-фильтры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `offline` | `bool \| None` | Показывать оффлайн rig'и. По умолчанию `false`. |
| `rented` | `bool \| None` | Показывать арендованные rig'и. По умолчанию `false`. |

#### Дополнительные фильтры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `region_type` | `str \| None` | `'include'` или `'exclude'` для фильтрации по региону. |
| `expdiff` | `float \| None` | Ожидаемая сложность worker. |
| `islive` | `str \| None` | Фильтр по rig'ам с хешрейтом (`yes`). |
| `xnonce` | `str \| None` | Фильтр по xnonce (`yes`, `no`). |

#### Параметры пагинации и сортировки

| Параметр | Тип | Описание |
|----------|-----|----------|
| `count` | `int \| None` | Количество результатов (макс. 100). По умолчанию `100`. |
| `offset` | `int \| None` | Смещение пагинации. По умолчанию `0`. |
| `orderby` | `str \| None` | Поле сортировки. По умолчанию `score`. |
| `orderdir` | `str \| None` | Направление сортировки: `asc`, `desc`. По умолчанию `asc`. |

### Возвращаемое значение

`MRRResponse[list[RigInfo]]` — ответ со списком rig'ов:

- **При успехе:** `MRRResponse(success=True, data=[RigInfo, ...])`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def search_available_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        # Поиск ригов с алгоритмом kawpow, цена от 0.001 до 0.01, сортировка по цене
        response = await client.rig.search_rigs(
            type="kawpow",
            price_min=0.001,
            price_max=0.01,
            orderby="price",
            orderdir="asc",
            count=50
        )
        
        if response.success:
            for rig in response.data:
                print(f"{rig.name}: {rig.price}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/08_advanced_search.py`

---

## get_mining_rigs

Получает список ваших rig'ов.

### Сигнатура

```python
async def get_mining_rigs(
    type: str | None = None,
    hashrate: bool | None = None
) -> MRRResponse[list[RigInfo]]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `type` | `str \| None` | Фильтр по алгоритму. |
| `hashrate` | `bool \| None` | Показывать расчёт хешрейта. |

### Возвращаемое значение

`MRRResponse[list[RigInfo]]` — ответ со списком ваших rig'ов:

- **При успехе:** `MRRResponse(success=True, data=[RigInfo, ...])`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def list_my_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_mining_rigs(type="scrypt", hashrate=True)
        
        if response.success:
            print(f"Найдено ригов: {len(response.data)}")
            for rig in response.data:
                print(f"{rig.id}: {rig.name} - {rig.hash}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## get_rigs

Получает один или несколько rig'ов по ID.

### Сигнатура

```python
async def get_rigs(
    ids: list[int],
    fields: list[str] | None = None
) -> MRRResponse[list[RigInfo]]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для получения. Пример: `[12345, 12346]`. |
| `fields` | `list[str] \| None` | Фильтр полей root level (например, `["name", "status"]`). |

### Возвращаемое значение

`MRRResponse[list[RigInfo]]` — ответ со списком rig'ов:

- **При успехе:** `MRRResponse(success=True, data=[RigInfo, ...])`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def get_rigs_by_id():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        # Получить только поля name и status
        response = await client.rig.get_rigs(
            ids=[12345, 12346],
            fields=["name", "status"]
        )
        
        if response.success:
            for rig in response.data:
                print(f"{rig.id}: {rig.name} - {rig.status}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## create_rig

Создаёт новый rig.

### Сигнатура

```python
async def create_rig(
    body: RigCreateBody
) -> MRRResponse[dict[str, Any]]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `body` | `RigCreateBody` | Тело запроса с параметрами создания rig. |

Поля `RigCreateBody`:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `name` | `str` | Да | Название рига. |
| `server` | `str` | Да | Сервер (например, `us-east01.miningrigrentals.com`). |
| `description` | `str \| None` | Нет | Описание рига. |
| `status` | `str \| None` | Нет | Статус рига. |
| `price_btc_enabled` | `bool \| None` | Нет | Включить оплату BTC. |
| `price_btc_price` | `float \| None` | Нет | Цена BTC. |
| `price_btc_autoprice` | `bool \| None` | Нет | Автоцены BTC. |
| `price_btc_minimum` | `float \| None` | Нет | Минимальная цена BTC. |
| `price_type` | `str \| None` | Нет | Тип цены (например, `mh`). |
| `minhours` | `float \| None` | Нет | Минимальное время аренды. |
| `maxhours` | `float \| None` | Нет | Максимальное время аренды. |
| `extensions` | `bool \| None` | Нет | Разрешить продление. |
| `hash_hash` | `float \| None` | Нет | Хешрейт. |
| `hash_type` | `str \| None` | Нет | Тип хешрейта. |
| `suggested_diff` | `float \| None` | Нет | Предложенная сложность. |
| `ndevices` | `int \| None` | Нет | Количество устройств. |

### Возвращаемое значение

`MRRResponse[dict[str, Any]]` — ответ с ID созданного rig:

- **При успехе:** `MRRResponse(success=True, data={"id": 12345})`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient
from aio_mrr.models.rig.request import RigCreateBody

async def create_new_rig():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        body = RigCreateBody(
            name="My Scrypt Rig",
            server="us-east01.miningrigrentals.com",
            price_type="mh",
            minhours=1.0,
            maxhours=24.0,
            extensions=True,
        )
        
        response = await client.rig.create_rig(body)
        
        if response.success:
            print(f"Риг создан с ID: {response.data['id']}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## batch_update_rigs

Обновляет пакет rig'ов.

### Сигнатура

```python
async def batch_update_rigs(
    body: RigBatchBody
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `body` | `RigBatchBody` | Тело запроса со списком rig'ов для обновления. |

Поля `RigBatchBody`:

| Поле | Тип | Описание |
|------|-----|----------|
| `rigs` | `list[dict[str, object]]` | Список словарей с данными ригов для обновления. |

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient
from aio_mrr.models.rig.request import RigBatchBody

async def batch_update():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        body = RigBatchBody(
            rigs=[
                {"id": 12345, "name": "Updated Name 1"},
                {"id": 12346, "name": "Updated Name 2"},
            ]
        )
        
        response = await client.rig.batch_update_rigs(body)
        
        if response.success:
            print("Риги обновлены успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## delete_rigs

Удаляет один или несколько rig'ов по ID.

### Сигнатура

```python
async def delete_rigs(
    ids: list[int]
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для удаления. |

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def delete_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.delete_rigs(ids=[12345, 12346])
        
        if response.success:
            print("Риги удалены успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## extend_rigs

Продлевает аренду rig'а (для владельцев).

### Сигнатура

```python
async def extend_rigs(
    ids: list[int],
    hours: float | None = None,
    minutes: float | None = None
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для продления. |
| `hours` | `float \| None` | Часы для продления. |
| `minutes` | `float \| None` | Минуты для продления. |

!!! note "Примечание"
    Укажите хотя бы один из параметров `hours` или `minutes`.

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def extend_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.extend_rigs(ids=[12345], hours=24)
        
        if response.success:
            print("Риг продлён успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## batch_extend_rigs

Пакетное продление аренды для нескольких rig'ов.

### Сигнатура

```python
async def batch_extend_rigs(
    rig_hours: dict[int, float]
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `rig_hours` | `dict[int, float]` | Словарь `{rig_id: hours}` для продления. |

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def batch_extend():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.batch_extend_rigs({12345: 24, 12346: 48})
        
        if response.success:
            print("Риги продлены успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## update_rig_profile

Применяет профиль пула к одному или нескольким rig'ам.

### Сигнатура

```python
async def update_rig_profile(
    ids: list[int],
    profile: int
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для обновления. |
| `profile` | `int` | ID профиля для применения. |

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def apply_profile():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.update_rig_profile(ids=[12345], profile=678)
        
        if response.success:
            print("Профиль применён успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## get_rig_pools

Получает пулы, назначенные rig'ам.

### Сигнатура

```python
async def get_rig_pools(
    ids: list[int]
) -> MRRResponse[list[Pool]]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для получения пулов. |

### Возвращаемое значение

`MRRResponse[list[Pool]]` — ответ со списком пулов:

- **При успехе:** `MRRResponse(success=True, data=[Pool, ...])`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def get_rig_pools():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_pools(ids=[12345])
        
        if response.success:
            for pool in response.data:
                print(f"{pool.name}: {pool.host}:{pool.port}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## update_rig_pool

Добавляет или заменяет пул на rig'ах.

### Сигнатура

```python
async def update_rig_pool(
    ids: list[int],
    body: RigPoolBody
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для обновления. |
| `body` | `RigPoolBody` | Тело запроса с данными пула. |

Поля `RigPoolBody`:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `host` | `str` | Да | Хост пула. |
| `port` | `int` | Да | Порт пула. |
| `user` | `str` | Да | Имя пользователя worker. |
| `password` | `str` | Да | Пароль пула. |
| `priority` | `int \| None` | Нет | Приоритет пула (0-4). |

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient
from aio_mrr.models.rig.request import RigPoolBody

async def update_rig_pool():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        body = RigPoolBody(
            host="pool.example.com",
            port=3333,
            user="worker1",
            password="password",
            priority=0,
        )
        
        response = await client.rig.update_rig_pool(ids=[12345], body=body)
        
        if response.success:
            print("Пул обновлён успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## delete_rig_pool

Удаляет пул с rig'ов.

Удаляет пул с указанным приоритетом с rig'ов.

### Сигнатура

```python
async def delete_rig_pool(
    ids: list[int]
) -> MRRResponse[None]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для удаления пула. |

### Возвращаемое значение

`MRRResponse[None]` — ответ:

- **При успехе:** `MRRResponse(success=True, data=None)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

### Пример использования

```python
from aio_mrr import MRRClient

async def delete_rig_pool():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.delete_rig_pool(ids=[12345])
        
        if response.success:
            print("Пул удалён успешно")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/03_manage_rigs.py`

---

## get_rig_ports

Получает прямой номер порта для подключения к серверу.

### Сигнатура

```python
async def get_rig_ports(
    ids: list[int]
) -> MRRResponse[RigPortInfo]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов (используется первый ID). |

### Возвращаемое значение

`MRRResponse[RigPortInfo]` — ответ с информацией о порте:

- **При успехе:** `MRRResponse(success=True, data=RigPortInfo)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

Поле `RigPortInfo`:

| Поле | Тип | Описание |
|------|-----|----------|
| `port` | `int` | Номер порта. |

### Пример использования

```python
from aio_mrr import MRRClient

async def get_rig_port():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_ports(ids=[12345])
        
        if response.success:
            print(f"Порт: {response.data.port}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/08_advanced_search.py`

---

## get_rig_threads

Получает список активных threads для rig'ов.

### Сигнатура

```python
async def get_rig_threads(
    ids: list[int]
) -> MRRResponse[list[RigThreadInfo]]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов для получения threads. |

### Возвращаемое значение

`MRRResponse[list[RigThreadInfo]]` — ответ со списком threads:

- **При успехе:** `MRRResponse(success=True, data=[RigThreadInfo, ...])`
- **При ошибке:** `MRRResponse(success=False, error=...)`

Поля `RigThreadInfo`:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID треда. |
| `rig_id` | `int` | ID рига. |
| `worker` | `str` | Имя worker. |
| `status` | `str` | Статус треда. |
| `hashrate` | `float \| None` | Хешрейт. |
| `last_share` | `str \| None` | Время последней шары. |

### Пример использования

```python
from aio_mrr import MRRClient

async def get_rig_threads():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_threads(ids=[12345])
        
        if response.success:
            for thread in response.data:
                print(f"{thread.worker}: {thread.status} - {thread.hashrate}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/08_advanced_search.py`

---

## get_rig_graph

Получает графические данные rig'а (исторический хешрейт, простои).

### Сигнатура

```python
async def get_rig_graph(
    ids: list[int],
    hours: float | None = None,
    deflate: bool | None = None
) -> MRRResponse[RigGraphData]
```

### Аргументы

| Параметр | Тип | Описание |
|----------|-----|----------|
| `ids` | `list[int]` | Список ID rig'ов (используется первый ID). |
| `hours` | `float \| None` | Часы данных (макс. 2 недели). По умолчанию `168`. |
| `deflate` | `bool \| None` | Base64 кодирование. По умолчанию `false`. |

### Возвращаемое значение

`MRRResponse[RigGraphData]` — ответ с графическими данными:

- **При успехе:** `MRRResponse(success=True, data=RigGraphData)`
- **При ошибке:** `MRRResponse(success=False, error=...)`

Поля `RigGraphData`:

| Поле | Тип | Описание |
|------|-----|----------|
| `hashrate_data` | `list[RigGraphDataPoint] \| None` | Данные о хешрейте. |
| `downtime_data` | `list[RigGraphDataPoint] \| None` | Данные о простоях. |
| `hours` | `float \| None` | Часы данных. |

Поля `RigGraphDataPoint`:

| Поле | Тип | Описание |
|------|-----|----------|
| `time` | `str` | Время точки. |
| `hashrate` | `float \| None` | Хешрейт в точке. |
| `downtime` | `bool \| None` | Признак простоя. |

### Пример использования

```python
from aio_mrr import MRRClient

async def get_rig_graph():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_graph(ids=[12345], hours=24)
        
        if response.success:
            print(f"Часов данных: {response.data.hours}")
            print(f"Точек хешрейта: {len(response.data.hashrate_data or [])}")
        else:
            print(f"Ошибка: {response.error}")
```

### Ссылка на пример

См.: `examples/08_advanced_search.py`

---

## Ссылки

- [« На главную](../../index.md)
- [Справочник AccountClient](./account.md)
- [Справочник RentalClient](./rentals.md)
- [Справочник RigGroupClient](./rig-groups.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

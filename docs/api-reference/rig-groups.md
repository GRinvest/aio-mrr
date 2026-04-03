# RigGroupClient — Справочник API

Справочник всех методов `RigGroupClient` для управления группами майнинг-установок (rig groups) на MiningRigRentals: создание групп, CRUD операции, добавление и удаление ригов из групп.

## Обзор

`RigGroupClient` предоставляет методы для:
- Получения списка групп ригов
- Получения информации о конкретной группе
- Создания новых групп ригов
- Обновления информации о группах
- Удаления групп ригов
- Добавления ригов в группу
- Удаления ригов из группы

---

## Методы

### 1. `get_list()`

Получает список ваших групп rig'ов.

**Сигнатура:**
```python
async def get_list() -> MRRResponse[list[RigGroupInfo]]
```

**Возвращает:**
- `MRRResponse[list[RigGroupInfo]]` — ответ со списком групп:
  - При успехе: `MRRResponse(success=True, data=[RigGroupInfo, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `RigGroupInfo`:**
- `id` — идентификатор группы (строка)
- `name` — название группы
- `enabled` — флаг включения группы (`True`/`False`)
- `rental_limit` — лимит активных аренд
- `rigs` — список идентификаторов rig'ов в группе (`list[int]`)
- `algo` — алгоритм майнинга группы (опционально, `str | None`)

**Пример использования:**
```python
# Получить список всех групп ригов
response = await client.riggroup.get_list()
if response.success:
    for group in response.data:
        print(f"Group ID: {group.id}")
        print(f"  Name: {group.name}")
        print(f"  Enabled: {group.enabled}")
        print(f"  Rental Limit: {group.rental_limit}")
        print(f"  Rigs: {group.rigs}")
        if group.algo:
            print(f"  Algorithm: {group.algo}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 2. `get_by_id(id)`

Получает детали группы rig'ов по ID.

**Сигнатура:**
```python
async def get_by_id(id: int) -> MRRResponse[RigGroupInfo]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `id` | `int` | Да | Идентификатор группы rig'ов |

**Возвращает:**
- `MRRResponse[RigGroupInfo]` — ответ с информацией о группе:
  - При успехе: `MRRResponse(success=True, data=RigGroupInfo)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `RigGroupInfo`:**
- `id` — идентификатор группы (строка)
- `name` — название группы
- `enabled` — флаг включения группы
- `rental_limit` — лимит активных аренд
- `rigs` — список идентификаторов rig'ов в группе
- `algo` — алгоритм майнинга группы (опционально)

**Пример использования:**
```python
# Получить информацию о конкретной группе
response = await client.riggroup.get_by_id(id=123)
if response.success:
    group = response.data
    print(f"Group ID: {group.id}")
    print(f"Name: {group.name}")
    print(f"Enabled: {group.enabled}")
    print(f"Rental Limit: {group.rental_limit}")
    print(f"Rigs in group: {len(group.rigs)}")
    print(f"Rig IDs: {group.rigs}")
    if group.algo:
        print(f"Algorithm: {group.algo}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 3. `create(body)`

Создаёт новую группу rig'ов.

**Сигнатура:**
```python
async def create(body: RigGroupCreateBody) -> MRRResponse[dict[str, Any]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `body` | `RigGroupCreateBody` | Да | Тело запроса с параметрами создания группы |

**Параметры `RigGroupCreateBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `name` | `str` | Да | Название группы |
| `enabled` | `bool` | Нет | Флаг включения группы. По умолчанию `True` |
| `rental_limit` | `int` | Нет | Лимит активных аренд. По умолчанию `1` |

**Возвращает:**
- `MRRResponse[dict[str, Any]]` — ответ с ID созданной группы и сообщением:
  - При успехе: `MRRResponse(success=True, data={"id": 123, "message": "..."})`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Пример использования:**
```python
from aio_mrr.models.riggroup.request import RigGroupCreateBody

# Создать группу с настройками по умолчанию (enabled=True, rental_limit=1)
body = RigGroupCreateBody(name="My Scrypt Rigs")
response = await client.riggroup.create(body)
if response.success:
    print(f"Group created with ID: {response.data['id']}")
    print(f"Message: {response.data['message']}")
else:
    print(f"Error: {response.error.message}")

# Создать группу с кастомными настройками
body = RigGroupCreateBody(
    name="High-Performance Rigs",
    enabled=True,
    rental_limit=10
)
response = await client.riggroup.create(body)
if response.success:
    print(f"Group created: {response.data}")
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 4. `update(id, body)`

Обновляет группу rig'ов.

**Сигнатура:**
```python
async def update(id: int, body: RigGroupUpdateBody) -> MRRResponse[None]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `id` | `int` | Да | Идентификатор группы rig'ов для обновления |
| `body` | `RigGroupUpdateBody` | Да | Тело запроса с параметрами обновления (все поля опциональные) |

**Параметры `RigGroupUpdateBody`:**
| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `name` | `str \| None` | Нет | Новое название группы |
| `enabled` | `bool \| None` | Нет | Новый статус включения |
| `rental_limit` | `int \| None` | Нет | Новый лимит аренд |

!!! note
    Все поля в `RigGroupUpdateBody` опциональные — можно обновлять только нужные параметры.

**Возвращает:**
- `MRRResponse[None]` — ответ о результате:
  - При успехе: `MRRResponse(success=True, data=None)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Пример использования:**
```python
from aio_mrr.models.riggroup.request import RigGroupUpdateBody

# Обновить только название группы
body = RigGroupUpdateBody(name="Updated Group Name")
response = await client.riggroup.update(id=123, body=body)
if response.success:
    print("Group name updated successfully")
else:
    print(f"Error: {response.error.message}")

# Обновить несколько параметров
body = RigGroupUpdateBody(
    name="New Name",
    enabled=False,
    rental_limit=15
)
response = await client.riggroup.update(id=123, body=body)
if response.success:
    print("Group updated successfully")
else:
    print(f"Error: {response.error.message}")

# Отключить группу
body = RigGroupUpdateBody(enabled=False)
response = await client.riggroup.update(id=123, body=body)
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 5. `delete(id)`

Удаляет группу rig'ов.

**Сигнатура:**
```python
async def delete(id: int) -> MRRResponse[dict[str, Any]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `id` | `int` | Да | Идентификатор группы rig'ов для удаления |

**Возвращает:**
- `MRRResponse[dict[str, Any]]` — ответ с подтверждением удаления:
  - При успехе: `MRRResponse(success=True, data={"id": 123, "message": "..."})`
  - При ошибке: `MRRResponse(success=False, error=...)`

!!! warning
    Удаление группы необратимо. Убедитесь, что группа больше не нужна перед удалением.

**Пример использования:**
```python
# Удалить группу
response = await client.riggroup.delete(id=123)
if response.success:
    print("Group deleted successfully")
    print(f"Message: {response.data['message']}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 6. `add_rigs(id, rig_ids)`

Добавляет rig'и в группу.

**Сигнатура:**
```python
async def add_rigs(id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `id` | `int` | Да | Идентификатор группы rig'ов |
| `rig_ids` | `list[int]` | Да | Список ID rig'ов для добавления в группу |

**Возвращает:**
- `MRRResponse[dict[str, Any]]` — ответ с подтверждением добавления:
  - При успехе: `MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит ответ:**
- `id` — идентификатор группы
- `message` — сообщение о результате
- `rigs` — список ID rig'ов, добавленных в группу

**Пример использования:**
```python
# Добавить один риг в группу
response = await client.riggroup.add_rigs(id=123, rig_ids=[12345])
if response.success:
    print(f"Rig added to group")
    print(f"Rigs in group: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")

# Добавить несколько ригов в группу
response = await client.riggroup.add_rigs(id=123, rig_ids=[12345, 12346, 12347])
if response.success:
    print(f"Rigs added: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 7. `remove_rigs(id, rig_ids)`

Удаляет rig'и из группы.

**Сигнатура:**
```python
async def remove_rigs(id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `id` | `int` | Да | Идентификатор группы rig'ов |
| `rig_ids` | `list[int]` | Да | Список ID rig'ов для удаления из группы |

**Возвращает:**
- `MRRResponse[dict[str, Any]]` — ответ с подтверждением удаления:
  - При успехе: `MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит ответ:**
- `id` — идентификатор группы
- `message` — сообщение о результате
- `rigs` — список ID rig'ов, удалённых из группы

**Пример использования:**
```python
# Удалить один риг из группы
response = await client.riggroup.remove_rigs(id=123, rig_ids=[12345])
if response.success:
    print(f"Rig removed from group")
    print(f"Remaining rigs: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")

# Удалить несколько ригов из группы
response = await client.riggroup.remove_rigs(id=123, rig_ids=[12345, 12346])
if response.success:
    print(f"Rigs removed: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

## Сводная таблица методов

| # | Метод | Описание | Возвращает | Пример |
|---|-------|----------|------------|--------|
| 1 | `get_list()` | Список групп ригов | `MRRResponse[list[RigGroupInfo]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 2 | `get_by_id(id)` | Группа по ID | `MRRResponse[RigGroupInfo]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 3 | `create(body)` | Создать группу | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 4 | `update(id, body)` | Обновить группу | `MRRResponse[None]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 5 | `delete(id)` | Удалить группу | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 6 | `add_rigs(id, rig_ids)` | Добавить риги в группу | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 7 | `remove_rigs(id, rig_ids)` | Удалить риги из группы | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |

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

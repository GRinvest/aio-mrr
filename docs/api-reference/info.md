# InfoClient — Справочник API

Справочник всех методов `InfoClient` для получения информации о серверах MiningRigRentals, алгоритмах майнинга и доступных валютах оплаты.

## Обзор

`InfoClient` предоставляет методы для:
- Получения списка серверов MRR
- Просмотра всех алгоритмов майнинга
- Получения информации о конкретном алгоритме
- Просмотра доступных валют оплаты

---

## Методы

### 1. `get_servers()`

Получает список всех серверов MiningRigRentals.

**Сигнатура:**
```python
async def get_servers(self) -> MRRResponse[ServersList]
```

**Возвращает:**
- `MRRResponse[ServersList]` — ответ со списком серверов
  - При успехе: `MRRResponse(success=True, data=ServersList)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `ServersList`:**
- `servers` — список `ServerInfo` объектов

**Что содержит `ServerInfo`:**
- `id` — идентификатор сервера (например, "EU-01")
- `name` — название сервера
- `region` — регион сервера
- `port` — порт сервера (опционально)
- `ethereum_port` — порт для Ethereum (опционально)

**Пример использования:**
```python
response = await client.info.get_servers()
if response.success:
    print("MRR Servers:")
    for server in response.data.servers:
        print(f"  - {server.name} ({server.id}): {server.region}")
        if server.port:
            print(f"    Port: {server.port}")
        if server.ethereum_port:
            print(f"    Ethereum Port: {server.ethereum_port}")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 2. `get_algos()`

Получает список всех алгоритмов майнинга с информацией о них.

**Сигнатура:**
```python
async def get_algos(currency: str | None = None) -> MRRResponse[list[AlgoInfo]]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `currency` | `str \| None` | Нет | Фильтр по валюте. По умолчанию возвращает все алгоритмы. |

**Возвращает:**
- `MRRResponse[list[AlgoInfo]]` — ответ со списком алгоритмов
  - При успехе: `MRRResponse(success=True, data=[AlgoInfo, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `AlgoInfo`:**
- `name` — внутреннее название алгоритма (например, "scrypt", "sha256")
- `display` — отображаемое название
- `suggested_price` — рекомендуемая цена (`PriceInfo`)
- `stats` — статистика алгоритма (`AlgoStats`)

**Что содержит `PriceInfo`:**
- `amount` — значение цены
- `currency` — валюта цены
- `unit` — единица измерения

**Что содержит `AlgoStats`:**
- `available` — доступная мощность (`AvailableHashInfo`)
- `rented` — арендованная мощность (`RentedHashInfo`)
- `prices` — ценовая информация (`PricesInfo`)

**Что содержит `AvailableHashInfo`:**
- `rigs` — количество доступных ригов
- `hash` — доступная хеш-мощность (`HashInfo`)

**Что содержит `RentedHashInfo`:**
- `rigs` — количество арендованных ригов
- `hash` — арендованная хеш-мощность (`HashInfo`)

**Что содержит `HashInfo`:**
- `hash` — значение хеш-мощности
- `unit` — единица измерения (например, "GH/s")
- `nice` — красивое форматирование

**Что содержит `PricesInfo`:**
- `lowest` — самая низкая цена
- `last_10` — средняя цена за последние 10 аренд
- `last` — последняя цена

!!! note
    Метод полезен для получения общего обзора всех доступных алгоритмов майнинга на платформе.

**Пример использования:**
```python
# Получить все алгоритмы
response = await client.info.get_algos()
if response.success:
    print("Mining Algorithms:")
    for algo in response.data:
        print(f"\n{algo.display} ({algo.name})")
        print(f"  Suggested Price: {algo.suggested_price.amount} {algo.suggested_price.currency}")
        print(f"  Available: {algo.stats.available.hash.nice}")
        print(f"  Rented: {algo.stats.rented.hash.nice}")
        print(f"  Lowest Price: {algo.stats.prices.lowest.amount}")
        print(f"  Last Price: {algo.stats.prices.last.amount}")
else:
    print(f"Error: {response.error.message}")

# Получить алгоритмы для конкретной валюты
response = await client.info.get_algos(currency="BTC")
```

**Ссылка на пример:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 3. `get_algo()`

Получает детальную информацию о конкретном алгоритме майнинга.

**Сигнатура:**
```python
async def get_algo(name: str, currency: str | None = None) -> MRRResponse[AlgoInfo]
```

**Аргументы:**
| Аргумент | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `name` | `str` | Да | Название алгоритма (например, "scrypt", "sha256", "x11") |
| `currency` | `str \| None` | Нет | Фильтр по валюте. По умолчанию возвращает информацию без фильтра. |

**Возвращает:**
- `MRRResponse[AlgoInfo]` — ответ с информацией об алгоритме
  - При успехе: `MRRResponse(success=True, data=AlgoInfo)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `AlgoInfo`:**
- `name` — внутреннее название алгоритма
- `display` — отображаемое название
- `suggested_price` — рекомендуемая цена (`PriceInfo`)
- `stats` — статистика алгоритма (`AlgoStats`)

!!! tip
    Используйте этот метод, когда вам нужна информация о конкретном алгоритме, например, для отображения в интерфейсе или для расчёта стоимости аренды.

**Пример использования:**
```python
# Получить информацию об алгоритме scrypt
response = await client.info.get_algo(name="scrypt")
if response.success:
    algo = response.data
    print(f"Algorithm: {algo.display}")
    print(f"Suggested Price: {algo.suggested_price.amount} {algo.suggested_price.currency}")
    print(f"Available Hashrate: {algo.stats.available.hash.nice}")
    print(f"Rented Hashrate: {algo.stats.rented.hash.nice}")
    print(f"Lowest Price: {algo.stats.prices.lowest.amount}")
    print(f"Last Price: {algo.stats.prices.last.amount}")
else:
    print(f"Error: {response.error.message}")

# Получить информацию с фильтром по валюте
response = await client.info.get_algo(name="sha256", currency="BTC")
```

**Ссылка на пример:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 4. `get_currencies()`

Получает список доступных валют для оплаты аренды.

**Сигнатура:**
```python
async def get_currencies(self) -> MRRResponse[list[CurrencyInfo]]
```

**Возвращает:**
- `MRRResponse[list[CurrencyInfo]]` — ответ со списком валют
  - При успехе: `MRRResponse(success=True, data=[CurrencyInfo, ...])`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `CurrencyInfo`:**
- `name` — название валюты (BTC, LTC, ETH, DOGE, BCH)
- `enabled` — статус включённости валюты
- `txfee` — комиссия транзакции для валюты

!!! note
    Этот метод возвращает валюты, доступные для оплаты аренды на платформе, в отличие от `AccountClient.get_currencies()`, который возвращает статусы валют для конкретного аккаунта.

**Пример использования:**
```python
response = await client.info.get_currencies()
if response.success:
    print("Available Payment Currencies:")
    for currency in response.data:
        status = "enabled" if currency.enabled else "disabled"
        print(f"  - {currency.name}: {status} (txfee: {currency.txfee})")
else:
    print(f"Error: {response.error.message}")
```

**Ссылка на пример:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

## Сводная таблица методов

| # | Метод | Описание | Возвращает | Пример |
|---|-------|----------|------------|--------|
| 1 | `get_servers()` | Список серверов MRR | `MRRResponse[ServersList]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 2 | `get_algos(currency)` | Все алгоритмы майнинга | `MRRResponse[list[AlgoInfo]]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 3 | `get_algo(name, currency)` | Информация об алгоритме | `MRRResponse[AlgoInfo]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 4 | `get_currencies()` | Доступные валюты оплаты | `MRRResponse[list[CurrencyInfo]]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |

---

## Дополнительные ресурсы

- [Главная страница](../../index.md)
- [Обработка ошибок](../error-handling.md)
- [Модели данных](../models.md)
- [Аутентификация](../authentication.md)
- [PricingClient](pricing.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

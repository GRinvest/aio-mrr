# Pydantic-модели данных

Полный справочник всех Pydantic-моделей библиотеки `aio-mrr`. Модели сгруппированы по категориям в соответствии с функциональными областями API.

---

## Содержание

- [Базовые модели](#базовые-модели)
- [Модели аккаунта](#модели-аккаунта)
- [Модели информации](#модели-информации)
- [Модели ценообразования](#модели-ценообразования)
- [Модели аренды](#модели-аренды)
- [Модели ригов](#модели-ригов)
- [Модели групп ригов](#модели-групп-ригов)
- [Модели запросов (Request Bodies)](#модели-запросов-request-bodies)

---

## Базовые модели

### BaseMRRModel

Базовая модель для всех Pydantic-моделей библиотеки. Использует конфигурацию `extra="ignore"`, что делает модели устойчивыми к изменениям API — дополнительные поля, возвращаемые API, игнорируются и не вызывают ошибок валидации.

```python
from pydantic import BaseModel, ConfigDict

class BaseMRRModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
```

---

### MRRResponseError

Объект ошибки, возвращаемый в случае неудачного запроса.

| Поле | Тип | Описание |
|------|-----|----------|
| `code` | `str` | Тип ошибки: `"network_error"`, `"api_error"`, `"validation_error"`, `"timeout"` |
| `message` | `str` | Человекочитаемое описание ошибки |
| `details` | `dict[str, Any] \| None` | Дополнительные данные об ошибке |
| `http_status` | `int \| None` | HTTP статус-код (401, 429, 500 и т.д.) |

Подробнее см.: [error-handling.md](./error-handling.md)

---

### MRRResponse[T]

Универсальная обёртка ответа API.

| Поле | Тип | Описание |
|------|-----|----------|
| `success` | `bool` | `True` если запрос успешен |
| `data` | `T \| None` | Типизированные данные (`None` при ошибке) |
| `error` | `MRRResponseError \| None` | Объект ошибки (`None` при успехе) |
| `http_status` | `int \| None` | HTTP статус-код ответа |
| `retry_count` | `int` | Количество повторных попыток |

Подробнее см.: [error-handling.md](./error-handling.md)

---

## Модели аккаунта

Модели для работы с аккаунтом, профилями, пулами и транзакциями.

### AccountInfo

Детальная информация об аккаунте.

| Поле | Тип | Описание |
|------|-----|----------|
| `username` | `str` | Имя пользователя |
| `email` | `str` | Email адрес |
| `withdraw` | `dict[str, WithdrawCurrencyInfo]` | Информация о выводе валют |
| `deposit` | `dict[str, DepositCurrencyInfo]` | Информация о депозитах валют |
| `notifications` | `NotificationsInfo` | Настройки уведомлений |
| `settings` | `SettingsInfo` | Настройки аккаунта |

---

### BalanceInfo

Информация о балансе по валютам.

| Поле | Тип | Описание |
|------|-----|----------|
| `confirmed` | `str` | Подтверждённый баланс |
| `pending` | `float` | Ожидающий баланс |
| `unconfirmed` | `str` | Неподтверждённый баланс |

---

### Transaction

Запись транзакции.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `str` | ID транзакции |
| `type` | `str` | Тип транзакции |
| `currency` | `str \| None` | Валюта транзакции |
| `amount` | `str` | Сумма транзакции |
| `when` | `str` | Дата/время (ISO формат) |
| `rental` | `str \| None` | ID аренды (если применимо) |
| `rig` | `str \| None` | ID рига (если применимо) |
| `txid` | `str \| None` | ID транзакции блокчейна |
| `txfee` | `str \| None` | Комиссия транзакции |
| `payout_address` | `str \| None` | Адрес выплаты |
| `sent` | `str \| None` | Отправлено |
| `status` | `str` | Статус транзакции |
| `pending_seconds` | `int \| None` | Секунды ожидания |
| `info` | `str \| None` | Дополнительная информация |

---

### TransactionsList

Список транзакций с метаданными пагинации.

| Поле | Тип | Описание |
|------|-----|----------|
| `total` | `str` | Общее количество транзакций |
| `returned` | `int` | Количество возвращённых записей |
| `start` | `int` | Начальная позиция |
| `limit` | `int` | Лимит записей |
| `transactions` | `list[Transaction]` | Список транзакций |

---

### Profile

Пул-профиль пользователя.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `str` | ID профиля |
| `name` | `str` | Название профиля |
| `algo` | `AlgoProfileInfo` | Информация об алгоритме профиля |
| `pools` | `list[PoolProfileInfo]` | Список пулов в профиле |

---

### Pool

Информация о сохранённом пуле.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID пула |
| `type` | `str` | Тип подключения (например, `stratum+tcp`) |
| `name` | `str` | Название пула |
| `host` | `str` | Хост пула |
| `port` | `int` | Порт пула |
| `user` | `str` | Имя пользователя/воркера |
| `password` | `str` | Пароль (alias: `pass`) |
| `notes` | `str \| None` | Примечания |
| `algo` | `AlgoPoolInfo \| None` | Информация об алгоритме |

---

### PoolCreateBody

Тело запроса для создания пула.

| Поле | Тип | Описание |
|------|-----|----------|
| `type` | `str` | Тип подключения (обязательный) |
| `name` | `str` | Название пула (обязательный) |
| `host` | `str` | Хост пула (обязательный) |
| `port` | `int` | Порт пула (обязательный) |
| `user` | `str` | Имя пользователя (обязательный) |
| `password` | `str \| None` | Пароль (alias: `pass`) |
| `notes` | `str \| None` | Примечания |

---

### PoolTestBody

Тело запроса для тестирования пула.

| Поле | Тип | Описание |
|------|-----|----------|
| `method` | `str` | Метод теста: `"simple"` или `"full"` (обязательный) |
| `extramethod` | `str \| None` | Дополнительный метод |
| `type` | `str \| None` | Тип подключения |
| `host` | `str \| None` | Хост пула |
| `port` | `int \| None` | Порт пула |
| `user` | `str \| None` | Имя пользователя |
| `password` | `str \| None` | Пароль (alias: `pass`) |
| `source` | `str \| None` | Источник теста |

---

### PoolTestResult

Результат тестирования пула.

| Поле | Тип | Описание |
|------|-----|----------|
| `result` | `list[PoolTestResultItem]` | Результаты тестов |
| `error` | `list[str]` | Список ошибок |

---

### PoolTestResultItem

Отдельный результат теста подключения пула.

| Поле | Тип | Описание |
|------|-----|----------|
| `source` | `str` | Источник теста |
| `dest` | `str` | Цель подключения |
| `error` | `str` | Ошибка подключения |
| `connection` | `bool` | Успешно ли подключение |
| `executiontime` | `float` | Время выполнения (сек) |
| `protocol` | `str \| None` | Протокол |
| `sub` | `bool \| None` | Поддержка subscription |
| `auth` | `bool \| None` | Авторизация успешна |
| `red` | `bool \| None` | Red connection |
| `diffs` | `bool \| None` | Поддержка diff |
| `diff` | `float \| None` | Диффференциал |
| `work` | `bool \| None` | Поддержка work |
| `xnonce` | `bool \| None` | Поддержка xnonce |
| `ssl` | `bool \| None` | SSL подключение |

---

### PoolCreateResponse

Ответ на создание пула.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID созданного пула |

---

### ProfileCreateBody

Тело запроса для создания профиля.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название профиля (обязательный) |
| `algo` | `str` | Алгоритм (обязательный) |

---

### ProfileCreateResponse

Ответ на создание профиля.

| Поле | Тип | Описание |
|------|-----|----------|
| `pid` | `str` | ID созданного профиля |

---

### ProfileDeleteResponse

Ответ на удаление профиля.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `str` | ID удалённого профиля |
| `success` | `bool` | Успешность удаления |
| `message` | `str` | Сообщение результата |

---

### CurrencyStatus

Статус валюты аккаунта.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название валюты |
| `enabled` | `bool` | Валюта включена |

---

### WithdrawCurrencyInfo

Информация о выводе валюты.

| Поле | Тип | Описание |
|------|-----|----------|
| `address` | `str` | Адрес вывода |
| `label` | `str` | Метка валюты |
| `auto_pay_threshold` | `str` | Порог автовыплаты |
| `txfee` | `float` | Комиссия транзакции |

---

### DepositCurrencyInfo

Информация о депозите валюты.

| Поле | Тип | Описание |
|------|-----|----------|
| `address` | `str` | Адрес депозита |

---

### NotificationsInfo

Настройки уведомлений аккаунта.

| Поле | Тип | Описание |
|------|-----|----------|
| `rental_comm` | `str` | Уведомления о комментариях аренды |
| `new_rental` | `str` | Уведомления о новых арендах |
| `offline` | `str` | Уведомления об оффлайне |
| `news` | `str` | Уведомления о новостях |
| `deposit` | `str` | Уведомления о депозитах |

---

### SettingsInfo

Настройки аккаунта.

| Поле | Тип | Описание |
|------|-----|----------|
| `live_data` | `str` | Режим живых данных |
| `public_profile` | `str` | Публичный профиль |
| `two_factor_auth` | `str` | Двухфакторная аутентификация |

---

### AlgoProfileInfo

Информация об алгоритме в профиле.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название алгоритма |
| `display` | `str` | Отображаемое название |
| `suggested_price` | `PriceInfo` | Рекомендуемая цена |

---

### PoolProfileInfo

Информация о пуле в профиле.

| Поле | Тип | Описание |
|------|-----|----------|
| `priority` | `int` | Приоритет пула (0-4) |
| `type` | `str` | Тип подключения |
| `host` | `str` | Хост пула |
| `port` | `str` | Порт пула |
| `user` | `str` | Имя пользователя |
| `password` | `str` | Пароль (alias: `pass`) |
| `status` | `str` | Статус пула |

---

### AlgoPoolInfo

Информация об алгоритме пула.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название алгоритма |
| `display` | `str` | Отображаемое название |

---

## Модели информации

Модели для получения информации о серверах, алгоритмах и валютах.

### AlgoInfo

Информация об алгоритме майнинга.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название алгоритма |
| `display` | `str` | Отображаемое название |
| `suggested_price` | `PriceInfo` | Рекомендуемая цена |
| `stats` | `AlgoStats` | Статистика алгоритма |

---

### AlgoStats

Статистика алгоритма майнинга.

| Поле | Тип | Описание |
|------|-----|----------|
| `available` | `AvailableHashInfo` | Доступная мощность |
| `rented` | `RentedHashInfo` | Арендованная мощность |
| `prices` | `PricesInfo` | Информация о ценах |

---

### AvailableHashInfo

Доступная хеш-мощность.

| Поле | Тип | Описание |
|------|-----|----------|
| `rigs` | `str` | Количество ригов |
| `hash` | `HashInfo` | Информация о хешрейте |

---

### RentedHashInfo

Арендованная хеш-мощность.

| Поле | Тип | Описание |
|------|-----|----------|
| `rigs` | `str` | Количество ригов |
| `hash` | `HashInfo` | Информация о хешрейте |

---

### PricesInfo

Информация о ценах.

| Поле | Тип | Описание |
|------|-----|----------|
| `lowest` | `PriceInfo` | Низшая цена |
| `last_10` | `PriceInfo` | Цена последних 10 аренд |
| `last` | `PriceInfo` | Последняя цена |

---

### PriceInfo

Информация о цене.

| Поле | Тип | Описание |
|------|-----|----------|
| `amount` | `str` | Сумма цены |
| `currency` | `str` | Валюта цены |
| `unit` | `str` | Единица измерения |

---

### HashInfo

Информация о хешрейте.

| Поле | Тип | Описание |
|------|-----|----------|
| `hash` | `float` | Значение хешрейта |
| `unit` | `str` | Единица измерения |
| `nice` | `str` | Красивое форматирование |

---

### ServerInfo

Информация о сервере MRR.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `str` | ID сервера |
| `name` | `str` | Название сервера |
| `region` | `str` | Регион |
| `port` | `str \| None` | Порт (общий) |
| `ethereum_port` | `str \| None` | Порт для Ethereum |

---

### ServersList

Список серверов MRR.

| Поле | Тип | Описание |
|------|-----|----------|
| `servers` | `list[ServerInfo]` | Список серверов |

---

### CurrencyInfo

Информация о валюте оплаты.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название валюты |
| `enabled` | `bool` | Валюта включена |
| `txfee` | `str` | Комиссия транзакции |

---

## Модели ценообразования

Модели для получения курсов конвертации и рыночных цен.

### PricingInfo

Общая информация о ценообразовании.

| Поле | Тип | Описание |
|------|-----|----------|
| `conversion_rates` | `ConversionRates` | Курсы конвертации валют |
| `market_rates` | `MarketRates` | Рыночные цены по алгоритмам |

---

### ConversionRates

Курсы конвертации между криптовалютами.

| Поле | Тип | Описание |
|------|-----|----------|
| `LTC` | `str` | Курс LTC |
| `ETH` | `str` | Курс ETH |
| `BCH` | `str` | Курс BCH |
| `DOGE` | `str` | Курс DOGE |

---

### MarketRate

Рыночная цена для алгоритма по валютам.

| Поле | Тип | Описание |
|------|-----|----------|
| `BTC` | `str` | Цена в BTC |
| `LTC` | `str` | Цена в LTC |
| `ETH` | `str` | Цена в ETH |
| `BCH` | `str` | Цена в BCH |
| `DOGE` | `str` | Цена в DOGE |

---

### MarketRates

Рыночные цены по всем алгоритмам.

| Поле | Тип | Описание |
|------|-----|----------|
| `allium` | `MarketRate` | Цена для allium |
| `argon2dchukwa` | `MarketRate` | Цена для argon2dchukwa |
| `autolykosv2` | `MarketRate` | Цена для autolykosv2 |
| `kawpow` | `MarketRate` | Цена для kawpow |
| `kheavyhash` | `MarketRate` | Цена для kheavyhash |
| `randomx` | `MarketRate` | Цена для randomx |
| `scrypt` | `MarketRate` | Цена для scrypt |
| `sha256` | `MarketRate` | Цена для sha256 |
| `x11` | `MarketRate` | Цена для x11 |

---

## Модели аренды

Модели для работы с арендами.

### RentalInfo

Информация об аренде.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `str` | ID аренды |
| `rig_id` | `str` | ID рига (alias: `rig_id`) |
| `rig_name` | `str \| None` | Название рига |
| `owner` | `str \| None` | Владелец рига |
| `renter` | `str \| None` | Арендатор |
| `status` | `str \| None` | Статус аренды |
| `started` | `str \| None` | Время начала |
| `ends` | `str \| None` | Время окончания |
| `length` | `float \| None` | Длительность (часы) |
| `currency` | `str \| None` | Валюта оплаты |
| `rate` | `RateInfo \| None` | Информация о ставке |
| `hash` | `RentalHashInfo \| None` | Информация о хешрейте |
| `cost` | `RentalCostInfo \| None` | Информация о стоимости |

---

### RentalLogEntry

Запись лога аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `time` | `str` | Время события |
| `message` | `str` | Сообщение события |

---

### RentalMessage

Сообщение аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `time` | `str` | Время сообщения |
| `user` | `str` | Отправитель |
| `message` | `str` | Текст сообщения |

---

### GraphData

Данные графика хешрейта аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `hashrate_data` | `list[GraphDataPoint] \| None` | Данные по хешрейту |
| `downtime_data` | `list[GraphDataPoint] \| None` | Данные по простоям |
| `hours` | `float \| None` | Количество часов |

---

### GraphDataPoint

Точка данных графика.

| Поле | Тип | Описание |
|------|-----|----------|
| `time` | `str \| None` | Время точки |
| `hashrate` | `float \| None` | Хешрейт в точке |
| `downtime` | `bool \| None` | Простой в точке |

---

### RateInfo

Информация о ставке аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `type` | `str \| None` | Тип ставки (alias: `rate.type`) |
| `price` | `str \| None` | Цена ставки (alias: `rate.price`) |

---

### RentalHashInfo

Информация о хешрейте аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `hash` | `float \| None` | Значение хешрейта |
| `type` | `str \| None` | Тип алгоритма |

---

### RentalCostInfo

Информация о стоимости аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `amount` | `str \| None` | Сумма стоимости |
| `currency` | `str \| None` | Валюта стоимости |

---

### RentalCreateBody

Тело запроса для создания аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `rig` | `int` | ID рига (обязательный) |
| `length` | `float` | Длительность в часах (обязательный) |
| `profile` | `int` | ID профиля (обязательный) |
| `currency` | `str \| None` | Валюта оплаты |
| `rate_type` | `str \| None` | Тип ставки (alias: `rate.type`) |
| `rate_price` | `float \| None` | Цена ставки (alias: `rate.price`) |

---

### RentalPoolBody

Тело запроса для обновления пула аренды.

| Поле | Тип | Описание |
|------|-----|----------|
| `host` | `str` | Хост пула (обязательный) |
| `port` | `int` | Порт пула (обязательный) |
| `user` | `str` | Имя пользователя (обязательный) |
| `password` | `str` | Пароль (alias: `pass`, обязательный) |
| `priority` | `int \| None` | Приоритет пула |

---

## Модели ригов

Модели для работы с ригами.

### RigInfo

Информация о rigе.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID рига |
| `name` | `str` | Название рига |
| `description` | `str \| None` | Описание рига |
| `server` | `str \| None` | Сервер рига |
| `status` | `str \| None` | Статус рига |
| `price` | `dict[str, RigPriceInfo] \| None` | Информация о цене (по валютам) |
| `price_type` | `str \| None` | Тип цены (alias: `price.type`) |
| `minhours` | `float \| None` | Минимальное время аренды |
| `maxhours` | `float \| None` | Максимальное время аренды |
| `extensions` | `bool \| None` | Возможность продления |
| `hash` | `RigHashInfo \| None` | Информация о хешрейте |
| `suggested_diff` | `float \| None` | Рекомендуемый дифф |
| `ndevices` | `int \| None` | Количество устройств |
| `type` | `str \| None` | Тип рига |
| `region` | `str \| None` | Регион |
| `online` | `bool \| None` | Онлайн статус |
| `rented` | `bool \| None` | Сдан в аренду |
| `last_hashrate` | `float \| None` | Последний хешрейт |
| `rpi` | `int \| None` | RPI индекс |
| `owner` | `str \| None` | Владелец |

---

### RigPortInfo

Информация о порте сервера рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `port` | `int` | Порт сервера |

---

### RigThreadInfo

Информация о рабочем треде рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID треда |
| `rig_id` | `int` | ID рига |
| `worker` | `str` | Название воркера |
| `status` | `str` | Статус треда |
| `hashrate` | `float \| None` | Хешрейт треда |
| `last_share` | `str \| None` | Время последней shares |

---

### RigGraphData

Данные графика хешрейта рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `hashrate_data` | `list[RigGraphDataPoint] \| None` | Данные по хешрейту |
| `downtime_data` | `list[RigGraphDataPoint] \| None` | Данные по простоям |
| `hours` | `float \| None` | Количество часов |

---

### RigGraphDataPoint

Точка данных графика рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `time` | `str` | Время точки |
| `hashrate` | `float \| None` | Хешрейт в точке |
| `downtime` | `bool \| None` | Простой в точке |

---

### RigPriceInfo

Информация о цене рига по валюте.

| Поле | Тип | Описание |
|------|-----|----------|
| `enabled` | `bool \| None` | Валюта включена |
| `price` | `float \| None` | Цена |
| `autoprice` | `bool \| None` | Автоматическое ценообразование |
| `minimum` | `float \| None` | Минимальная цена |
| `modifier` | `str \| None` | Модификатор цены |

---

### RigHashInfo

Информация о хешрейте рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `hash` | `float \| None` | Значение хешрейта |
| `type` | `str \| None` | Тип алгоритма |

---

### RigCreateBody

Тело запроса для создания рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название рига (обязательный) |
| `description` | `str \| None` | Описание рига |
| `status` | `str \| None` | Статус рига |
| `server` | `str` | Сервер рига (обязательный) |
| `price_btc_enabled` | `bool \| None` | BTC включён (alias: `price.btc.enabled`) |
| `price_btc_price` | `float \| None` | Цена BTC (alias: `price.btc.price`) |
| `price_btc_autoprice` | `bool \| None` | Автоцена BTC (alias: `price.btc.autoprice`) |
| `price_btc_minimum` | `float \| None` | Мин. цена BTC (alias: `price.btc.minimum`) |
| `price_btc_modifier` | `str \| None` | Модификатор BTC (alias: `price.btc.modifier`) |
| `price_ltc_enabled` | `bool \| None` | LTC включён (alias: `price.ltc.enabled`) |
| `price_eth_enabled` | `bool \| None` | ETH включён (alias: `price.eth.enabled`) |
| `price_doge_enabled` | `bool \| None` | DOGE включён (alias: `price.doge.enabled`) |
| `price_type` | `str \| None` | Тип цены (alias: `price.type`) |
| `minhours` | `float \| None` | Минимальное время |
| `maxhours` | `float \| None` | Максимальное время |
| `extensions` | `bool \| None` | Возможность продления |
| `hash_hash` | `float \| None` | Хешрейт (alias: `hash.hash`) |
| `hash_type` | `str \| None` | Тип алгоритма (alias: `hash.type`) |
| `suggested_diff` | `float \| None` | Рекомендуемый дифф |
| `ndevices` | `int \| None` | Количество устройств |

---

### RigBatchBody

Тело запроса для пакетного обновления ригов.

| Поле | Тип | Описание |
|------|-----|----------|
| `rigs` | `list[dict[str, object]]` | Список ригов для обновления (обязательный) |

---

### RigPoolBody

Тело запроса для обновления пула рига.

| Поле | Тип | Описание |
|------|-----|----------|
| `host` | `str` | Хост пула (обязательный) |
| `port` | `int` | Порт пула (обязательный) |
| `user` | `str` | Имя пользователя (обязательный) |
| `password` | `str` | Пароль (alias: `pass`, обязательный) |
| `priority` | `int \| None` | Приоритет пула |

---

## Модели групп ригов

Модели для работы с группами ригов.

### RigGroupInfo

Информация о группе ригов.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `str` | ID группы |
| `name` | `str` | Название группы |
| `enabled` | `bool` | Группа включена |
| `rental_limit` | `int` | Лимит аренды |
| `rigs` | `list[int]` | Список ID ригов в группе |
| `algo` | `str \| None` | Алгоритм группы |

---

### RigGroupCreateBody

Тело запроса для создания группы ригов.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название группы (обязательный) |
| `enabled` | `bool` | Включить группу (по умолчанию `True`) |
| `rental_limit` | `int` | Лимит аренды (по умолчанию `1`) |

---

### RigGroupUpdateBody

Тело запроса для обновления группы ригов.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str \| None` | Новое название группы |
| `enabled` | `bool \| None` | Новый статус включения |
| `rental_limit` | `int \| None` | Новый лимит аренды |

---

## Модели запросов (Request Bodies)

Дополнительные модели для параметров запросов.

### TransactionsQueryParams

Параметры запроса для получения транзакций.

| Поле | Тип | Описание |
|------|-----|----------|
| `start` | `int \| None` | Начальная позиция |
| `limit` | `int \| None` | Лимит записей |
| `algo` | `str \| None` | Фильтр по алгоритму |
| `type` | `str \| None` | Фильтр по типу |
| `rig` | `int \| None` | Фильтр по rigу |
| `rental` | `int \| None` | Фильтр по аренде |
| `txid` | `str \| None` | Фильтр по txid |
| `time_greater_eq` | `str \| None` | Время >= (ISO) |
| `time_less_eq` | `str \| None` | Время <= (ISO) |

---

## См. также

- [« На главную](./index.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>
- [Обработка ошибок](./error-handling.md)
- [Справочник API](./api-reference/account.md)

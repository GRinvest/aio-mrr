# PricingClient — Справочник API

Справочник метода `PricingClient` для получения информации о курсах конвертации и рыночных ценах алгоритмов майнинга на MiningRigRentals.

## Обзор

`PricingClient` предоставляет метод для:

- Получения актуальных курсов конвертации между криптовалютами (LTC, ETH, BCH, DOGE)
- Просмотра рыночных цен по всем алгоритмам майнинга

---

## Методы

### 1. `get_pricing()`

Получает актуальные курсы конвертации и рыночные цены по алгоритмам майнинга.

**Сигнатура:**

```python
async def get_pricing(self) -> MRRResponse[PricingInfo]
```

**Возвращает:**

- `MRRResponse[PricingInfo]` — ответ с информацией о ценообразовании
  - При успехе: `MRRResponse(success=True, data=PricingInfo)`
  - При ошибке: `MRRResponse(success=False, error=...)`

**Что содержит `PricingInfo`:**

| Поле | Тип | Описание |
| --- | --- | --- |
| `conversion_rates` | `ConversionRates` | Курсы конвертации между криптовалютами |
| `market_rates` | `MarketRates` | Рыночные цены по алгоритмам майнинга |

### Структура `ConversionRates`

Курсы конвертации между основными криптовалютами:

| Поле | Тип | Описание |
| --- | --- | --- |
| `LTC` | `str` | Курс Litecoin (например, "0.02345678") |
| `ETH` | `str` | Курс Ethereum (например, "0.00123456") |
| `BCH` | `str` | Курс Bitcoin Cash (например, "0.00098765") |
| `DOGE` | `str` | Курс Dogecoin (например, "123.45678901") |

!!! note
    Курсы конвертации позволяют пересчитывать цены между разными валютами при аренде ригов.

### Структура `MarketRates`

Рыночные цены по каждому алгоритму майнинга. Для каждого алгоритма доступны цены в 5 валютах:

| Алгоритм | BTC | LTC | ETH | BCH | DOGE |
| --- | --- | --- | --- | --- | --- |
| `allium` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `argon2dchukwa` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `autolykosv2` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `kawpow` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `kheavyhash` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `randomx` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `scrypt` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `sha256` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |
| `x11` | Цена в BTC | Цена в LTC | Цена в ETH | Цена в BCH | Цена в DOGE |

### Структура `MarketRate`

Для каждого алгоритма доступна следующая структура:

| Поле | Тип | Описание |
| --- | --- | --- |
| `BTC` | `str` | Рыночная цена в Bitcoin |
| `LTC` | `str` | Рыночная цена в Litecoin |
| `ETH` | `str` | Рыночная цена в Ethereum |
| `BCH` | `str` | Рыночная цена в Bitcoin Cash |
| `DOGE` | `str` | Рыночная цена в Dogecoin |

!!! tip
    Используйте `market_rates`, чтобы узнать актуальную стоимость аренды ригов для конкретного алгоритма в выбранной валюте.

**Пример использования:**

```python
response = await client.pricing.get_pricing()
if response.success:
    pricing = response.data
    
    # Вывод курсов конвертации
    print("Conversion Rates:")
    print(f"  LTC: {pricing.conversion_rates.LTC}")
    print(f"  ETH: {pricing.conversion_rates.ETH}")
    print(f"  BCH: {pricing.conversion_rates.BCH}")
    print(f"  DOGE: {pricing.conversion_rates.DOGE}")
    
    # Вывод рыночных цен для алгоритма scrypt
    print("\nMarket Rates for scrypt:")
    scrypt_rates = pricing.market_rates.scrypt
    print(f"  BTC: {scrypt_rates.BTC}")
    print(f"  LTC: {scrypt_rates.LTC}")
    print(f"  ETH: {scrypt_rates.ETH}")
    print(f"  BCH: {scrypt_rates.BCH}")
    print(f"  DOGE: {scrypt_rates.DOGE}")
    
    # Вывод всех алгоритмов
    print("\nAll Algorithm Market Rates:")
    for algo_name in ["allium", "argon2dchukwa", "autolykosv2", "kawpow",
                      "kheavyhash", "randomx", "scrypt", "sha256", "x11"]:
        algo_rates = getattr(pricing.market_rates, algo_name)
        print(f"  {algo_name}: BTC={algo_rates.BTC}, LTC={algo_rates.LTC}")
else:
    print(f"Error: {response.error.message}")
```

---

## Сводная таблица методов

| # | Метод | Описание | Возвращает | Пример |
| --- | --- | --- | --- | --- |
| 1 | `get_pricing()` | Курсы конвертации и рыночные цены | `MRRResponse[PricingInfo]` | — |

---

## Дополнительные ресурсы

- [Главная страница](../../index.md)
- [Обработка ошибок](../error-handling.md)
- [Модели данных](../models.md)
- [Аутентификация](../authentication.md)
- [InfoClient](info.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

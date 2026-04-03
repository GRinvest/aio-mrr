# PricingClient — API Reference

Reference for the `PricingClient` method for retrieving conversion rates and market prices for mining algorithms on MiningRigRentals.

## Overview

`PricingClient` provides a method for:

- Retrieving up-to-date conversion rates between cryptocurrencies (LTC, ETH, BCH, DOGE)
- Viewing market prices for all mining algorithms

---

## Methods

### 1. `get_pricing()`

Retrieves current conversion rates and market prices for mining algorithms.

**Signature:**

```python
async def get_pricing(self) -> MRRResponse[PricingInfo]
```

**Returns:**

- `MRRResponse[PricingInfo]` — response with pricing information
  - On success: `MRRResponse(success=True, data=PricingInfo)`
  - On error: `MRRResponse(success=False, error=...)`

**What `PricingInfo` contains:**

| Field | Type | Description |
|-------|------|-------------|
| `conversion_rates` | `ConversionRates` | Conversion rates between cryptocurrencies |
| `market_rates` | `MarketRates` | Market prices for mining algorithms |

### `ConversionRates` Structure

Conversion rates between major cryptocurrencies:

| Field | Type | Description |
|-------|------|-------------|
| `LTC` | `str` | Litecoin rate (e.g., "0.02345678") |
| `ETH` | `str` | Ethereum rate (e.g., "0.00123456") |
| `BCH` | `str` | Bitcoin Cash rate (e.g., "0.00098765") |
| `DOGE` | `str` | Dogecoin rate (e.g., "123.45678901") |

!!! note
    Conversion rates allow you to recalculate prices between different currencies when renting rigs.

### `MarketRates` Structure

Market prices for each mining algorithm. For each algorithm, prices are available in 5 currencies:

| Algorithm | BTC | LTC | ETH | BCH | DOGE |
|-----------|-----|-----|-----|-----|------|
| `allium` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `argon2dchukwa` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `autolykosv2` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `kawpow` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `kheavyhash` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `randomx` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `scrypt` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `sha256` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |
| `x11` | Price in BTC | Price in LTC | Price in ETH | Price in BCH | Price in DOGE |

### `MarketRate` Structure

For each algorithm, the following structure is available:

| Field | Type | Description |
|-------|------|-------------|
| `BTC` | `str` | Market price in Bitcoin |
| `LTC` | `str` | Market price in Litecoin |
| `ETH` | `str` | Market price in Ethereum |
| `BCH` | `str` | Market price in Bitcoin Cash |
| `DOGE` | `str` | Market price in Dogecoin |

!!! tip
    Use `market_rates` to find out the current rental cost of rigs for a specific algorithm in your chosen currency.

**Usage Example:**

```python
response = await client.pricing.get_pricing()
if response.success:
    pricing = response.data

    # Output conversion rates
    print("Conversion Rates:")
    print(f"  LTC: {pricing.conversion_rates.LTC}")
    print(f"  ETH: {pricing.conversion_rates.ETH}")
    print(f"  BCH: {pricing.conversion_rates.BCH}")
    print(f"  DOGE: {pricing.conversion_rates.DOGE}")

    # Output market prices for the scrypt algorithm
    print("\nMarket Rates for scrypt:")
    scrypt_rates = pricing.market_rates.scrypt
    print(f"  BTC: {scrypt_rates.BTC}")
    print(f"  LTC: {scrypt_rates.LTC}")
    print(f"  ETH: {scrypt_rates.ETH}")
    print(f"  BCH: {scrypt_rates.BCH}")
    print(f"  DOGE: {scrypt_rates.DOGE}")

    # Output all algorithms
    print("\nAll Algorithm Market Rates:")
    for algo_name in ["allium", "argon2dchukwa", "autolykosv2", "kawpow",
                      "kheavyhash", "randomx", "scrypt", "sha256", "x11"]:
        algo_rates = getattr(pricing.market_rates, algo_name)
        print(f"  {algo_name}: BTC={algo_rates.BTC}, LTC={algo_rates.LTC}")
else:
    print(f"Error: {response.error.message}")
```

---

## Methods Summary Table

| # | Method | Description | Returns | Example |
|---|--------|-------------|---------|---------|
| 1 | `get_pricing()` | Conversion rates and market prices | `MRRResponse[PricingInfo]` | — |

---

## Additional Resources

- [Home Page](../../index.md)
- [Error Handling](../error-handling.md)
- [Data Models](../models.md)
- [Authentication](../authentication.md)
- [InfoClient](info.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

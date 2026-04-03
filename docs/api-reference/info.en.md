# InfoClient — API Reference

Reference for all `InfoClient` methods for retrieving information about MiningRigRentals servers, mining algorithms, and available payment currencies.

## Overview

`InfoClient` provides methods for:
- Retrieving the list of MRR servers
- Viewing all mining algorithms
- Getting information about a specific algorithm
- Viewing available payment currencies

---

## Methods

### 1. `get_servers()`

Retrieves a list of all MiningRigRentals servers.

**Signature:**
```python
async def get_servers(self) -> MRRResponse[ServersList]
```

**Returns:**
- `MRRResponse[ServersList]` — response with server list
  - On success: `MRRResponse(success=True, data=ServersList)`
  - On error: `MRRResponse(success=False, error=...)`

**What `ServersList` contains:**
- `servers` — list of `ServerInfo` objects

**What `ServerInfo` contains:**
- `id` — server identifier (e.g., "EU-01")
- `name` — server name
- `region` — server region
- `port` — server port (optional)
- `ethereum_port` — Ethereum port (optional)

**Usage Example:**
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

**Example link:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 2. `get_algos()`

Retrieves a list of all mining algorithms with their information.

**Signature:**
```python
async def get_algos(currency: str | None = None) -> MRRResponse[list[AlgoInfo]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `currency` | `str \| None` | No | Filter by currency. Returns all algorithms by default. |

**Returns:**
- `MRRResponse[list[AlgoInfo]]` — response with algorithm list
  - On success: `MRRResponse(success=True, data=[AlgoInfo, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `AlgoInfo` contains:**
- `name` — internal algorithm name (e.g., "scrypt", "sha256")
- `display` — display name
- `suggested_price` — suggested price (`PriceInfo`)
- `stats` — algorithm statistics (`AlgoStats`)

**What `PriceInfo` contains:**
- `amount` — price value
- `currency` — price currency
- `unit` — unit of measurement

**What `AlgoStats` contains:**
- `available` — available hash power (`AvailableHashInfo`)
- `rented` — rented hash power (`RentedHashInfo`)
- `prices` — price information (`PricesInfo`)

**What `AvailableHashInfo` contains:**
- `rigs` — number of available rigs
- `hash` — available hash power (`HashInfo`)

**What `RentedHashInfo` contains:**
- `rigs` — number of rented rigs
- `hash` — rented hash power (`HashInfo`)

**What `HashInfo` contains:**
- `hash` — hash power value
- `unit` — unit of measurement (e.g., "GH/s")
- `nice` — pretty-formatted string

**What `PricesInfo` contains:**
- `lowest` — lowest price
- `last_10` — average price for the last 10 rentals
- `last` — last price

!!! note
    This method is useful for getting a general overview of all available mining algorithms on the platform.

**Usage Example:**
```python
# Get all algorithms
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

# Get algorithms for a specific currency
response = await client.info.get_algos(currency="BTC")
```

**Example link:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 3. `get_algo()`

Retrieves detailed information about a specific mining algorithm.

**Signature:**
```python
async def get_algo(name: str, currency: str | None = None) -> MRRResponse[AlgoInfo]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | `str` | Yes | Algorithm name (e.g., "scrypt", "sha256", "x11") |
| `currency` | `str \| None` | No | Filter by currency. Returns unfiltered information by default. |

**Returns:**
- `MRRResponse[AlgoInfo]` — response with algorithm information
  - On success: `MRRResponse(success=True, data=AlgoInfo)`
  - On error: `MRRResponse(success=False, error=...)`

**What `AlgoInfo` contains:**
- `name` — internal algorithm name
- `display` — display name
- `suggested_price` — suggested price (`PriceInfo`)
- `stats` — algorithm statistics (`AlgoStats`)

!!! tip
    Use this method when you need information about a specific algorithm, for example, to display in a UI or to calculate rental costs.

**Usage Example:**
```python
# Get information about the scrypt algorithm
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

# Get information with currency filter
response = await client.info.get_algo(name="sha256", currency="BTC")
```

**Example link:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 4. `get_currencies()`

Retrieves a list of available currencies for rental payment.

**Signature:**
```python
async def get_currencies(self) -> MRRResponse[list[CurrencyInfo]]
```

**Returns:**
- `MRRResponse[list[CurrencyInfo]]` — response with currency list
  - On success: `MRRResponse(success=True, data=[CurrencyInfo, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `CurrencyInfo` contains:**
- `name` — currency name (BTC, LTC, ETH, DOGE, BCH)
- `enabled` — currency enabled status
- `txfee` — transaction fee for the currency

!!! note
    This method returns currencies available for rental payment on the platform, as opposed to `AccountClient.get_currencies()`, which returns currency statuses for a specific account.

**Usage Example:**
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

**Example link:** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

## Methods Summary Table

| # | Method | Description | Returns | Example |
|---|--------|-------------|---------|---------|
| 1 | `get_servers()` | MRR server list | `MRRResponse[ServersList]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 2 | `get_algos(currency)` | All mining algorithms | `MRRResponse[list[AlgoInfo]]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 3 | `get_algo(name, currency)` | Algorithm information | `MRRResponse[AlgoInfo]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 4 | `get_currencies()` | Available payment currencies | `MRRResponse[list[CurrencyInfo]]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |

---

## Additional Resources

- [Home Page](../../index.md)
- [Error Handling](../error-handling.md)
- [Data Models](../models.md)
- [Authentication](../authentication.md)
- [PricingClient](pricing.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

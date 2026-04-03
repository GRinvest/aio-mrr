# Pydantic Data Models

Complete reference of all Pydantic models in the `aio-mrr` library. Models are grouped by categories corresponding to the functional areas of the API.

---

## Table of Contents

- [Base Models](#base-models)
- [Account Models](#account-models)
- [Info Models](#info-models)
- [Pricing Models](#pricing-models)
- [Rental Models](#rental-models)
- [Rig Models](#rig-models)
- [Rig Group Models](#rig-group-models)
- [Request Body Models](#request-body-models)

---

## Base Models

### BaseMRRModel

Base model for all Pydantic models in the library. Uses the `extra="ignore"` configuration, making models resilient to API changes — additional fields returned by the API are ignored and do not cause validation errors.

```python
from pydantic import BaseModel, ConfigDict

class BaseMRRModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
```

---

### MRRResponseError

Error object returned on a failed request.

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Error type: `"network_error"`, `"api_error"`, `"validation_error"`, `"timeout"` |
| `message` | `str` | Human-readable error description |
| `details` | `dict[str, Any] \| None` | Additional error data |
| `http_status` | `int \| None` | HTTP status code (401, 429, 500, etc.) |

See also: [error-handling.md](./error-handling.md)

---

### MRRResponse[T]

Universal API response wrapper.

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | `True` if the request succeeded |
| `data` | `T \| None` | Typed data (`None` on error) |
| `error` | `MRRResponseError \| None` | Error object (`None` on success) |
| `http_status` | `int \| None` | HTTP status code of the response |
| `retry_count` | `int` | Number of retry attempts |

See also: [error-handling.md](./error-handling.md)

---

## Account Models

Models for working with account, profiles, pools, and transactions.

### AccountInfo

Detailed account information.

| Field | Type | Description |
|-------|------|-------------|
| `username` | `str` | Username |
| `email` | `str` | Email address |
| `withdraw` | `dict[str, WithdrawCurrencyInfo]` | Currency withdrawal information |
| `deposit` | `dict[str, DepositCurrencyInfo]` | Currency deposit information |
| `notifications` | `NotificationsInfo` | Notification settings |
| `settings` | `SettingsInfo` | Account settings |

---

### BalanceInfo

Balance information by currency.

| Field | Type | Description |
|-------|------|-------------|
| `confirmed` | `str` | Confirmed balance |
| `pending` | `float` | Pending balance |
| `unconfirmed` | `str` | Unconfirmed balance |

---

### Transaction

Transaction record.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Transaction ID |
| `type` | `str` | Transaction type |
| `currency` | `str \| None` | Transaction currency |
| `amount` | `str` | Transaction amount |
| `when` | `str` | Date/time (ISO format) |
| `rental` | `str \| None` | Rental ID (if applicable) |
| `rig` | `str \| None` | Rig ID (if applicable) |
| `txid` | `str \| None` | Blockchain transaction ID |
| `txfee` | `str \| None` | Transaction fee |
| `payout_address` | `str \| None` | Payout address |
| `sent` | `str \| None` | Sent amount |
| `status` | `str` | Transaction status |
| `pending_seconds` | `int \| None` | Seconds pending |
| `info` | `str \| None` | Additional information |

---

### TransactionsList

Transaction list with pagination metadata.

| Field | Type | Description |
|-------|------|-------------|
| `total` | `str` | Total number of transactions |
| `returned` | `int` | Number of returned records |
| `start` | `int` | Start position |
| `limit` | `int` | Record limit |
| `transactions` | `list[Transaction]` | List of transactions |

---

### Profile

User pool profile.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Profile ID |
| `name` | `str` | Profile name |
| `algo` | `AlgoProfileInfo` | Profile algorithm information |
| `pools` | `list[PoolProfileInfo] \| None` | List of pools in the profile (optional) |

---

### Pool

Saved pool information.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Pool ID |
| `type` | `str` | Connection type (e.g., `stratum+tcp`) |
| `name` | `str` | Pool name |
| `host` | `str` | Pool host |
| `port` | `int` | Pool port |
| `user` | `str` | Username/worker |
| `password` | `str` | Password (alias: `pass`) |
| `notes` | `str \| None` | Notes |
| `algo` | `AlgoPoolInfo \| None` | Algorithm information |

---

### PoolCreateBody

Request body for creating a pool.

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Connection type (required) |
| `name` | `str` | Pool name (required) |
| `host` | `str` | Pool host (required) |
| `port` | `int` | Pool port (required) |
| `user` | `str` | Username (required) |
| `password` | `str \| None` | Password (alias: `pass`) |
| `notes` | `str \| None` | Notes |

---

### PoolTestBody

Request body for testing a pool.

| Field | Type | Description |
|-------|------|-------------|
| `method` | `str` | Test method: `"simple"` or `"full"` (required) |
| `extramethod` | `str \| None` | Additional method |
| `type` | `str \| None` | Connection type |
| `host` | `str \| None` | Pool host |
| `port` | `int \| None` | Pool port |
| `user` | `str \| None` | Username |
| `password` | `str \| None` | Password (alias: `pass`) |
| `source` | `str \| None` | Test source |

---

### PoolTestResult

Pool test result.

| Field | Type | Description |
|-------|------|-------------|
| `result` | `list[PoolTestResultItem]` | Test results |
| `error` | `list[str]` | List of errors |

---

### PoolTestResultItem

Individual pool connection test result.

| Field | Type | Description |
|-------|------|-------------|
| `source` | `str` | Test source |
| `dest` | `str` | Connection destination |
| `error` | `str` | Connection error |
| `connection` | `bool` | Whether the connection was successful |
| `executiontime` | `float` | Execution time (sec) |
| `protocol` | `str \| None` | Protocol |
| `sub` | `bool \| None` | Subscription support |
| `auth` | `bool \| None` | Authorization successful |
| `red` | `bool \| None` | Red connection |
| `diffs` | `bool \| None` | Diff support |
| `diff` | `float \| None` | Differential |
| `work` | `bool \| None` | Work support |
| `xnonce` | `bool \| None` | Xnonce support |
| `ssl` | `bool \| None` | SSL connection |

---

### PoolCreateResponse

Response to pool creation.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Created pool ID |

---

### ProfileCreateBody

Request body for creating a profile.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Profile name (required) |
| `algo` | `str` | Algorithm (required) |

---

### ProfileCreateResponse

Response to profile creation.

| Field | Type | Description |
|-------|------|-------------|
| `pid` | `str` | Created profile ID |

---

### ProfileDeleteResponse

Response to profile deletion.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Deleted profile ID |
| `success` | `bool` | Deletion success |
| `message` | `str` | Result message |

---

### CurrencyStatus

Account currency status.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Currency name |
| `enabled` | `bool` | Currency is enabled |

---

### WithdrawCurrencyInfo

Currency withdrawal information.

| Field | Type | Description |
|-------|------|-------------|
| `address` | `str` | Withdrawal address |
| `label` | `str` | Currency label |
| `auto_pay_threshold` | `str` | Auto-pay threshold |
| `txfee` | `float` | Transaction fee |

---

### DepositCurrencyInfo

Currency deposit information.

| Field | Type | Description |
|-------|------|-------------|
| `address` | `str` | Deposit address |

---

### NotificationsInfo

Account notification settings.

| Field | Type | Description |
|-------|------|-------------|
| `rental_comm` | `str` | Rental comment notifications |
| `new_rental` | `str` | New rental notifications |
| `offline` | `str` | Offline notifications |
| `news` | `str` | News notifications |
| `deposit` | `str` | Deposit notifications |

---

### SettingsInfo

Account settings.

| Field | Type | Description |
|-------|------|-------------|
| `live_data` | `str` | Live data mode |
| `public_profile` | `str` | Public profile |
| `two_factor_auth` | `str` | Two-factor authentication |

---

### AlgoProfileInfo

Algorithm information in a profile.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Algorithm name |
| `display` | `str` | Display name |
| `suggested_price` | `PriceInfo` | Suggested price |

---

### PoolProfileInfo

Pool information in a profile.

| Field | Type | Description |
|-------|------|-------------|
| `priority` | `int` | Pool priority (0-4) |
| `type` | `str` | Connection type |
| `host` | `str` | Pool host |
| `port` | `str` | Pool port |
| `user` | `str` | Username |
| `password` | `str` | Password (alias: `pass`) |
| `status` | `str` | Pool status |

---

### AlgoPoolInfo

Pool algorithm information.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Algorithm name |
| `display` | `str` | Display name |

---

## Info Models

Models for obtaining information about servers, algorithms, and currencies.

### AlgoInfo

Mining algorithm information.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Algorithm name |
| `display` | `str` | Display name |
| `suggested_price` | `PriceInfo` | Suggested price |
| `stats` | `AlgoStats` | Algorithm statistics |

---

### AlgoStats

Mining algorithm statistics.

| Field | Type | Description |
|-------|------|-------------|
| `available` | `AvailableHashInfo` | Available hash power |
| `rented` | `RentedHashInfo` | Rented hash power |
| `prices` | `PricesInfo` | Price information |

---

### AvailableHashInfo

Available hash power.

| Field | Type | Description |
|-------|------|-------------|
| `rigs` | `str` | Number of rigs |
| `hash` | `HashInfo` | Hashrate information |

---

### RentedHashInfo

Rented hash power.

| Field | Type | Description |
|-------|------|-------------|
| `rigs` | `str` | Number of rigs |
| `hash` | `HashInfo` | Hashrate information |

---

### PricesInfo

Price information.

| Field | Type | Description |
|-------|------|-------------|
| `lowest` | `PriceInfo` | Lowest price |
| `last_10` | `PriceInfo` | Price of the last 10 rentals |
| `last` | `PriceInfo` | Last price |

---

### PriceInfo

Price information.

| Field | Type | Description |
|-------|------|-------------|
| `amount` | `str` | Price amount |
| `currency` | `str` | Price currency |
| `unit` | `str` | Unit of measurement |

---

### HashInfo

Hashrate information.

| Field | Type | Description |
|-------|------|-------------|
| `hash` | `float` | Hashrate value |
| `unit` | `str` | Unit of measurement |
| `nice` | `str` | Pretty-formatted string |

---

### ServerInfo

MRR server information.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Server ID |
| `name` | `str` | Server name |
| `region` | `str` | Region |
| `port` | `str \| None` | Port (general) |
| `ethereum_port` | `str \| None` | Ethereum port |

---

### ServersList

List of MRR servers.

| Field | Type | Description |
|-------|------|-------------|
| `servers` | `list[ServerInfo]` | List of servers |

---

### CurrencyInfo

Payment currency information.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Currency name |
| `enabled` | `bool` | Currency is enabled |
| `txfee` | `str` | Transaction fee |

---

## Pricing Models

Models for obtaining conversion rates and market prices.

### PricingInfo

General pricing information.

| Field | Type | Description |
|-------|------|-------------|
| `conversion_rates` | `ConversionRates` | Currency conversion rates |
| `market_rates` | `MarketRates` | Market prices by algorithm |

---

### ConversionRates

Conversion rates between cryptocurrencies.

| Field | Type | Description |
|-------|------|-------------|
| `LTC` | `str` | LTC rate |
| `ETH` | `str` | ETH rate |
| `BCH` | `str` | BCH rate |
| `DOGE` | `str` | DOGE rate |

---

### MarketRate

Market price for an algorithm by currency.

| Field | Type | Description |
|-------|------|-------------|
| `BTC` | `str` | Price in BTC |
| `LTC` | `str` | Price in LTC |
| `ETH` | `str` | Price in ETH |
| `BCH` | `str` | Price in BCH |
| `DOGE` | `str` | Price in DOGE |

---

### MarketRates

Market prices for all algorithms.

| Field | Type | Description |
|-------|------|-------------|
| `allium` | `MarketRate` | Price for allium |
| `argon2dchukwa` | `MarketRate` | Price for argon2dchukwa |
| `autolykosv2` | `MarketRate` | Price for autolykosv2 |
| `kawpow` | `MarketRate` | Price for kawpow |
| `kheavyhash` | `MarketRate` | Price for kheavyhash |
| `randomx` | `MarketRate` | Price for randomx |
| `scrypt` | `MarketRate` | Price for scrypt |
| `sha256` | `MarketRate` | Price for sha256 |
| `x11` | `MarketRate` | Price for x11 |

---

## Rental Models

Models for working with rentals.

### RentalInfo

Rental information.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Rental ID |
| `rig_id` | `str \| None` | Rig ID (optional) |
| `rig_name` | `str \| None` | Rig name |
| `owner` | `str \| None` | Rig owner |
| `renter` | `str \| None` | Renter |
| `status` | `str \| None` | Rental status |
| `started` | `str \| None` | Start time |
| `ends` | `str \| None` | End time |
| `length` | `float \| None` | Duration (hours) |
| `currency` | `str \| None` | Payment currency |
| `rate` | `RateInfo \| None` | Rate information |
| `hash` | `RentalHashInfo \| None` | Hashrate information |
| `cost` | `RentalCostInfo \| None` | Cost information |

---

### RentalLogEntry

Rental log entry.

| Field | Type | Description |
|-------|------|-------------|
| `time` | `str` | Event time |
| `message` | `str` | Event message |

---

### RentalMessage

Rental message.

| Field | Type | Description |
|-------|------|-------------|
| `time` | `str` | Message time |
| `user` | `str` | Sender |
| `message` | `str` | Message text |

---

### GraphData

Rental hashrate graph data.

| Field | Type | Description |
|-------|------|-------------|
| `hashrate_data` | `list[GraphDataPoint] \| None` | Hashrate data |
| `downtime_data` | `list[GraphDataPoint] \| None` | Downtime data |
| `hours` | `float \| None` | Number of hours |

---

### GraphDataPoint

Graph data point.

| Field | Type | Description |
|-------|------|-------------|
| `time` | `str \| None` | Point time |
| `hashrate` | `float \| None` | Hashrate at point |
| `downtime` | `bool \| None` | Downtime at point |

---

### RateInfo

Rental rate information.

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str \| None` | Rate type (alias: `rate.type`) |
| `price` | `str \| None` | Rate price (alias: `rate.price`) |

---

### RentalHashInfo

Rental hashrate information.

| Field | Type | Description |
|-------|------|-------------|
| `hash` | `float \| None` | Hashrate value |
| `type` | `str \| None` | Algorithm type |

---

### RentalCostInfo

Rental cost information.

| Field | Type | Description |
|-------|------|-------------|
| `amount` | `str \| None` | Cost amount |
| `currency` | `str \| None` | Cost currency |

---

### RentalCreateBody

Request body for creating a rental.

| Field | Type | Description |
|-------|------|-------------|
| `rig` | `int` | Rig ID (required) |
| `length` | `float` | Duration in hours (required) |
| `profile` | `int` | Profile ID (required) |
| `currency` | `str \| None` | Payment currency |
| `rate_type` | `str \| None` | Rate type (alias: `rate.type`) |
| `rate_price` | `float \| None` | Rate price (alias: `rate.price`) |

---

### RentalPoolBody

Request body for updating a rental pool.

| Field | Type | Description |
|-------|------|-------------|
| `host` | `str` | Pool host (required) |
| `port` | `int` | Pool port (required) |
| `user` | `str` | Username (required) |
| `password` | `str` | Password (alias: `pass`, required) |
| `priority` | `int \| None` | Pool priority |

---

## Rig Models

Models for working with rigs.

### RigInfo

Rig information.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Rig ID |
| `name` | `str` | Rig name |
| `description` | `str \| None` | Rig description |
| `server` | `str \| None` | Rig server |
| `status` | `dict[str, Any] \| str \| None` | Rig status (can be a string or dictionary) |
| `price` | `dict[str, RigPriceInfo] \| None` | Price information (by currency) |
| `price_type` | `str \| None` | Price type (alias: `price.type`) |
| `minhours` | `float \| None` | Minimum rental time |
| `maxhours` | `float \| None` | Maximum rental time |
| `extensions` | `bool \| None` | Extension capability |
| `hash` | `RigHashInfo \| None` | Hashrate information |
| `suggested_diff` | `float \| None` | Suggested difficulty |
| `ndevices` | `int \| None` | Number of devices |
| `type` | `str \| None` | Rig type |
| `region` | `str \| None` | Region |
| `online` | `bool \| None` | Online status |
| `rented` | `bool \| None` | Rented out |
| `last_hashrate` | `float \| None` | Last hashrate |
| `rpi` | `int \| None` | RPI index |
| `owner` | `str \| None` | Owner |

---

### RigPortInfo

Rig server port information.

| Field | Type | Description |
|-------|------|-------------|
| `rigid` | `str \| None` | Rig ID (optional) |
| `port` | `int` | Server port |
| `server` | `str \| None` | Server name (optional) |
| `worker` | `str \| None` | Worker name for connection (optional) |

---

### RigThreadInfo

Information about rig worker threads (grouped by rigs).

Response for GET /rig/{ids}/threads returns a list of rig groups with their threads.

| Field | Type | Description |
|-------|------|-------------|
| `rigid` | `str \| None` | Rig ID |
| `access` | `str \| None` | Access level (owner/renter) |
| `threads` | `list[RigThreadDetail]` | List of thread details |

### RigThreadDetail

Details of a single rig thread.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int \| None` | Thread ID |
| `worker` | `str \| None` | Worker name |
| `status` | `str \| None` | Thread status |
| `hashrate` | `float \| None` | Thread hashrate |
| `last_share` | `str \| None` | Time of last share |

---

### RigGraphData

Rig hashrate graph data.

Response for GET /rig/{ids}/graph returns data in the new format with chartdata.

| Field | Type | Description |
|-------|------|-------------|
| `rigid` | `str \| None` | Rig ID |
| `chartdata` | `dict[str, Any] \| None` | Graph data (time_start, time_end, timestamp_start, timestamp_end, bars) |

**`chartdata` structure:**

| Field | Type | Description |
|-------|------|-------------|
| `time_start` | `str` | Start of time range |
| `time_end` | `str` | End of time range |
| `timestamp_start` | `int` | Start timestamp |
| `timestamp_end` | `int` | End timestamp |
| `bars` | `str` | Data in "[ts,val],[ts,val],..." format |

---

### RigGraphDataPoint

Rig graph data point.

| Field | Type | Description |
|-------|------|-------------|
| `time` | `str` | Point time |
| `hashrate` | `float \| None` | Hashrate at point |
| `downtime` | `bool \| None` | Downtime at point |

---

### RigPriceInfo

Rig price information by currency.

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | `bool \| None` | Currency is enabled |
| `price` | `float \| None` | Price |
| `autoprice` | `bool \| None` | Automatic pricing |
| `minimum` | `float \| None` | Minimum price |
| `modifier` | `str \| None` | Price modifier |

---

### RigHashInfo

Rig hashrate information.

| Field | Type | Description |
|-------|------|-------------|
| `hash` | `float \| None` | Hashrate value |
| `type` | `str \| None` | Algorithm type |

---

### RigCreateBody

Request body for creating a rig.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Rig name (required) |
| `description` | `str \| None` | Rig description |
| `status` | `str \| None` | Rig status |
| `server` | `str` | Rig server (required) |
| `price_btc_enabled` | `bool \| None` | BTC enabled (alias: `price.btc.enabled`) |
| `price_btc_price` | `float \| None` | BTC price (alias: `price.btc.price`) |
| `price_btc_autoprice` | `bool \| None` | BTC auto-price (alias: `price.btc.autoprice`) |
| `price_btc_minimum` | `float \| None` | BTC min. price (alias: `price.btc.minimum`) |
| `price_btc_modifier` | `str \| None` | BTC modifier (alias: `price.btc.modifier`) |
| `price_ltc_enabled` | `bool \| None` | LTC enabled (alias: `price.ltc.enabled`) |
| `price_eth_enabled` | `bool \| None` | ETH enabled (alias: `price.eth.enabled`) |
| `price_doge_enabled` | `bool \| None` | DOGE enabled (alias: `price.doge.enabled`) |
| `price_type` | `str \| None` | Price type (alias: `price.type`) |
| `minhours` | `float \| None` | Minimum time |
| `maxhours` | `float \| None` | Maximum time |
| `extensions` | `bool \| None` | Extension capability |
| `hash_hash` | `float \| None` | Hashrate (alias: `hash.hash`) |
| `hash_type` | `str \| None` | Algorithm type (alias: `hash.type`) |
| `suggested_diff` | `float \| None` | Suggested difficulty |
| `ndevices` | `int \| None` | Number of devices |

---

### RigBatchBody

Request body for batch updating rigs.

| Field | Type | Description |
|-------|------|-------------|
| `rigs` | `list[dict[str, object]]` | List of rigs to update (required) |

---

### RigPoolBody

Request body for updating a rig pool.

| Field | Type | Description |
|-------|------|-------------|
| `host` | `str` | Pool host (required) |
| `port` | `int` | Pool port (required) |
| `user` | `str` | Username (required) |
| `password` | `str` | Password (alias: `pass`, required) |
| `priority` | `int \| None` | Pool priority |

---

## Rig Group Models

Models for working with rig groups.

### RigGroupInfo

Rig group information.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Group ID |
| `name` | `str` | Group name |
| `enabled` | `bool` | Group is enabled |
| `rental_limit` | `int` | Rental limit |
| `rigs` | `list[int]` | List of rig IDs in the group |
| `algo` | `str \| None` | Group algorithm |

---

### RigGroupCreateBody

Request body for creating a rig group.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Group name (required) |
| `enabled` | `bool` | Enable group (default `True`) |
| `rental_limit` | `int` | Rental limit (default `1`) |

---

### RigGroupUpdateBody

Request body for updating a rig group.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str \| None` | New group name |
| `enabled` | `bool \| None` | New enabled status |
| `rental_limit` | `int \| None` | New rental limit |

---

## Request Body Models

Additional models for request parameters.

### TransactionsQueryParams

Query parameters for retrieving transactions.

| Field | Type | Description |
|-------|------|-------------|
| `start` | `int \| None` | Start position |
| `limit` | `int \| None` | Record limit |
| `algo` | `str \| None` | Filter by algorithm |
| `type` | `str \| None` | Filter by type |
| `rig` | `int \| None` | Filter by rig |
| `rental` | `int \| None` | Filter by rental |
| `txid` | `str \| None` | Filter by txid |
| `time_greater_eq` | `str \| None` | Time >= (ISO) |
| `time_less_eq` | `str \| None` | Time <= (ISO) |

---

## See Also

- [« Back to Home](./index.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

# AccountClient — API Reference

Reference for all `AccountClient` methods for working with MiningRigRentals account: managing balance, transactions, pool profiles, saved pools, and currency statuses.

## Overview

`AccountClient` provides methods for:
- Retrieving account information and balances
- Viewing transaction history
- CRUD operations on pool profiles
- CRUD operations on saved pools
- Testing pool connections
- Viewing currency statuses

---

## Methods

### 1. `get_account()`

Retrieves detailed information about the user account.

**Signature:**
```python
async def get_account(self) -> MRRResponse[AccountInfo]
```

**Returns:**
- `MRRResponse[AccountInfo]` — response with account information
  - On success: `MRRResponse(success=True, data=AccountInfo)`
  - On error: `MRRResponse(success=False, error=...)`

**What `AccountInfo` contains:**
- `username` — username
- `email` — email address
- `withdraw` — withdrawal addresses by currency
- `deposit` — deposit addresses by currency
- `notifications` — notification settings
- `settings` — account settings

**Usage Example:**
```python
response = await client.account.get_account()
if response.success:
    print(f"Username: {response.data.username}")
    print(f"Email: {response.data.email}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

### 2. `get_balance()`

Retrieves account balances for all currencies.

**Signature:**
```python
async def get_balance(self) -> MRRResponse[dict[str, BalanceInfo]]
```

**Returns:**
- `MRRResponse[dict[str, BalanceInfo]]` — response with balances by currency
  - On success: `MRRResponse(success=True, data={"BTC": BalanceInfo, "LTC": BalanceInfo, ...})`
  - On error: `MRRResponse(success=False, error=...)`

**What `BalanceInfo` contains:**
- `confirmed` — confirmed balance (string)
- `pending` — pending balance (float)
- `unconfirmed` — unconfirmed balance (string)

!!! note
    Balances are updated in real time when funds are received.

**Usage Example:**
```python
response = await client.account.get_balance()
if response.success:
    for currency, balance in response.data.items():
        print(f"{currency}: confirmed={balance.confirmed}, pending={balance.pending}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/01_quickstart.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/01_quickstart.py)

---

### 3. `get_transactions()`

Retrieves account transaction history with filtering capability.

**Signature:**
```python
async def get_transactions(params: TransactionsQueryParams | None = None) -> MRRResponse[TransactionsList]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `params` | `TransactionsQueryParams \| None` | No | Filter parameters. Returns all transactions by default (limit=100). |

**`TransactionsQueryParams` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start` | `int \| None` | No | Pagination start (default 0) |
| `limit` | `int \| None` | No | Record limit (default 100) |
| `algo` | `str \| None` | No | Filter by algorithm |
| `type` | `str \| None` | No | Transaction type (credit, payout, referral, deposit, payment, credit/refund, debit/refund, rental fee) |
| `rig` | `int \| None` | No | Filter by rig ID |
| `rental` | `int \| None` | No | Filter by rental ID |
| `txid` | `str \| None` | No | Filter by txid |
| `time_greater_eq` | `str \| None` | No | Time >= (Unix timestamp) |
| `time_less_eq` | `str \| None` | No | Time <= (Unix timestamp) |

**Returns:**
- `MRRResponse[TransactionsList]` — response with transaction list
  - On success: `MRRResponse(success=True, data=TransactionsList)`
  - On error: `MRRResponse(success=False, error=...)`

**What `TransactionsList` contains:**
- `total` — total number of transactions (string)
- `returned` — number of returned records
- `start` — start position
- `limit` — record limit
- `transactions` — list of `Transaction` objects

**Usage Example:**
```python
# Get the last 10 credits
params = TransactionsQueryParams(type="credit", limit=10)
response = await client.account.get_transactions(params)
if response.success:
    for tx in response.data.transactions:
        print(f"{tx.type}: {tx.amount} ({tx.when})")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

### 4. `get_profiles()`

Retrieves a list of all pool profiles or filters by algorithm.

**Signature:**
```python
async def get_profiles(algo: str | None = None) -> MRRResponse[list[Profile]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `algo` | `str \| None` | No | Filter by algorithm (e.g., "scrypt", "sha256"). Returns all profiles by default. |

**Returns:**
- `MRRResponse[list[Profile]]` — response with profile list
  - On success: `MRRResponse(success=True, data=[Profile, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `Profile` contains:**
- `id` — profile identifier
- `name` — profile name
- `algo` — algorithm information (`AlgoProfileInfo`)
- `pools` — list of pools (`list[PoolProfileInfo]`) with priorities

**Usage Example:**
```python
# Get all profiles
response = await client.account.get_profiles()
if response.success:
    for profile in response.data:
        print(f"{profile.name}: {len(profile.pools)} pools")
        for pool in profile.pools:
            print(f"  - {pool.host}:{pool.port} (priority {pool.priority})")

# Get profiles only for scrypt
response = await client.account.get_profiles(algo="scrypt")
```

**Example link:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 5. `create_profile()`

Creates a new pool profile for the specified algorithm.

**Signature:**
```python
async def create_profile(body: ProfileCreateBody) -> MRRResponse[ProfileCreateResponse]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `body` | `ProfileCreateBody` | Yes | Request body with profile name and algorithm |

**`ProfileCreateBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Profile name |
| `algo` | `str` | Yes | Profile algorithm (e.g., "scrypt", "sha256") |

**Returns:**
- `MRRResponse[ProfileCreateResponse]` — response with created profile ID
  - On success: `MRRResponse(success=True, data=ProfileCreateResponse)`
  - On error: `MRRResponse(success=False, error=...)`

**What `ProfileCreateResponse` contains:**
- `pid` — created profile identifier (string)

**Usage Example:**
```python
body = ProfileCreateBody(name="My Scrypt Profile", algo="scrypt")
response = await client.account.create_profile(body)
if response.success:
    print(f"Profile created with ID: {response.data.pid}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 6. `get_profile()`

Retrieves a specific pool profile by ID.

**Signature:**
```python
async def get_profile(pid: int) -> MRRResponse[Profile]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `pid` | `int` | Yes | Profile identifier |

**Returns:**
- `MRRResponse[Profile]` — response with profile information
  - On success: `MRRResponse(success=True, data=Profile)`
  - On error: `MRRResponse(success=False, error=...)`

**Usage Example:**
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

**Example link:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 7. `update_profile()`

Adds or replaces a pool in a profile with a specified priority.

**Signature:**
```python
async def update_profile(pid: int, poolid: int, priority: int | None = None) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `pid` | `int` | Yes | Profile identifier |
| `poolid` | `int` | Yes | Pool ID to add |
| `priority` | `int \| None` | No | Pool priority (0-4). If not specified, the pool is added to the first available priority. |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! note
    Priority 0 has the highest value. Pools with lower priority numbers are processed first.

**Usage Example:**
```python
# Add pool at priority 0
response = await client.account.update_profile(pid=40073, poolid=98708, priority=0)
if response.success:
    print("Pool added to profile at priority 0")
else:
    print(f"Error: {response.error.message}")

# Add pool without specifying priority (auto-select)
response = await client.account.update_profile(pid=40073, poolid=98708)
```

**Example link:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 8. `update_profile_priority()`

Adds a pool to a specific priority position in a profile.

**Signature:**
```python
async def update_profile_priority(pid: int, priority: int, poolid: int) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `pid` | `int` | Yes | Profile identifier |
| `priority` | `int` | Yes | Pool priority (0-4) |
| `poolid` | `int` | Yes | Pool ID to add |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! warning
    Priority must be in the range 0-4. Values outside this range will cause an API error.

**Usage Example:**
```python
response = await client.account.update_profile_priority(pid=41818, priority=0, poolid=98708)
if response.success:
    print("Pool added at priority 0")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 9. `delete_profile()`

Deletes a pool profile by ID.

**Signature:**
```python
async def delete_profile(pid: int) -> MRRResponse[ProfileDeleteResponse]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `pid` | `int` | Yes | Profile identifier to delete |

**Returns:**
- `MRRResponse[ProfileDeleteResponse]` — response with deletion result
  - On success: `MRRResponse(success=True, data=ProfileDeleteResponse)`
  - On error: `MRRResponse(success=False, error=...)`

**What `ProfileDeleteResponse` contains:**
- `id` — deleted profile identifier
- `success` — deletion success status
- `message` — result message

**Usage Example:**
```python
response = await client.account.delete_profile(pid=42281)
if response.success:
    print(f"Deleted: {response.data.message}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 10. `get_pools()`

Retrieves a list of all saved pools for the account.

**Signature:**
```python
async def get_pools(self) -> MRRResponse[list[Pool]]
```

**Returns:**
- `MRRResponse[list[Pool]]` — response with pool list
  - On success: `MRRResponse(success=True, data=[Pool, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `Pool` contains:**
- `id` — pool identifier
- `type` — algorithm (sha256, scrypt, x11, etc.)
- `name` — pool name
- `host` — pool host
- `port` — pool port
- `user` — username/worker
- `password` — password
- `notes` — notes (optional)
- `algo` — algorithm information (optional)

**Usage Example:**
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

**Example link:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 11. `get_pools_by_ids()`

Retrieves specific pools by their IDs.

**Signature:**
```python
async def get_pools_by_ids(ids: list[int]) -> MRRResponse[list[Pool]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of pool identifiers |

**Returns:**
- `MRRResponse[list[Pool]]` — response with pool list
  - On success: `MRRResponse(success=True, data=[Pool, ...])`
  - On error: `MRRResponse(success=False, error=...)`

!!! note
    Pools are separated by semicolons in the request URL (`/account/pool/12345;12346`).

**Usage Example:**
```python
response = await client.account.get_pools_by_ids(ids=[12345, 12346])
if response.success:
    for pool in response.data:
        print(f"ID: {pool.id}, Type: {pool.type}, Name: {pool.name}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 12. `create_pool()`

Creates a new saved pool.

**Signature:**
```python
async def create_pool(body: PoolCreateBody) -> MRRResponse[PoolCreateResponse]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `body` | `PoolCreateBody` | Yes | Request body with pool parameters |

**`PoolCreateBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | `str` | Yes | Pool algorithm (sha256, scrypt, x11, etc.) |
| `name` | `str` | Yes | Name to identify the pool |
| `host` | `str` | Yes | Pool host |
| `port` | `int` | Yes | Pool port |
| `user` | `str` | Yes | Worker name |
| `password` | `str \| None` | No | Worker password |
| `notes` | `str \| None` | No | Pool notes |

**Returns:**
- `MRRResponse[PoolCreateResponse]` — response with created pool ID
  - On success: `MRRResponse(success=True, data=PoolCreateResponse)`
  - On error: `MRRResponse(success=False, error=...)`

**What `PoolCreateResponse` contains:**
- `id` — created pool identifier (int)

**Usage Example:**
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

**Example link:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 13. `update_pools()`

Updates parameters of existing pools by their IDs.

**Signature:**
```python
async def update_pools(ids: list[int], body: dict[str, Any]) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of pool identifiers to update |
| `body` | `dict[str, Any]` | Yes | Request body with new pool parameters |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

**Valid fields in `body`:**
- `name` — new pool name
- `host` — new host
- `port` — new port
- `user` — new username
- `password` — new password
- `notes` — new notes

!!! note
    You can update only the fields you need. Unspecified fields remain unchanged.

**Usage Example:**
```python
# Update name and host
body = {"name": "Updated Pool Name", "host": "new.pool.com"}
response = await client.account.update_pools(ids=[12345], body=body)
if response.success:
    print("Pool updated")
else:
    print(f"Error: {response.error.message}")

# Batch update multiple pools
response = await client.account.update_pools(ids=[12345, 12346], body={"notes": "Updated notes"})
```

**Example link:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 14. `delete_pools()`

Deletes saved pools by their IDs.

**Signature:**
```python
async def delete_pools(ids: list[int]) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of pool identifiers to delete |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! warning
    Pool deletion is irreversible. Make sure the pools are not used in active profiles or rentals.

**Usage Example:**
```python
response = await client.account.delete_pools(ids=[12345, 12346])
if response.success:
    print("Pools deleted successfully")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 15. `test_pool()`

Tests pool connection from different MRR servers.

**Signature:**
```python
async def test_pool(body: PoolTestBody) -> MRRResponse[PoolTestResult]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `body` | `PoolTestBody` | Yes | Request body with test parameters |

**`PoolTestBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | `str` | Yes | Test method: `"simple"` (connection only) or `"full"` (with authentication) |
| `extramethod` | `str \| None` | No | For ethhash: `[esm0,esm1,esm2,esm3]`. Default `esm0`. |
| `type` | `str \| None` | No | Algorithm (scrypt, sha256, x11). Required for `full` method. |
| `host` | `str \| None` | No | Pool host (may include port) |
| `port` | `int \| None` | No | Pool port. Required if not in `host`. |
| `user` | `str \| None` | No | Username. Required for `full` method. |
| `password` | `str \| None` | No | Password. Required for `full` method. |
| `source` | `str \| None` | No | MRR server for testing. Default `us-central01`. |

**Returns:**
- `MRRResponse[PoolTestResult]` — response with test results
  - On success: `MRRResponse(success=True, data=PoolTestResult)`
  - On error: `MRRResponse(success=False, error=...)`

**What `PoolTestResult` contains:**
- `result` — list of `PoolTestResultItem` with test results from different servers
- `error` — list of errors (if any)

**What `PoolTestResultItem` contains:**
- `source` — MRR server from which the test was conducted
- `dest` — pool address (host:port)
- `error` — error description (empty string on success)
- `connection` — whether the connection was successful
- `executiontime` — test execution time (seconds)
- `protocol` — protocol (stratum, etc.)
- `sub` — whether subscription was successful
- `auth` — whether authentication was successful
- `diff` — received difficulty
- `xnonce` — xnonce support
- `ssl` — SSL usage

!!! note
    - **Simple test**: checks only the connection to the pool port.
    - **Full test**: checks connection, subscription, authentication, and work reception.

**Usage Example:**
```python
# Simple test (connection only)
body = PoolTestBody(method="simple", host="de.minexmr.com:4444")
response = await client.account.test_pool(body)
if response.success:
    for item in response.data.result:
        status = "OK" if item.connection else f"FAILED: {item.error}"
        print(f"{item.source} -> {item.dest}: {status} ({item.executiontime}s)")

# Full test (with authentication)
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

**Example link:** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 16. `get_currencies()`

Retrieves a list of currencies with enabled status for the account.

**Signature:**
```python
async def get_currencies(self) -> MRRResponse[list[CurrencyStatus]]
```

**Returns:**
- `MRRResponse[list[CurrencyStatus]]` — response with currency list
  - On success: `MRRResponse(success=True, data=[CurrencyStatus, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `CurrencyStatus` contains:**
- `name` — currency name (BTC, LTC, ETH, DOGE, BCH)
- `enabled` — enabled status for the account

**Usage Example:**
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

**Example link:** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

## Methods Summary Table

| # | Method | Description | Returns | Example |
|---|--------|-------------|---------|---------|
| 1 | `get_account()` | Account information | `MRRResponse[AccountInfo]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |
| 2 | `get_balance()` | Balances by currency | `MRRResponse[dict[str, BalanceInfo]]` | [01_quickstart.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/01_quickstart.py) |
| 3 | `get_transactions(params)` | Transaction history | `MRRResponse[TransactionsList]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |
| 4 | `get_profiles(algo)` | All pool profiles | `MRRResponse[list[Profile]]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 5 | `create_profile(body)` | Create profile | `MRRResponse[ProfileCreateResponse]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 6 | `get_profile(pid)` | Profile by ID | `MRRResponse[Profile]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 7 | `update_profile(pid, poolid, priority)` | Add/replace pool in profile | `MRRResponse[None]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 8 | `update_profile_priority(pid, priority, poolid)` | Set pool priority | `MRRResponse[None]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 9 | `delete_profile(pid)` | Delete profile | `MRRResponse[ProfileDeleteResponse]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 10 | `get_pools()` | All saved pools | `MRRResponse[list[Pool]]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 11 | `get_pools_by_ids(ids)` | Pools by ID | `MRRResponse[list[Pool]]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 12 | `create_pool(body)` | Create pool | `MRRResponse[PoolCreateResponse]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 13 | `update_pools(ids, body)` | Update pools | `MRRResponse[None]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 14 | `delete_pools(ids)` | Delete pools | `MRRResponse[None]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 15 | `test_pool(body)` | Test pool | `MRRResponse[PoolTestResult]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 16 | `get_currencies()` | Currency statuses | `MRRResponse[list[CurrencyStatus]]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |

---

## Additional Resources

- [Home Page](../../index.md)
- [Error Handling](../error-handling.md)
- [Data Models](../models.md)
- [Authentication](../authentication.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

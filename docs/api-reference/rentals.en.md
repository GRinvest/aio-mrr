# RentalClient — API Reference

Reference for all `RentalClient` methods for working with mining rig rentals on MiningRigRentals: creating rentals, managing pools, extending, retrieving statistics, graph data, and logs.

## Overview

`RentalClient` provides methods for:
- Retrieving rental lists with filtering
- Creating and managing rentals
- Applying pool profiles to rentals
- Managing rental pools
- Extending rentals
- Retrieving graph data, logs, and messages

---

## Methods

### 1. `get_list(params)`

Retrieves a list of rentals with filtering and pagination.

**Signature:**
```python
async def get_list(params: dict[str, Any] | None = None) -> MRRResponse[list[RentalInfo]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `params` | `dict[str, Any] \| None` | No | Query parameters for filtering. Returns all rentals by default. |

**Filtering parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | `str \| None` | No | `'owner'` or `'renter'` — filter by role |
| `algo` | `str \| None` | No | Filter by mining algorithm |
| `history` | `bool \| None` | No | `true` = completed rentals, `false` = active |
| `rig` | `int \| None` | No | Filter by rig ID |
| `start` | `int \| None` | No | Pagination start (default 0) |
| `limit` | `int \| None` | No | Record limit (default 100) |
| `currency` | `str \| None` | No | Payment currency: `BTC`, `LTC`, `ETH`, `DOGE`, `BCH` |

**Returns:**
- `MRRResponse[list[RentalInfo]]` — response with rental list
  - On success: `MRRResponse(success=True, data=[RentalInfo, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `RentalInfo` contains:**
- `id` — rental identifier
- `rig_id` — rig identifier
- `rig_name` — rig name (optional)
- `owner` — rig owner
- `renter` — renter
- `status` — rental status
- `started` — start time
- `ends` — end time
- `length` — duration in hours
- `currency` — payment currency
- `rate` — rate information (`RateInfo`)
- `hash` — hashrate information (`RentalHashInfo`)
- `cost` — rental cost (`RentalCostInfo`)

**Usage Example:**
```python
# Get active rentals as renter
response = await client.rental.get_list(params={"type": "renter", "history": False})
if response.success:
    for rental in response.data:
        print(f"Rental {rental.id}: {rental.status}, ends: {rental.ends}")
else:
    print(f"Error: {response.error.message}")

# Get completed rentals with pagination
response = await client.rental.get_list(params={"type": "owner", "history": True, "start": 0, "limit": 10})
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 2. `get_by_ids(ids)`

Retrieves rental information by ID.

**Signature:**
```python
async def get_by_ids(ids: list[int]) -> MRRResponse[RentalInfo]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to retrieve (first ID is used) |

**Returns:**
- `MRRResponse[RentalInfo]` — response with rental information
  - On success: `MRRResponse(success=True, data=RentalInfo)`
  - On error: `MRRResponse(success=False, error=...)`

!!! note
    If a list of multiple IDs is passed, only the first ID is used to retrieve rental information.

**Usage Example:**
```python
response = await client.rental.get_by_ids(ids=[54321])
if response.success:
    rental = response.data
    print(f"Rental ID: {rental.id}")
    print(f"Rig ID: {rental.rig_id}")
    print(f"Status: {rental.status}")
    print(f"Owner: {rental.owner}")
    print(f"Renter: {rental.renter}")
    print(f"Currency: {rental.currency}")
    print(f"Length: {rental.length} hours")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 3. `create(body)`

Creates a new rental.

**Signature:**
```python
async def create(body: RentalCreateBody) -> MRRResponse[dict[str, Any]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `body` | `RentalCreateBody` | Yes | Request body with rental creation parameters |

**`RentalCreateBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `rig` | `int` | Yes | Rig ID for rental |
| `length` | `float` | Yes | Rental duration in hours |
| `profile` | `int` | Yes | Pool profile ID to use |
| `currency` | `str \| None` | No | Payment currency (default `BTC`) |
| `rate_type` | `str \| None` | No | Hash type (default `'mh'`) |
| `rate_price` | `float \| None` | No | Price per hash unit per day |

**Returns:**
- `MRRResponse[dict[str, Any]]` — response with created rental ID and cost
  - On success: `MRRResponse(success=True, data={"id": "54321", "cost": "0.02000000"})`
  - On error: `MRRResponse(success=False, error=...)`

**Usage Example:**
```python
from aio_mrr.models.rental.request import RentalCreateBody

body = RentalCreateBody(
    rig=12345,
    length=24.0,
    profile=678,
    currency="BTC",
    rate_type="mh",
    rate_price=0.005
)
response = await client.rental.create(body)
if response.success:
    print(f"Rental created with ID: {response.data['id']}")
    print(f"Cost: {response.data['cost']}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 4. `update_profile(ids, profile)`

Applies a pool profile to rentals.

**Signature:**
```python
async def update_profile(ids: list[int], profile: int) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to update |
| `profile` | `int` | Yes | Profile ID to apply |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! note
    The pool profile determines the set of pools with priorities that will be used for mining on the rental.

**Usage Example:**
```python
# Apply profile to a single rental
response = await client.rental.update_profile(ids=[54321], profile=678)
if response.success:
    print("Profile applied successfully")
else:
    print(f"Error: {response.error.message}")

# Apply profile to multiple rentals
response = await client.rental.update_profile(ids=[54321, 54322, 54323], profile=678)
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 5. `get_pools(ids)`

Retrieves pools assigned to rentals.

**Signature:**
```python
async def get_pools(ids: list[int]) -> MRRResponse[list[Pool]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to get pools for |

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
response = await client.rental.get_pools(ids=[54321])
if response.success:
    for pool in response.data:
        print(f"Pool: {pool.name}")
        print(f"  Type: {pool.type}")
        print(f"  Host: {pool.host}:{pool.port}")
        print(f"  User: {pool.user}")
        if pool.notes:
            print(f"  Notes: {pool.notes}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 6. `update_pool(ids, body)`

Adds or replaces a pool on rentals.

**Signature:**
```python
async def update_pool(ids: list[int], body: RentalPoolBody) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to update |
| `body` | `RentalPoolBody` | Yes | Request body with pool data |

**`RentalPoolBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `host` | `str` | Yes | Pool host |
| `port` | `int` | Yes | Pool port |
| `user` | `str` | Yes | Worker name |
| `password` | `str` | Yes | Worker password |
| `priority` | `int \| None` | No | Pool priority (0-4) |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! note
    If a pool with the same priority already exists, it will be replaced. Priority 0 has the highest value.

**Usage Example:**
```python
from aio_mrr.models.rental.request import RentalPoolBody

body = RentalPoolBody(
    host="pool.example.com",
    port=3333,
    user="worker1",
    password="password",
    priority=0
)
response = await client.rental.update_pool(ids=[54321], body=body)
if response.success:
    print("Pool updated successfully")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 7. `delete_pool(ids)`

Removes a pool from rentals.

**Signature:**
```python
async def delete_pool(ids: list[int]) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to remove the pool from |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! warning
    Removing a pool may stop mining if no pool with another priority is assigned.

**Usage Example:**
```python
response = await client.rental.delete_pool(ids=[54321])
if response.success:
    print("Pool deleted successfully")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 8. `extend(ids, length, getcost)`

Purchases a rental extension.

**Signature:**
```python
async def extend(ids: list[int], length: float, getcost: bool | None = None) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to extend |
| `length` | `float` | Yes | Hours to extend |
| `getcost` | `bool \| None` | No | If `True`, simulates the extension and returns the cost without actual deduction |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! tip
    Use `getcost=True` to preview the extension cost before actually extending.

**Usage Example:**
```python
# Extend rental
response = await client.rental.extend(ids=[54321], length=12.0)
if response.success:
    print("Rental extended successfully")
else:
    print(f"Error: {response.error.message}")

# Simulate extension cost
response = await client.rental.extend(ids=[54321], length=12.0, getcost=True)
if response.success:
    print("Cost simulation completed")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 9. `get_graph(ids, hours, interval)`

Retrieves rental graph data (historical hashrate, downtime).

**Signature:**
```python
async def get_graph(ids: list[int], hours: float | None = None, interval: str | None = None) -> MRRResponse[GraphData]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs (first ID is used) |
| `hours` | `float \| None` | No | Hours of data (max 2 weeks = 336 hours). Default 168 (7 days). |
| `interval` | `str \| None` | No | Data interval. Default `None`. |

**Returns:**
- `MRRResponse[GraphData]` — response with graph data
  - On success: `MRRResponse(success=True, data=GraphData)`
  - On error: `MRRResponse(success=False, error=...)`

**What `GraphData` contains:**
- `hashrate_data` — list of hashrate data points (`list[GraphDataPoint] | None`)
- `downtime_data` — list of downtime data points (`list[GraphDataPoint] | None`)
- `hours` — number of hours of data (`float | None`)

**What `GraphDataPoint` contains:**
- `time` — timestamp (`str | None`)
- `hashrate` — hashrate value (`float | None`)
- `downtime` — downtime status (`bool | None`)

**Usage Example:**
```python
# Get last 24 hours of data
response = await client.rental.get_graph(ids=[54321], hours=24)
if response.success:
    graph = response.data
    print(f"Hours of data: {graph.hours}")
    print(f"Hashrate points: {len(graph.hashrate_data or [])}")
    print(f"Downtime points: {len(graph.downtime_data or [])}")

    # Output last 5 hashrate points
    for point in (graph.hashrate_data or [])[-5:]:
        print(f"  {point.time}: {point.hashrate}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 10. `get_log(ids)`

Retrieves the rental activity log.

**Signature:**
```python
async def get_log(ids: list[int]) -> MRRResponse[list[RentalLogEntry]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to get logs for (first ID is used) |

**Returns:**
- `MRRResponse[list[RentalLogEntry]]` — response with log entry list
  - On success: `MRRResponse(success=True, data=[RentalLogEntry, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `RentalLogEntry` contains:**
- `time` — entry timestamp
- `message` — event message

**Usage Example:**
```python
response = await client.rental.get_log(ids=[54321])
if response.success:
    for log_entry in response.data:
        print(f"{log_entry.time}: {log_entry.message}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 11. `get_message(ids)`

Retrieves rental messages.

**Signature:**
```python
async def get_message(ids: list[int]) -> MRRResponse[list[RentalMessage]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to get messages for (first ID is used) |

**Returns:**
- `MRRResponse[list[RentalMessage]]` — response with message list
  - On success: `MRRResponse(success=True, data=[RentalMessage, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `RentalMessage` contains:**
- `time` — message timestamp
- `user` — username of the sender
- `message` — message text

**Usage Example:**
```python
response = await client.rental.get_message(ids=[54321])
if response.success:
    for msg in response.data:
        print(f"{msg.time} [{msg.user}]: {msg.message}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 12. `send_message(ids, message)`

Sends a message to a rental.

**Signature:**
```python
async def send_message(ids: list[int], message: str) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ids` | `list[int]` | Yes | List of rental IDs to send message to (first ID is used) |
| `message` | `str` | Yes | Message text |

**Returns:**
- `MRRResponse[None]` — response with result
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

!!! note
    Messages are visible to both the rig owner and the renter. Use them for communication regarding the rental.

**Usage Example:**
```python
response = await client.rental.send_message(
    ids=[54321],
    message="Please check the rig status. Hashrate is lower than expected."
)
if response.success:
    print("Message sent successfully")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

## Methods Summary Table

| # | Method | Description | Returns | Example |
|---|--------|-------------|---------|---------|
| 1 | `get_list(params)` | Rental list | `MRRResponse[list[RentalInfo]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 2 | `get_by_ids(ids)` | Rental by ID | `MRRResponse[RentalInfo]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 3 | `create(body)` | Create rental | `MRRResponse[dict[str, Any]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 4 | `update_profile(ids, profile)` | Apply profile | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 5 | `get_pools(ids)` | Rental pools | `MRRResponse[list[Pool]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 6 | `update_pool(ids, body)` | Update pool | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 7 | `delete_pool(ids)` | Delete pool | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 8 | `extend(ids, length, getcost)` | Extend rental | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 9 | `get_graph(ids, hours, interval)` | Hashrate graph | `MRRResponse[GraphData]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 10 | `get_log(ids)` | Rental log | `MRRResponse[list[RentalLogEntry]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 11 | `get_message(ids)` | Rental messages | `MRRResponse[list[RentalMessage]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 12 | `send_message(ids, message)` | Send message | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |

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

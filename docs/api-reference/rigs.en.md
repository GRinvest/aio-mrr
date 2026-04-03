# RigClient API Reference

This reference contains complete documentation for all 15 methods of `RigClient` for working with mining rigs.

> **Navigation:** [« Back to Home](../../index.md)

---

## Table of Contents

1. [Search Rigs](#search_rigs)
2. [Get Your Rigs](#get_mining_rigs)
3. [Get Rigs by ID](#get_rigs)
4. [Create Rig](#create_rig)
5. [Batch Update Rigs](#batch_update_rigs)
6. [Delete Rigs](#delete_rigs)
7. [Extend Rigs](#extend_rigs)
8. [Batch Extend Rigs](#batch_extend_rigs)
9. [Apply Profile to Rigs](#update_rig_profile)
10. [Get Rig Pools](#get_rig_pools)
11. [Update Rig Pool](#update_rig_pool)
12. [Delete Rig Pool](#delete_rig_pool)
13. [Get Rig Port](#get_rig_ports)
14. [Get Rig Threads](#get_rig_threads)
15. [Get Rig Graph](#get_rig_graph)

---

## search_rigs

Searches rigs by algorithm with filtering and sorting.

Similar to the main rig listing page on the MRR website.

### Signature

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

### Arguments

#### Required Parameter

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `str` | Algorithm: `sha256`, `scrypt`, `x11`, `kawpow`, etc. |

#### Pricing Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `currency` | `str \| None` | Currency: `BTC`, `LTC`, `ETH`, `DOGE`, `BCH`. Default `BTC`. |
| `price_min` | `float \| None` | Minimum price. |
| `price_max` | `float \| None` | Maximum price. |
| `price_type` | `str \| None` | Hash type for price (e.g., `mh`, `gh`). |

#### Time Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `minhours_min` | `int \| None` | Minimum hours (lower bound). |
| `minhours_max` | `int \| None` | Maximum hours (upper bound). |
| `maxhours_min` | `int \| None` | Minimum maximum time. |
| `maxhours_max` | `int \| None` | Maximum maximum time. |

#### Hashrate Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `hash_min` | `int \| None` | Minimum hashrate. |
| `hash_max` | `int \| None` | Maximum hashrate. |
| `hash_type` | `str \| None` | Type: `hash`, `kh`, `mh`, `gh`, `th`, `ph`, `eh`. Default `mh`. |

#### Performance Parameters (RPI)

| Parameter | Type | Description |
|-----------|------|-------------|
| `rpi_min` | `int \| None` | Minimum RPI (0-100). |
| `rpi_max` | `int \| None` | Maximum RPI (0-100). |

#### Status Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `offline` | `bool \| None` | Show offline rigs. Default `false`. |
| `rented` | `bool \| None` | Show rented rigs. Default `false`. |

#### Additional Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `region_type` | `str \| None` | `'include'` or `'exclude'` for region filtering. |
| `expdiff` | `float \| None` | Expected worker difficulty. |
| `islive` | `str \| None` | Filter rigs with hashrate (`yes`). |
| `xnonce` | `str \| None` | Filter by xnonce (`yes`, `no`). |

#### Pagination and Sorting Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `count` | `int \| None` | Number of results (max 100). Default `100`. |
| `offset` | `int \| None` | Pagination offset. Default `0`. |
| `orderby` | `str \| None` | Sort field. Default `score`. |
| `orderdir` | `str \| None` | Sort direction: `asc`, `desc`. Default `asc`. |

### Return Value

`MRRResponse[list[RigInfo]]` — response with rig list:

- **On success:** `MRRResponse(success=True, data=[RigInfo, ...])`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def search_available_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        # Search rigs with kawpow algorithm, price from 0.001 to 0.01, sorted by price
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
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/08_advanced_search.py`

---

## get_mining_rigs

Retrieves a list of your rigs.

### Signature

```python
async def get_mining_rigs(
    type: str | None = None,
    hashrate: bool | None = None
) -> MRRResponse[list[RigInfo]]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `str \| None` | Filter by algorithm. |
| `hashrate` | `bool \| None` | Show hashrate calculation. |

### Return Value

`MRRResponse[list[RigInfo]]` — response with your rig list:

- **On success:** `MRRResponse(success=True, data=[RigInfo, ...])`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def list_my_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_mining_rigs(type="scrypt", hashrate=True)

        if response.success:
            print(f"Rigs found: {len(response.data)}")
            for rig in response.data:
                print(f"{rig.id}: {rig.name} - {rig.hash}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## get_rigs

Retrieves one or more rigs by ID.

### Signature

```python
async def get_rigs(
    ids: list[int],
    fields: list[str] | None = None
) -> MRRResponse[list[RigInfo]]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to retrieve. Example: `[12345, 12346]`. |
| `fields` | `list[str] \| None` | Root-level field filter (e.g., `["name", "status"]`). |

### Return Value

`MRRResponse[list[RigInfo]]` — response with rig list:

- **On success:** `MRRResponse(success=True, data=[RigInfo, ...])`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def get_rigs_by_id():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        # Get only name and status fields
        response = await client.rig.get_rigs(
            ids=[12345, 12346],
            fields=["name", "status"]
        )

        if response.success:
            for rig in response.data:
                print(f"{rig.id}: {rig.name} - {rig.status}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## create_rig

Creates a new rig.

### Signature

```python
async def create_rig(
    body: RigCreateBody
) -> MRRResponse[dict[str, Any]]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `body` | `RigCreateBody` | Request body with rig creation parameters. |

`RigCreateBody` fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | Yes | Rig name. |
| `server` | `str` | Yes | Server (e.g., `us-east01.miningrigrentals.com`). |
| `description` | `str \| None` | No | Rig description. |
| `status` | `str \| None` | No | Rig status. |
| `price_btc_enabled` | `bool \| None` | No | Enable BTC payment. |
| `price_btc_price` | `float \| None` | No | BTC price. |
| `price_btc_autoprice` | `bool \| None` | No | BTC auto-pricing. |
| `price_btc_minimum` | `float \| None` | No | Minimum BTC price. |
| `price_type` | `str \| None` | No | Price type (e.g., `mh`). |
| `minhours` | `float \| None` | No | Minimum rental time. |
| `maxhours` | `float \| None` | No | Maximum rental time. |
| `extensions` | `bool \| None` | No | Allow extensions. |
| `hash_hash` | `float \| None` | No | Hashrate. |
| `hash_type` | `str \| None` | No | Hashrate type. |
| `suggested_diff` | `float \| None` | No | Suggested difficulty. |
| `ndevices` | `int \| None` | No | Number of devices. |

### Return Value

`MRRResponse[dict[str, Any]]` — response with created rig ID:

- **On success:** `MRRResponse(success=True, data={"id": 12345})`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

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
            print(f"Rig created with ID: {response.data['id']}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## batch_update_rigs

Updates a batch of rigs.

### Signature

```python
async def batch_update_rigs(
    body: RigBatchBody
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `body` | `RigBatchBody` | Request body with list of rigs to update. |

`RigBatchBody` fields:

| Field | Type | Description |
|-------|------|-------------|
| `rigs` | `list[dict[str, object]]` | List of dictionaries with rig data to update. |

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

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
            print("Rigs updated successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## delete_rigs

Deletes one or more rigs by ID.

### Signature

```python
async def delete_rigs(
    ids: list[int]
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to delete. |

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def delete_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.delete_rigs(ids=[12345, 12346])

        if response.success:
            print("Rigs deleted successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## extend_rigs

Extends a rig rental (for owners).

### Signature

```python
async def extend_rigs(
    ids: list[int],
    hours: float | None = None,
    minutes: float | None = None
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to extend. |
| `hours` | `float \| None` | Hours to extend. |
| `minutes` | `float \| None` | Minutes to extend. |

!!! note
    Specify at least one of `hours` or `minutes`.

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def extend_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.extend_rigs(ids=[12345], hours=24)

        if response.success:
            print("Rig extended successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## batch_extend_rigs

Batch extension of rentals for multiple rigs.

### Signature

```python
async def batch_extend_rigs(
    rig_hours: dict[int, float]
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `rig_hours` | `dict[int, float]` | Dictionary `{rig_id: hours}` for extension. |

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def batch_extend():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.batch_extend_rigs({12345: 24, 12346: 48})

        if response.success:
            print("Rigs extended successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## update_rig_profile

Applies a pool profile to one or more rigs.

### Signature

```python
async def update_rig_profile(
    ids: list[int],
    profile: int
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to update. |
| `profile` | `int` | Profile ID to apply. |

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def apply_profile():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.update_rig_profile(ids=[12345], profile=678)

        if response.success:
            print("Profile applied successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## get_rig_pools

Retrieves pools assigned to rigs.

### Signature

```python
async def get_rig_pools(
    ids: list[int]
) -> MRRResponse[list[Pool]]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to get pools for. |

### Return Value

`MRRResponse[list[Pool]]` — response with pool list:

- **On success:** `MRRResponse(success=True, data=[Pool, ...])`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def get_rig_pools():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_pools(ids=[12345])

        if response.success:
            for pool in response.data:
                print(f"{pool.name}: {pool.host}:{pool.port}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## update_rig_pool

Adds or replaces a pool on rigs.

### Signature

```python
async def update_rig_pool(
    ids: list[int],
    body: RigPoolBody
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to update. |
| `body` | `RigPoolBody` | Request body with pool data. |

`RigPoolBody` fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `host` | `str` | Yes | Pool host. |
| `port` | `int` | Yes | Pool port. |
| `user` | `str` | Yes | Worker username. |
| `password` | `str` | Yes | Pool password. |
| `priority` | `int \| None` | No | Pool priority (0-4). |

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

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
            print("Pool updated successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## delete_rig_pool

Removes a pool from rigs.

Removes the pool with the specified priority from rigs.

### Signature

```python
async def delete_rig_pool(
    ids: list[int]
) -> MRRResponse[None]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to remove the pool from. |

### Return Value

`MRRResponse[None]` — response:

- **On success:** `MRRResponse(success=True, data=None)`
- **On error:** `MRRResponse(success=False, error=...)`

### Usage Example

```python
from aio_mrr import MRRClient

async def delete_rig_pool():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.delete_rig_pool(ids=[12345])

        if response.success:
            print("Pool removed successfully")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/03_manage_rigs.py`

---

## get_rig_ports

Retrieves the direct port number for server connection.

### Signature

```python
async def get_rig_ports(
    ids: list[int]
) -> MRRResponse[RigPortInfo]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs (first ID is used). |

### Return Value

`MRRResponse[RigPortInfo]` — response with port information:

- **On success:** `MRRResponse(success=True, data=RigPortInfo)`
- **On error:** `MRRResponse(success=False, error=...)`

`RigPortInfo` fields:

| Field | Type | Description |
|-------|------|-------------|
| `rigid` | `str \| None` | Rig ID. |
| `port` | `int` | Port number. |
| `server` | `str \| None` | Server name. |
| `worker` | `str \| None` | Worker name for connection. |

### Usage Example

```python
from aio_mrr import MRRClient

async def get_rig_port():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_ports(ids=[12345])

        if response.success:
            print(f"Rig: {response.data.rigid}")
            print(f"Port: {response.data.port}")
            print(f"Server: {response.data.server}")
            print(f"Worker: {response.data.worker}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/08_advanced_search.py`

---

## get_rig_threads

Retrieves list of active threads for rigs.

### Signature

```python
async def get_rig_threads(
    ids: list[int]
) -> MRRResponse[list[RigThreadInfo]]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs to get threads for. |

### Return Value

`MRRResponse[list[RigThreadInfo]]` — response with list of rig-thread groups:

- **On success:** `MRRResponse(success=True, data=[RigThreadInfo, ...])`
- **On error:** `MRRResponse(success=False, error=...)`

`RigThreadInfo` fields:

| Field | Type | Description |
|-------|------|-------------|
| `rigid` | `str \| None` | Rig ID. |
| `access` | `str \| None` | Access level (owner/renter). |
| `threads` | `list[RigThreadDetail]` | List of thread details. |

`RigThreadDetail` fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int \| None` | Thread ID. |
| `worker` | `str \| None` | Worker name. |
| `status` | `str \| None` | Thread status. |
| `hashrate` | `float \| None` | Hashrate. |
| `last_share` | `str \| None` | Time of last share. |

### Usage Example

```python
from aio_mrr import MRRClient

async def get_rig_threads():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_threads(ids=[12345])

        if response.success:
            for group in response.data:
                print(f"Rig: {group.rigid}, Access: {group.access}")
                for thread in group.threads:
                    print(f"  {thread.worker}: {thread.status} - {thread.hashrate}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/08_advanced_search.py`

---

## get_rig_graph

Retrieves rig graph data (historical hashrate, downtime).

### Signature

```python
async def get_rig_graph(
    ids: list[int],
    hours: float | None = None,
    deflate: bool | None = None
) -> MRRResponse[RigGraphData]
```

### Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | `list[int]` | List of rig IDs (first ID is used). |
| `hours` | `float \| None` | Hours of data (max 2 weeks). Default `168`. |
| `deflate` | `bool \| None` | Base64 encoding. Default `false`. |

### Return Value

`MRRResponse[RigGraphData]` — response with graph data:

- **On success:** `MRRResponse(success=True, data=RigGraphData)`
- **On error:** `MRRResponse(success=False, error=...)`

`RigGraphData` fields:

| Field | Type | Description |
|-------|------|-------------|
| `rigid` | `str \| None` | Rig ID. |
| `chartdata` | `dict \| None` | Graph data (time_start, time_end, timestamp_start, timestamp_end, bars). |

The `chartdata` field contains:

| Field | Type | Description |
|-------|------|-------------|
| `time_start` | `str` | Graph start time. |
| `time_end` | `str` | Graph end time. |
| `timestamp_start` | `str` | Start Unix timestamp. |
| `timestamp_end` | `int` | End Unix timestamp. |
| `bars` | `str` | Graph data in `"[ts,val],[ts,val],..."` format. |

### Usage Example

```python
from aio_mrr import MRRClient

async def get_rig_graph():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_graph(ids=[12345], hours=24)

        if response.success:
            data = response.data.chartdata
            if data:
                print(f"Start: {data['time_start']}")
                print(f"End: {data['time_end']}")
                bars = data.get('bars', '')
                bar_count = bars.count('],[') + 1 if bars else 0
                print(f"Data points: {bar_count}")
        else:
            print(f"Error: {response.error}")
```

### Example Link

See: `examples/08_advanced_search.py`

---

## Links

- [« Back to Home](../../index.md)
- [AccountClient Reference](./account.md)
- [RentalClient Reference](./rentals.md)
- [RigGroupClient Reference](./rig-groups.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

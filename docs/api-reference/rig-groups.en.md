# RigGroupClient — API Reference

Reference for all `RigGroupClient` methods for managing mining rig groups on MiningRigRentals: creating groups, CRUD operations, adding and removing rigs from groups.

## Overview

`RigGroupClient` provides methods for:
- Retrieving rig group lists
- Getting information about a specific group
- Creating new rig groups
- Updating group information
- Deleting rig groups
- Adding rigs to a group
- Removing rigs from a group

---

## Methods

### 1. `get_list()`

Retrieves a list of your rig groups.

**Signature:**
```python
async def get_list() -> MRRResponse[list[RigGroupInfo]]
```

**Returns:**
- `MRRResponse[list[RigGroupInfo]]` — response with group list:
  - On success: `MRRResponse(success=True, data=[RigGroupInfo, ...])`
  - On error: `MRRResponse(success=False, error=...)`

**What `RigGroupInfo` contains:**
- `id` — group identifier (`str`)
- `name` — group name
- `enabled` — group enabled flag (`True`/`False`)
- `rental_limit` — limit of active rentals
- `rigs` — list of rig identifiers in the group (`list[int]`)
- `algo` — group mining algorithm (optional, `str | None`)

**Usage Example:**
```python
# Get list of all rig groups
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

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 2. `get_by_id(id)`

Retrieves rig group details by ID.

**Signature:**
```python
async def get_by_id(id: int) -> MRRResponse[RigGroupInfo]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `int` | Yes | Rig group identifier |

**Returns:**
- `MRRResponse[RigGroupInfo]` — response with group information:
  - On success: `MRRResponse(success=True, data=RigGroupInfo)`
  - On error: `MRRResponse(success=False, error=...)`

**What `RigGroupInfo` contains:**
- `id` — group identifier (`str`)
- `name` — group name
- `enabled` — group enabled flag
- `rental_limit` — limit of active rentals
- `rigs` — list of rig identifiers in the group
- `algo` — group mining algorithm (optional)

**Usage Example:**
```python
# Get information about a specific group
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

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 3. `create(body)`

Creates a new rig group.

**Signature:**
```python
async def create(body: RigGroupCreateBody) -> MRRResponse[dict[str, Any]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `body` | `RigGroupCreateBody` | Yes | Request body with group creation parameters |

**`RigGroupCreateBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Group name |
| `enabled` | `bool` | No | Group enabled flag. Default `True` |
| `rental_limit` | `int` | No | Active rental limit. Default `1` |

**Returns:**
- `MRRResponse[dict[str, Any]]` — response with created group ID and message:
  - On success: `MRRResponse(success=True, data={"id": 123, "message": "..."})`
  - On error: `MRRResponse(success=False, error=...)`

**Usage Example:**
```python
from aio_mrr.models.riggroup.request import RigGroupCreateBody

# Create group with default settings (enabled=True, rental_limit=1)
body = RigGroupCreateBody(name="My Scrypt Rigs")
response = await client.riggroup.create(body)
if response.success:
    print(f"Group created with ID: {response.data['id']}")
    print(f"Message: {response.data['message']}")
else:
    print(f"Error: {response.error.message}")

# Create group with custom settings
body = RigGroupCreateBody(
    name="High-Performance Rigs",
    enabled=True,
    rental_limit=10
)
response = await client.riggroup.create(body)
if response.success:
    print(f"Group created: {response.data}")
```

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 4. `update(id, body)`

Updates a rig group.

**Signature:**
```python
async def update(id: int, body: RigGroupUpdateBody) -> MRRResponse[None]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `int` | Yes | Rig group identifier to update |
| `body` | `RigGroupUpdateBody` | Yes | Request body with update parameters (all fields optional) |

**`RigGroupUpdateBody` parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str \| None` | No | New group name |
| `enabled` | `bool \| None` | No | New enabled status |
| `rental_limit` | `int \| None` | No | New rental limit |

!!! note
    All fields in `RigGroupUpdateBody` are optional — you can update only the parameters you need.

**Returns:**
- `MRRResponse[None]` — response with result:
  - On success: `MRRResponse(success=True, data=None)`
  - On error: `MRRResponse(success=False, error=...)`

**Usage Example:**
```python
from aio_mrr.models.riggroup.request import RigGroupUpdateBody

# Update only the group name
body = RigGroupUpdateBody(name="Updated Group Name")
response = await client.riggroup.update(id=123, body=body)
if response.success:
    print("Group name updated successfully")
else:
    print(f"Error: {response.error.message}")

# Update multiple parameters
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

# Disable a group
body = RigGroupUpdateBody(enabled=False)
response = await client.riggroup.update(id=123, body=body)
```

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 5. `delete(id)`

Deletes a rig group.

**Signature:**
```python
async def delete(id: int) -> MRRResponse[dict[str, Any]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `int` | Yes | Rig group identifier to delete |

**Returns:**
- `MRRResponse[dict[str, Any]]` — response with deletion confirmation:
  - On success: `MRRResponse(success=True, data={"id": 123, "message": "..."})`
  - On error: `MRRResponse(success=False, error=...)`

!!! warning
    Group deletion is irreversible. Make sure the group is no longer needed before deleting.

**Usage Example:**
```python
# Delete a group
response = await client.riggroup.delete(id=123)
if response.success:
    print("Group deleted successfully")
    print(f"Message: {response.data['message']}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 6. `add_rigs(id, rig_ids)`

Adds rigs to a group.

**Signature:**
```python
async def add_rigs(id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `int` | Yes | Rig group identifier |
| `rig_ids` | `list[int]` | Yes | List of rig IDs to add to the group |

**Returns:**
- `MRRResponse[dict[str, Any]]` — response with addition confirmation:
  - On success: `MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})`
  - On error: `MRRResponse(success=False, error=...)`

**What the response contains:**
- `id` — group identifier
- `message` — result message
- `rigs` — list of rig IDs added to the group

**Usage Example:**
```python
# Add one rig to a group
response = await client.riggroup.add_rigs(id=123, rig_ids=[12345])
if response.success:
    print(f"Rig added to group")
    print(f"Rigs in group: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")

# Add multiple rigs to a group
response = await client.riggroup.add_rigs(id=123, rig_ids=[12345, 12346, 12347])
if response.success:
    print(f"Rigs added: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 7. `remove_rigs(id, rig_ids)`

Removes rigs from a group.

**Signature:**
```python
async def remove_rigs(id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]
```

**Arguments:**
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `int` | Yes | Rig group identifier |
| `rig_ids` | `list[int]` | Yes | List of rig IDs to remove from the group |

**Returns:**
- `MRRResponse[dict[str, Any]]` — response with removal confirmation:
  - On success: `MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})`
  - On error: `MRRResponse(success=False, error=...)`

**What the response contains:**
- `id` — group identifier
- `message` — result message
- `rigs` — list of rig IDs removed from the group

**Usage Example:**
```python
# Remove one rig from a group
response = await client.riggroup.remove_rigs(id=123, rig_ids=[12345])
if response.success:
    print(f"Rig removed from group")
    print(f"Remaining rigs: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")

# Remove multiple rigs from a group
response = await client.riggroup.remove_rigs(id=123, rig_ids=[12345, 12346])
if response.success:
    print(f"Rigs removed: {response.data['rigs']}")
else:
    print(f"Error: {response.error.message}")
```

**Example link:** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

## Methods Summary Table

| # | Method | Description | Returns | Example |
|---|--------|-------------|---------|---------|
| 1 | `get_list()` | Rig group list | `MRRResponse[list[RigGroupInfo]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 2 | `get_by_id(id)` | Group by ID | `MRRResponse[RigGroupInfo]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 3 | `create(body)` | Create group | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 4 | `update(id, body)` | Update group | `MRRResponse[None]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 5 | `delete(id)` | Delete group | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 6 | `add_rigs(id, rig_ids)` | Add rigs to group | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 7 | `remove_rigs(id, rig_ids)` | Remove rigs from group | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |

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

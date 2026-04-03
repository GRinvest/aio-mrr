# RigGroupClient — API 参考

`RigGroupClient` 所有方法的参考文档，用于管理 MiningRigRentals 上的矿机组（rig groups）：创建组、CRUD 操作、添加和删除组内矿机。

## 概述

`RigGroupClient` 提供以下方法：
- 获取矿机组列表
- 获取特定组的信息
- 创建新矿机组
- 更新组信息
- 删除矿机组
- 向组添加矿机
- 从组删除矿机

---

## 方法

### 1. `get_list()`

获取您的矿机组列表。

**签名：**
```python
async def get_list() -> MRRResponse[list[RigGroupInfo]]
```

**返回：**
- `MRRResponse[list[RigGroupInfo]]` — 包含组列表的响应：
  - 成功时：`MRRResponse(success=True, data=[RigGroupInfo, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`RigGroupInfo` 包含：**
- `id` — 组标识符（`str`）
- `name` — 组名称
- `enabled` — 组启用标志（`True`/`False`）
- `rental_limit` — 活跃租赁限制
- `rigs` — 组内矿机标识符列表（`list[int]`）
- `algo` — 组挖矿算法（可选，`str | None`）

**使用示例：**
```python
# 获取所有矿机组列表
response = await client.riggroup.get_list()
if response.success:
    for group in response.data:
        print(f"组 ID: {group.id}")
        print(f"  名称: {group.name}")
        print(f"  已启用: {group.enabled}")
        print(f"  租赁限制: {group.rental_limit}")
        print(f"  矿机: {group.rigs}")
        if group.algo:
            print(f"  算法: {group.algo}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 2. `get_by_id(id)`

按 ID 获取矿机组详情。

**签名：**
```python
async def get_by_id(id: int) -> MRRResponse[RigGroupInfo]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `id` | `int` | 是 | 矿机组标识符 |

**返回：**
- `MRRResponse[RigGroupInfo]` — 包含组信息的响应：
  - 成功时：`MRRResponse(success=True, data=RigGroupInfo)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`RigGroupInfo` 包含：**
- `id` — 组标识符（`str`）
- `name` — 组名称
- `enabled` — 组启用标志
- `rental_limit` — 活跃租赁限制
- `rigs` — 组内矿机标识符列表
- `algo` — 组挖矿算法（可选）

**使用示例：**
```python
# 获取特定组的信息
response = await client.riggroup.get_by_id(id=123)
if response.success:
    group = response.data
    print(f"组 ID: {group.id}")
    print(f"名称: {group.name}")
    print(f"已启用: {group.enabled}")
    print(f"租赁限制: {group.rental_limit}")
    print(f"组内矿机数: {len(group.rigs)}")
    print(f"矿机 ID: {group.rigs}")
    if group.algo:
        print(f"算法: {group.algo}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 3. `create(body)`

创建新矿机组。

**签名：**
```python
async def create(body: RigGroupCreateBody) -> MRRResponse[dict[str, Any]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `body` | `RigGroupCreateBody` | 是 | 包含创建组参数的请求体 |

**`RigGroupCreateBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `name` | `str` | 是 | 组名称 |
| `enabled` | `bool` | 否 | 组启用标志。默认 `True` |
| `rental_limit` | `int` | 否 | 活跃租赁限制。默认 `1` |

**返回：**
- `MRRResponse[dict[str, Any]]` — 包含已创建组 ID 和消息的响应：
  - 成功时：`MRRResponse(success=True, data={"id": 123, "message": "..."})`
  - 失败时：`MRRResponse(success=False, error=...)`

**使用示例：**
```python
from aio_mrr.models.riggroup.request import RigGroupCreateBody

# 使用默认设置创建组（enabled=True, rental_limit=1）
body = RigGroupCreateBody(name="我的 Scrypt 矿机组")
response = await client.riggroup.create(body)
if response.success:
    print(f"组已创建，ID: {response.data['id']}")
    print(f"消息: {response.data['message']}")
else:
    print(f"错误: {response.error.message}")

# 使用自定义设置创建组
body = RigGroupCreateBody(
    name="高性能矿机组",
    enabled=True,
    rental_limit=10
)
response = await client.riggroup.create(body)
if response.success:
    print(f"组已创建: {response.data}")
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 4. `update(id, body)`

更新矿机组。

**签名：**
```python
async def update(id: int, body: RigGroupUpdateBody) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `id` | `int` | 是 | 要更新的矿机组标识符 |
| `body` | `RigGroupUpdateBody` | 是 | 包含更新参数的请求体（所有字段可选） |

**`RigGroupUpdateBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `name` | `str \| None` | 否 | 新组名称 |
| `enabled` | `bool \| None` | 否 | 新启用状态 |
| `rental_limit` | `int \| None` | 否 | 新租赁限制 |

!!! note
    `RigGroupUpdateBody` 中的所有字段都是可选的 — 可以仅更新需要的参数。

**返回：**
- `MRRResponse[None]` — 结果响应：
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

**使用示例：**
```python
from aio_mrr.models.riggroup.request import RigGroupUpdateBody

# 仅更新组名称
body = RigGroupUpdateBody(name="更新后的组名称")
response = await client.riggroup.update(id=123, body=body)
if response.success:
    print("组名称更新成功")
else:
    print(f"错误: {response.error.message}")

# 更新多个参数
body = RigGroupUpdateBody(
    name="新名称",
    enabled=False,
    rental_limit=15
)
response = await client.riggroup.update(id=123, body=body)
if response.success:
    print("组更新成功")
else:
    print(f"错误: {response.error.message}")

# 禁用组
body = RigGroupUpdateBody(enabled=False)
response = await client.riggroup.update(id=123, body=body)
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 5. `delete(id)`

删除矿机组。

**签名：**
```python
async def delete(id: int) -> MRRResponse[dict[str, Any]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `id` | `int` | 是 | 要删除的矿机组标识符 |

**返回：**
- `MRRResponse[dict[str, Any]]` — 包含删除确认的响应：
  - 成功时：`MRRResponse(success=True, data={"id": 123, "message": "..."})`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! warning
    删除组不可逆。删除前请确认不再需要该组。

**使用示例：**
```python
# 删除组
response = await client.riggroup.delete(id=123)
if response.success:
    print("组删除成功")
    print(f"消息: {response.data['message']}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 6. `add_rigs(id, rig_ids)`

向组添加矿机。

**签名：**
```python
async def add_rigs(id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `id` | `int` | 是 | 矿机组标识符 |
| `rig_ids` | `list[int]` | 是 | 要添加到组的矿机 ID 列表 |

**返回：**
- `MRRResponse[dict[str, Any]]` — 包含添加确认的响应：
  - 成功时：`MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})`
  - 失败时：`MRRResponse(success=False, error=...)`

**响应包含：**
- `id` — 组标识符
- `message` — 结果消息
- `rigs` — 已添加到组的矿机 ID 列表

**使用示例：**
```python
# 向组添加单个矿机
response = await client.riggroup.add_rigs(id=123, rig_ids=[12345])
if response.success:
    print(f"矿机已添加到组")
    print(f"组内矿机: {response.data['rigs']}")
else:
    print(f"错误: {response.error.message}")

# 向组添加多个矿机
response = await client.riggroup.add_rigs(id=123, rig_ids=[12345, 12346, 12347])
if response.success:
    print(f"矿机已添加: {response.data['rigs']}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

### 7. `remove_rigs(id, rig_ids)`

从组删除矿机。

**签名：**
```python
async def remove_rigs(id: int, rig_ids: list[int]) -> MRRResponse[dict[str, Any]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `id` | `int` | 是 | 矿机组标识符 |
| `rig_ids` | `list[int]` | 是 | 要从组删除的矿机 ID 列表 |

**返回：**
- `MRRResponse[dict[str, Any]]` — 包含删除确认的响应：
  - 成功时：`MRRResponse(success=True, data={"id": ..., "message": "...", "rigs": [...]})`
  - 失败时：`MRRResponse(success=False, error=...)`

**响应包含：**
- `id` — 组标识符
- `message` — 结果消息
- `rigs` — 已从组删除的矿机 ID 列表

**使用示例：**
```python
# 从组删除单个矿机
response = await client.riggroup.remove_rigs(id=123, rig_ids=[12345])
if response.success:
    print(f"矿机已从组删除")
    print(f"剩余矿机: {response.data['rigs']}")
else:
    print(f"错误: {response.error.message}")

# 从组删除多个矿机
response = await client.riggroup.remove_rigs(id=123, rig_ids=[12345, 12346])
if response.success:
    print(f"矿机已删除: {response.data['rigs']}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/05_rig_groups.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py)

---

## 方法汇总表

| # | 方法 | 描述 | 返回类型 | 示例 |
|---|-------|------|----------|------|
| 1 | `get_list()` | 矿机组列表 | `MRRResponse[list[RigGroupInfo]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 2 | `get_by_id(id)` | 按 ID 获取组 | `MRRResponse[RigGroupInfo]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 3 | `create(body)` | 创建组 | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 4 | `update(id, body)` | 更新组 | `MRRResponse[None]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 5 | `delete(id)` | 删除组 | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 6 | `add_rigs(id, rig_ids)` | 向组添加矿机 | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |
| 7 | `remove_rigs(id, rig_ids)` | 从组删除矿机 | `MRRResponse[dict[str, Any]]` | [05_rig_groups.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/05_rig_groups.py) |

---

## 附加资源

- [首页](../../index.zh.md)
- [错误处理](../error-handling.zh.md)
- [数据模型](../models.zh.md)
- [认证](../authentication.zh.md)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

# RentalClient — API 参考

`RentalClient` 所有方法的参考文档，用于管理 MiningRigRentals 上的矿机租赁：创建租赁、管理矿池、续期、获取统计、图表数据和日志。

## 概述

`RentalClient` 提供以下方法：
- 获取带过滤的租赁列表
- 创建和管理租赁
- 将矿池配置文件应用到租赁
- 管理租赁矿池
- 续期租赁
- 获取图表数据、日志和消息

---

## 方法

### 1. `get_list(params)`

获取租赁列表，支持过滤和分页。

**签名：**
```python
async def get_list(params: dict[str, Any] | None = None) -> MRRResponse[list[RentalInfo]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `params` | `dict[str, Any] \| None` | 否 | 用于过滤的查询参数。默认返回所有租赁。 |

**过滤参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `type` | `str \| None` | 否 | `'owner'` 或 `'renter'` — 按角色过滤 |
| `algo` | `str \| None` | 否 | 按挖矿算法过滤 |
| `history` | `bool \| None` | 否 | `true` = 已完成的租赁，`false` = 活跃的租赁 |
| `rig` | `int \| None` | 否 | 按矿机 ID 过滤 |
| `start` | `int \| None` | 否 | 分页起始位置（默认 0） |
| `limit` | `int \| None` | 否 | 记录限制（默认 100） |
| `currency` | `str \| None` | 否 | 支付币种：`BTC`、`LTC`、`ETH`、`DOGE`、`BCH` |

**返回：**
- `MRRResponse[list[RentalInfo]]` — 包含租赁列表的响应
  - 成功时：`MRRResponse(success=True, data=[RentalInfo, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`RentalInfo` 包含：**
- `id` — 租赁标识符
- `rig_id` — 矿机标识符
- `rig_name` — 矿机名称（可选）
- `owner` — 矿机所有者
- `renter` — 承租人
- `status` — 租赁状态
- `started` — 开始时间
- `ends` — 结束时间
- `length` — 时长（小时）
- `currency` — 支付币种
- `rate` — 费率信息（`RateInfo`）
- `hash` — 算力信息（`RentalHashInfo`）
- `cost` — 租赁费用（`RentalCostInfo`）

**使用示例：**
```python
# 获取作为承租人的活跃租赁
response = await client.rental.get_list(params={"type": "renter", "history": False})
if response.success:
    for rental in response.data:
        print(f"租赁 {rental.id}: {rental.status}, 结束: {rental.ends}")
else:
    print(f"错误: {response.error.message}")

# 获取已完成的租赁并分页
response = await client.rental.get_list(params={"type": "owner", "history": True, "start": 0, "limit": 10})
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 2. `get_by_ids(ids)`

按 ID 获取租赁信息。

**签名：**
```python
async def get_by_ids(ids: list[int]) -> MRRResponse[RentalInfo]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要获取的租赁 ID 列表（使用第一个 ID） |

**返回：**
- `MRRResponse[RentalInfo]` — 包含租赁信息的响应
  - 成功时：`MRRResponse(success=True, data=RentalInfo)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! note
    如果传递了多个 ID 的列表，仅使用第一个 ID 获取租赁信息。

**使用示例：**
```python
response = await client.rental.get_by_ids(ids=[54321])
if response.success:
    rental = response.data
    print(f"租赁 ID: {rental.id}")
    print(f"矿机 ID: {rental.rig_id}")
    print(f"状态: {rental.status}")
    print(f"所有者: {rental.owner}")
    print(f"承租人: {rental.renter}")
    print(f"币种: {rental.currency}")
    print(f"时长: {rental.length} 小时")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 3. `create(body)`

创建新租赁。

**签名：**
```python
async def create(body: RentalCreateBody) -> MRRResponse[dict[str, Any]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `body` | `RentalCreateBody` | 是 | 包含创建租赁参数的请求体 |

**`RentalCreateBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `rig` | `int` | 是 | 要租赁的矿机 ID |
| `length` | `float` | 是 | 租赁时长（小时） |
| `profile` | `int` | 是 | 要使用的矿池配置文件 ID |
| `currency` | `str \| None` | 否 | 支付币种（默认 `BTC`） |
| `rate_type` | `str \| None` | 否 | 算力类型（默认 `'mh'`） |
| `rate_price` | `float \| None` | 否 | 每单位算力每日价格 |

**返回：**
- `MRRResponse[dict[str, Any]]` — 包含已创建租赁 ID 和费用的响应
  - 成功时：`MRRResponse(success=True, data={"id": "54321", "cost": "0.02000000"})`
  - 失败时：`MRRResponse(success=False, error=...)`

**使用示例：**
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
    print(f"租赁已创建，ID: {response.data['id']}")
    print(f"费用: {response.data['cost']}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 4. `update_profile(ids, profile)`

将矿池配置文件应用到租赁。

**签名：**
```python
async def update_profile(ids: list[int], profile: int) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要更新的租赁 ID 列表 |
| `profile` | `int` | 是 | 要应用的配置文件 ID |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! note
    矿池配置文件定义了用于租赁挖矿的带优先级的矿池集合。

**使用示例：**
```python
# 将配置文件应用到单个租赁
response = await client.rental.update_profile(ids=[54321], profile=678)
if response.success:
    print("配置文件应用成功")
else:
    print(f"错误: {response.error.message}")

# 将配置文件应用到多个租赁
response = await client.rental.update_profile(ids=[54321, 54322, 54323], profile=678)
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 5. `get_pools(ids)`

获取分配给租赁的矿池。

**签名：**
```python
async def get_pools(ids: list[int]) -> MRRResponse[list[Pool]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要获取矿池的租赁 ID 列表 |

**返回：**
- `MRRResponse[list[Pool]]` — 包含矿池列表的响应
  - 成功时：`MRRResponse(success=True, data=[Pool, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`Pool` 包含：**
- `id` — 矿池标识符
- `type` — 算法（sha256、scrypt、x11 等）
- `name` — 矿池名称
- `host` — 矿池主机
- `port` — 矿池端口
- `user` — 用户名/worker
- `password` — 密码
- `notes` — 备注（可选）
- `algo` — 算法信息（可选）

**使用示例：**
```python
response = await client.rental.get_pools(ids=[54321])
if response.success:
    for pool in response.data:
        print(f"矿池: {pool.name}")
        print(f"  类型: {pool.type}")
        print(f"  主机: {pool.host}:{pool.port}")
        print(f"  用户: {pool.user}")
        if pool.notes:
            print(f"  备注: {pool.notes}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 6. `update_pool(ids, body)`

在租赁上添加或替换矿池。

**签名：**
```python
async def update_pool(ids: list[int], body: RentalPoolBody) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要更新的租赁 ID 列表 |
| `body` | `RentalPoolBody` | 是 | 包含矿池数据的请求体 |

**`RentalPoolBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `host` | `str` | 是 | 矿池主机 |
| `port` | `int` | 是 | 矿池端口 |
| `user` | `str` | 是 | worker 名称 |
| `password` | `str` | 是 | worker 密码 |
| `priority` | `int \| None` | 否 | 矿池优先级（0-4） |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! note
    如果已存在相同优先级的矿池，它将被替换。优先级 0 为最高。

**使用示例：**
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
    print("矿池更新成功")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 7. `delete_pool(ids)`

从租赁删除矿池。

**签名：**
```python
async def delete_pool(ids: list[int]) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要删除矿池的租赁 ID 列表 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! warning
    删除矿池可能导致挖矿停止，如果没有分配其他优先级的矿池。

**使用示例：**
```python
response = await client.rental.delete_pool(ids=[54321])
if response.success:
    print("矿池删除成功")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 8. `extend(ids, length, getcost)`

购买租赁续期。

**签名：**
```python
async def extend(ids: list[int], length: float, getcost: bool | None = None) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要续期的租赁 ID 列表 |
| `length` | `float` | 是 | 续期小时数 |
| `getcost` | `bool \| None` | 否 | 如果为 `True`，模拟续期并返回费用而不实际扣款 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! tip
    使用 `getcost=True` 在实际续期前预先计算续期费用。

**使用示例：**
```python
# 续期租赁
response = await client.rental.extend(ids=[54321], length=12.0)
if response.success:
    print("租赁续期成功")
else:
    print(f"错误: {response.error.message}")

# 模拟续期费用
response = await client.rental.extend(ids=[54321], length=12.0, getcost=True)
if response.success:
    print("费用模拟完成")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 9. `get_graph(ids, hours, interval)`

获取租赁的图表数据（历史算力、停机时间）。

**签名：**
```python
async def get_graph(ids: list[int], hours: float | None = None, interval: str | None = None) -> MRRResponse[GraphData]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 租赁 ID 列表（使用第一个 ID） |
| `hours` | `float \| None` | 否 | 数据小时数（最大 2 周 = 336 小时）。默认 168（7 天）。 |
| `interval` | `str \| None` | 否 | 数据间隔。默认 `None`。 |

**返回：**
- `MRRResponse[GraphData]` — 包含图表数据的响应
  - 成功时：`MRRResponse(success=True, data=GraphData)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`GraphData` 包含：**
- `hashrate_data` — 算力数据点列表（`list[GraphDataPoint] | None`）
- `downtime_data` — 停机数据点列表（`list[GraphDataPoint] | None`）
- `hours` — 数据小时数（`float | None`）

**`GraphDataPoint` 包含：**
- `time` — 时间戳（`str | None`）
- `hashrate` — 算力值（`float | None`）
- `downtime` — 停机状态（`bool | None`）

**使用示例：**
```python
# 获取最近 24 小时的数据
response = await client.rental.get_graph(ids=[54321], hours=24)
if response.success:
    graph = response.data
    print(f"数据小时数: {graph.hours}")
    print(f"算力数据点: {len(graph.hashrate_data or [])}")
    print(f"停机数据点: {len(graph.downtime_data or [])}")
    
    # 输出最后 5 个算力数据点
    for point in (graph.hashrate_data or [])[-5:]:
        print(f"  {point.time}: {point.hashrate}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 10. `get_log(ids)`

获取租赁活动日志。

**签名：**
```python
async def get_log(ids: list[int]) -> MRRResponse[list[RentalLogEntry]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要获取日志的租赁 ID 列表（使用第一个 ID） |

**返回：**
- `MRRResponse[list[RentalLogEntry]]` — 包含日志条目列表的响应
  - 成功时：`MRRResponse(success=True, data=[RentalLogEntry, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`RentalLogEntry` 包含：**
- `time` — 条目时间戳
- `message` — 事件消息

**使用示例：**
```python
response = await client.rental.get_log(ids=[54321])
if response.success:
    for log_entry in response.data:
        print(f"{log_entry.time}: {log_entry.message}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 11. `get_message(ids)`

获取租赁消息。

**签名：**
```python
async def get_message(ids: list[int]) -> MRRResponse[list[RentalMessage]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要获取消息的租赁 ID 列表（使用第一个 ID） |

**返回：**
- `MRRResponse[list[RentalMessage]]` — 包含消息列表的响应
  - 成功时：`MRRResponse(success=True, data=[RentalMessage, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`RentalMessage` 包含：**
- `time` — 消息时间戳
- `user` — 发送消息的用户名
- `message` — 消息内容

**使用示例：**
```python
response = await client.rental.get_message(ids=[54321])
if response.success:
    for msg in response.data:
        print(f"{msg.time} [{msg.user}]: {msg.message}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

### 12. `send_message(ids, message)`

发送租赁消息。

**签名：**
```python
async def send_message(ids: list[int], message: str) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要发送消息的租赁 ID 列表（使用第一个 ID） |
| `message` | `str` | 是 | 消息内容 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! note
    消息对矿机所有者和承租人均可见。使用它们就租赁事宜进行沟通。

**使用示例：**
```python
response = await client.rental.send_message(
    ids=[54321],
    message="请检查矿机状态。算力低于预期。"
)
if response.success:
    print("消息发送成功")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/04_create_rental.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py)

---

## 方法汇总表

| # | 方法 | 描述 | 返回类型 | 示例 |
|---|-------|------|----------|------|
| 1 | `get_list(params)` | 租赁列表 | `MRRResponse[list[RentalInfo]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 2 | `get_by_ids(ids)` | 按 ID 获取租赁 | `MRRResponse[RentalInfo]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 3 | `create(body)` | 创建租赁 | `MRRResponse[dict[str, Any]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 4 | `update_profile(ids, profile)` | 应用配置文件 | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 5 | `get_pools(ids)` | 租赁矿池 | `MRRResponse[list[Pool]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 6 | `update_pool(ids, body)` | 更新矿池 | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 7 | `delete_pool(ids)` | 删除矿池 | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 8 | `extend(ids, length, getcost)` | 续期租赁 | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 9 | `get_graph(ids, hours, interval)` | 算力图表 | `MRRResponse[GraphData]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 10 | `get_log(ids)` | 租赁日志 | `MRRResponse[list[RentalLogEntry]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 11 | `get_message(ids)` | 租赁消息 | `MRRResponse[list[RentalMessage]]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |
| 12 | `send_message(ids, message)` | 发送消息 | `MRRResponse[None]` | [04_create_rental.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/04_create_rental.py) |

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

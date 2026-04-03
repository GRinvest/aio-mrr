# AccountClient — API 参考

`AccountClient` 所有方法的参考文档，用于管理 MiningRigRentals 账户：余额、交易记录、矿池配置文件、已保存矿池和币种状态。

## 概述

`AccountClient` 提供以下方法：
- 获取账户信息和余额
- 查看交易历史
- 矿池配置文件的 CRUD 操作
- 已保存矿池的 CRUD 操作
- 矿池连接测试
- 查看币种状态

---

## 方法

### 1. `get_account()`

获取用户账户的详细信息。

**签名：**
```python
async def get_account(self) -> MRRResponse[AccountInfo]
```

**返回：**
- `MRRResponse[AccountInfo]` — 包含账户信息的响应
  - 成功时：`MRRResponse(success=True, data=AccountInfo)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`AccountInfo` 包含：**
- `username` — 用户名
- `email` — 电子邮件地址
- `withdraw` — 各币种提现地址
- `deposit` — 各币种充值地址
- `notifications` — 通知设置
- `settings` — 账户设置

**使用示例：**
```python
response = await client.account.get_account()
if response.success:
    print(f"用户名: {response.data.username}")
    print(f"邮箱: {response.data.email}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

### 2. `get_balance()`

获取账户所有币种的余额。

**签名：**
```python
async def get_balance(self) -> MRRResponse[dict[str, BalanceInfo]]
```

**返回：**
- `MRRResponse[dict[str, BalanceInfo]]` — 包含各币种余额的响应
  - 成功时：`MRRResponse(success=True, data={"BTC": BalanceInfo, "LTC": BalanceInfo, ...})`
  - 失败时：`MRRResponse(success=False, error=...)`

**`BalanceInfo` 包含：**
- `confirmed` — 已确认余额（字符串）
- `pending` — 待确认余额（浮点数）
- `unconfirmed` — 未确认余额（字符串）

!!! note
    余额会在资金入账时实时更新。

**使用示例：**
```python
response = await client.account.get_balance()
if response.success:
    for currency, balance in response.data.items():
        print(f"{currency}: 已确认={balance.confirmed}, 待确认={balance.pending}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/01_quickstart.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/01_quickstart.py)

---

### 3. `get_transactions()`

获取账户交易历史，支持过滤。

**签名：**
```python
async def get_transactions(params: TransactionsQueryParams | None = None) -> MRRResponse[TransactionsList]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `params` | `TransactionsQueryParams \| None` | 否 | 过滤参数。默认返回所有交易（limit=100）。 |

**`TransactionsQueryParams` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `start` | `int \| None` | 否 | 分页起始位置（默认 0） |
| `limit` | `int \| None` | 否 | 记录限制（默认 100） |
| `algo` | `str \| None` | 否 | 按算法过滤 |
| `type` | `str \| None` | 否 | 交易类型（credit、payout、referral、deposit、payment、credit/refund、debit/refund、rental fee） |
| `rig` | `int \| None` | 否 | 按矿机 ID 过滤 |
| `rental` | `int \| None` | 否 | 按租赁 ID 过滤 |
| `txid` | `str \| None` | 否 | 按 txid 过滤 |
| `time_greater_eq` | `str \| None` | 否 | 时间 >=（Unix 时间戳） |
| `time_less_eq` | `str \| None` | 否 | 时间 <=（Unix 时间戳） |

**返回：**
- `MRRResponse[TransactionsList]` — 包含交易列表的响应
  - 成功时：`MRRResponse(success=True, data=TransactionsList)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`TransactionsList` 包含：**
- `total` — 交易总数（字符串）
- `returned` — 返回的记录数
- `start` — 起始位置
- `limit` — 记录限制
- `transactions` — `Transaction` 对象列表

**使用示例：**
```python
# 获取最近 10 笔收入
params = TransactionsQueryParams(type="credit", limit=10)
response = await client.account.get_transactions(params)
if response.success:
    for tx in response.data.transactions:
        print(f"{tx.type}: {tx.amount} ({tx.when})")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

### 4. `get_profiles()`

获取所有矿池配置文件列表，或按算法过滤。

**签名：**
```python
async def get_profiles(algo: str | None = None) -> MRRResponse[list[Profile]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `algo` | `str \| None` | 否 | 按算法过滤（例如 "scrypt"、"sha256"）。默认返回所有配置文件。 |

**返回：**
- `MRRResponse[list[Profile]]` — 包含配置文件列表的响应
  - 成功时：`MRRResponse(success=True, data=[Profile, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`Profile` 包含：**
- `id` — 配置文件标识符
- `name` — 配置文件名称
- `algo` — 算法信息（`AlgoProfileInfo`）
- `pools` — 矿池列表（`list[PoolProfileInfo]`）及优先级

**使用示例：**
```python
# 获取所有配置文件
response = await client.account.get_profiles()
if response.success:
    for profile in response.data:
        print(f"{profile.name}: {len(profile.pools)} 个矿池")
        for pool in profile.pools:
            print(f"  - {pool.host}:{pool.port} (优先级 {pool.priority})")

# 仅获取 scrypt 的配置文件
response = await client.account.get_profiles(algo="scrypt")
```

**示例链接：** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 5. `create_profile()`

为指定算法创建新的矿池配置文件。

**签名：**
```python
async def create_profile(body: ProfileCreateBody) -> MRRResponse[ProfileCreateResponse]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `body` | `ProfileCreateBody` | 是 | 包含配置文件名称和算法的请求体 |

**`ProfileCreateBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `name` | `str` | 是 | 配置文件名称 |
| `algo` | `str` | 是 | 配置文件算法（例如 "scrypt"、"sha256"） |

**返回：**
- `MRRResponse[ProfileCreateResponse]` — 包含已创建配置文件 ID 的响应
  - 成功时：`MRRResponse(success=True, data=ProfileCreateResponse)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`ProfileCreateResponse` 包含：**
- `pid` — 已创建配置文件的标识符（字符串）

**使用示例：**
```python
body = ProfileCreateBody(name="我的 Scrypt 配置文件", algo="scrypt")
response = await client.account.create_profile(body)
if response.success:
    print(f"配置文件已创建，ID: {response.data.pid}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 6. `get_profile()`

按 ID 获取特定矿池配置文件。

**签名：**
```python
async def get_profile(pid: int) -> MRRResponse[Profile]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `pid` | `int` | 是 | 配置文件标识符 |

**返回：**
- `MRRResponse[Profile]` — 包含配置文件信息的响应
  - 成功时：`MRRResponse(success=True, data=Profile)`
  - 失败时：`MRRResponse(success=False, error=...)`

**使用示例：**
```python
response = await client.account.get_profile(pid=40073)
if response.success:
    profile = response.data
    print(f"配置文件: {profile.name}")
    print(f"算法: {profile.algo.display}")
    for pool in profile.pools:
        print(f"  - {pool.host}:{pool.port} (优先级 {pool.priority}, 状态 {pool.status})")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 7. `update_profile()`

在配置文件中添加或替换矿池并指定优先级。

**签名：**
```python
async def update_profile(pid: int, poolid: int, priority: int | None = None) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `pid` | `int` | 是 | 配置文件标识符 |
| `poolid` | `int` | 是 | 要添加的矿池标识符 |
| `priority` | `int \| None` | 否 | 矿池优先级（0-4）。如未指定，矿池将添加到第一个可用优先级。 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! note
    优先级 0 为最高优先级。优先级编号越小的矿池越先被处理。

**使用示例：**
```python
# 在优先级 0 添加矿池
response = await client.account.update_profile(pid=40073, poolid=98708, priority=0)
if response.success:
    print("矿池已添加到配置文件，优先级 0")
else:
    print(f"错误: {response.error.message}")

# 不指定优先级添加矿池（自动选择）
response = await client.account.update_profile(pid=40073, poolid=98708)
```

**示例链接：** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 8. `update_profile_priority()`

在配置文件的特定优先级位置添加矿池。

**签名：**
```python
async def update_profile_priority(pid: int, priority: int, poolid: int) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `pid` | `int` | 是 | 配置文件标识符 |
| `priority` | `int` | 是 | 矿池优先级（0-4） |
| `poolid` | `int` | 是 | 要添加的矿池标识符 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! warning
    优先级必须在 0-4 范围内。超出此范围的值将导致 API 错误。

**使用示例：**
```python
response = await client.account.update_profile_priority(pid=41818, priority=0, poolid=98708)
if response.success:
    print("矿池已在优先级 0 添加")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 9. `delete_profile()`

按 ID 删除矿池配置文件。

**签名：**
```python
async def delete_profile(pid: int) -> MRRResponse[ProfileDeleteResponse]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `pid` | `int` | 是 | 要删除的配置文件标识符 |

**返回：**
- `MRRResponse[ProfileDeleteResponse]` — 删除结果响应
  - 成功时：`MRRResponse(success=True, data=ProfileDeleteResponse)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`ProfileDeleteResponse` 包含：**
- `id` — 已删除配置文件的标识符
- `success` — 删除成功状态
- `message` — 结果消息

**使用示例：**
```python
response = await client.account.delete_profile(pid=42281)
if response.success:
    print(f"已删除: {response.data.message}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/10_profile_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py)

---

### 10. `get_pools()`

获取账户所有已保存矿池的列表。

**签名：**
```python
async def get_pools(self) -> MRRResponse[list[Pool]]
```

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
response = await client.account.get_pools()
if response.success:
    for pool in response.data:
        print(f"{pool.name}: {pool.type}://{pool.host}:{pool.port}")
        if pool.notes:
            print(f"  备注: {pool.notes}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 11. `get_pools_by_ids()`

按标识符列表获取特定矿池。

**签名：**
```python
async def get_pools_by_ids(ids: list[int]) -> MRRResponse[list[Pool]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 矿池标识符列表 |

**返回：**
- `MRRResponse[list[Pool]]` — 包含矿池列表的响应
  - 成功时：`MRRResponse(success=True, data=[Pool, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! note
    矿池在请求 URL 中以分号分隔（`/account/pool/12345;12346`）。

**使用示例：**
```python
response = await client.account.get_pools_by_ids(ids=[12345, 12346])
if response.success:
    for pool in response.data:
        print(f"ID: {pool.id}, 类型: {pool.type}, 名称: {pool.name}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 12. `create_pool()`

创建新的已保存矿池。

**签名：**
```python
async def create_pool(body: PoolCreateBody) -> MRRResponse[PoolCreateResponse]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `body` | `PoolCreateBody` | 是 | 包含矿池参数的请求体 |

**`PoolCreateBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `type` | `str` | 是 | 矿池算法（sha256、scrypt、x11 等） |
| `name` | `str` | 是 | 矿池识别名称 |
| `host` | `str` | 是 | 矿池主机 |
| `port` | `int` | 是 | 矿池端口 |
| `user` | `str` | 是 | worker 名称 |
| `password` | `str \| None` | 否 | worker 密码 |
| `notes` | `str \| None` | 否 | 矿池备注 |

**返回：**
- `MRRResponse[PoolCreateResponse]` — 包含已创建矿池 ID 的响应
  - 成功时：`MRRResponse(success=True, data=PoolCreateResponse)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`PoolCreateResponse` 包含：**
- `id` — 已创建矿池的标识符（int）

**使用示例：**
```python
body = PoolCreateBody(
    type="scrypt",
    name="我的主矿池",
    host="pool.example.com",
    port=3333,
    user="worker1",
    password="pass123",
    notes="scrypt 挖矿主矿池"
)
response = await client.account.create_pool(body)
if response.success:
    print(f"矿池已创建，ID: {response.data.id}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 13. `update_pools()`

按标识符列表更新现有矿池的参数。

**签名：**
```python
async def update_pools(ids: list[int], body: dict[str, Any]) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要更新的矿池标识符列表 |
| `body` | `dict[str, Any]` | 是 | 包含新矿池参数的请求体 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`body` 中允许的字段：**
- `name` — 新矿池名称
- `host` — 新主机
- `port` — 新端口
- `user` — 新用户名
- `password` — 新密码
- `notes` — 新备注

!!! note
    可以仅更新需要的字段。未指定的字段将保持不变。

**使用示例：**
```python
# 更新名称和主机
body = {"name": "更新后的矿池名称", "host": "new.pool.com"}
response = await client.account.update_pools(ids=[12345], body=body)
if response.success:
    print("矿池已更新")
else:
    print(f"错误: {response.error.message}")

# 批量更新多个矿池
response = await client.account.update_pools(ids=[12345, 12346], body={"notes": "更新后的备注"})
```

**示例链接：** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 14. `delete_pools()`

按标识符列表删除已保存的矿池。

**签名：**
```python
async def delete_pools(ids: list[int]) -> MRRResponse[None]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `ids` | `list[int]` | 是 | 要删除的矿池标识符列表 |

**返回：**
- `MRRResponse[None]` — 结果响应
  - 成功时：`MRRResponse(success=True, data=None)`
  - 失败时：`MRRResponse(success=False, error=...)`

!!! warning
    删除矿池不可逆。请确保矿池未在活跃的配置文件或租赁中使用。

**使用示例：**
```python
response = await client.account.delete_pools(ids=[12345, 12346])
if response.success:
    print("矿池删除成功")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 15. `test_pool()`

从不同 MRR 服务器测试矿池连接。

**签名：**
```python
async def test_pool(body: PoolTestBody) -> MRRResponse[PoolTestResult]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `body` | `PoolTestBody` | 是 | 包含测试参数的请求体 |

**`PoolTestBody` 参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `method` | `str` | 是 | 测试方法：`"simple"`（仅连接）或 `"full"`（含认证） |
| `extramethod` | `str \| None` | 否 | 用于 ethhash：`[esm0,esm1,esm2,esm3]`。默认 `esm0`。 |
| `type` | `str \| None` | 否 | 算法（scrypt、sha256、x11）。`full` 方法需要。 |
| `host` | `str \| None` | 否 | 矿池主机（可包含端口） |
| `port` | `int \| None` | 否 | 矿池端口。`host` 中未包含时需要。 |
| `user` | `str \| None` | 否 | 用户名。`full` 方法需要。 |
| `password` | `str \| None` | 否 | 密码。`full` 方法需要。 |
| `source` | `str \| None` | 否 | 用于测试的 MRR 服务器。默认 `us-central01`。 |

**返回：**
- `MRRResponse[PoolTestResult]` — 包含测试结果的响应
  - 成功时：`MRRResponse(success=True, data=PoolTestResult)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`PoolTestResult` 包含：**
- `result` — `PoolTestResultItem` 列表，包含来自不同服务器的测试结果
- `error` — 错误列表（如有）

**`PoolTestResultItem` 包含：**
- `source` — 执行测试的 MRR 服务器
- `dest` — 矿池地址（host:port）
- `error` — 错误描述（成功时为空字符串）
- `connection` — 连接是否成功
- `executiontime` — 测试执行时间（秒）
- `protocol` — 协议（stratum 等）
- `sub` — 订阅是否成功
- `auth` — 认证是否成功
- `diff` — 获取的难度值
- `xnonce` — 是否支持 xnonce
- `ssl` — 是否使用 SSL

!!! note
    - **简单测试**：仅检查矿池端口连接。
    - **完整测试**：检查连接、订阅、认证和获取工作。

**使用示例：**
```python
# 简单测试（仅连接）
body = PoolTestBody(method="simple", host="de.minexmr.com:4444")
response = await client.account.test_pool(body)
if response.success:
    for item in response.data.result:
        status = "成功" if item.connection else f"失败: {item.error}"
        print(f"{item.source} -> {item.dest}: {status} ({item.executiontime}s)")

# 完整测试（含认证）
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
    print(f"连接: {result.connection}")
    print(f"认证: {result.auth}")
    print(f"工作: {result.work}")
    print(f"难度: {result.diff}")
```

**示例链接：** [`examples/09_pool_management.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py)

---

### 16. `get_currencies()`

获取账户的币种列表及其启用状态。

**签名：**
```python
async def get_currencies(self) -> MRRResponse[list[CurrencyStatus]]
```

**返回：**
- `MRRResponse[list[CurrencyStatus]]` — 包含币种列表的响应
  - 成功时：`MRRResponse(success=True, data=[CurrencyStatus, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`CurrencyStatus` 包含：**
- `name` — 币种名称（BTC、LTC、ETH、DOGE、BCH）
- `enabled` — 账户的启用状态

**使用示例：**
```python
response = await client.account.get_currencies()
if response.success:
    print("可用币种:")
    for currency in response.data:
        status = "已启用" if currency.enabled else "已禁用"
        print(f"  - {currency.name}: {status}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/02_account_balance.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py)

---

## 方法汇总表

| # | 方法 | 描述 | 返回类型 | 示例 |
|---|-------|------|----------|------|
| 1 | `get_account()` | 账户信息 | `MRRResponse[AccountInfo]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |
| 2 | `get_balance()` | 各币种余额 | `MRRResponse[dict[str, BalanceInfo]]` | [01_quickstart.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/01_quickstart.py) |
| 3 | `get_transactions(params)` | 交易历史 | `MRRResponse[TransactionsList]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |
| 4 | `get_profiles(algo)` | 所有矿池配置文件 | `MRRResponse[list[Profile]]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 5 | `create_profile(body)` | 创建配置文件 | `MRRResponse[ProfileCreateResponse]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 6 | `get_profile(pid)` | 按 ID 获取配置文件 | `MRRResponse[Profile]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 7 | `update_profile(pid, poolid, priority)` | 在配置文件中添加/替换矿池 | `MRRResponse[None]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 8 | `update_profile_priority(pid, priority, poolid)` | 设置矿池优先级 | `MRRResponse[None]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 9 | `delete_profile(pid)` | 删除配置文件 | `MRRResponse[ProfileDeleteResponse]` | [10_profile_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/10_profile_management.py) |
| 10 | `get_pools()` | 所有已保存矿池 | `MRRResponse[list[Pool]]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 11 | `get_pools_by_ids(ids)` | 按 ID 获取矿池 | `MRRResponse[list[Pool]]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 12 | `create_pool(body)` | 创建矿池 | `MRRResponse[PoolCreateResponse]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 13 | `update_pools(ids, body)` | 更新矿池 | `MRRResponse[None]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 14 | `delete_pools(ids)` | 删除矿池 | `MRRResponse[None]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 15 | `test_pool(body)` | 测试矿池 | `MRRResponse[PoolTestResult]` | [09_pool_management.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/09_pool_management.py) |
| 16 | `get_currencies()` | 币种状态 | `MRRResponse[list[CurrencyStatus]]` | [02_account_balance.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/02_account_balance.py) |

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

# RigClient 参考

本参考包含 `RigClient` 全部 15 个方法的完整文档，用于管理挖矿矿机（rigs）。

> **导航：** [« 返回首页](../../index.zh.md)

---

## 目录

1. [搜索矿机](#search_rigs)
2. [获取我的矿机](#get_mining_rigs)
3. [按 ID 获取矿机](#get_rigs)
4. [创建矿机](#create_rig)
5. [批量更新矿机](#batch_update_rigs)
6. [删除矿机](#delete_rigs)
7. [续期矿机](#extend_rigs)
8. [批量续期矿机](#batch_extend_rigs)
9. [应用配置文件到矿机](#update_rig_profile)
10. [获取矿机矿池](#get_rig_pools)
11. 更新矿机矿池](#update_rig_pool)
12. [删除矿机矿池](#delete_rig_pool)
13. [获取矿机端口](#get_rig_ports)
14. [获取矿机线程](#get_rig_threads)
15. [获取矿机图表](#get_rig_graph)

---

## search_rigs

按算法搜索矿机，支持过滤和排序。

等同于 MRR 网站上的矿机列表页面。

### 签名

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

### 参数

#### 必填参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `type` | `str` | 算法：`sha256`、`scrypt`、`x11`、`kawpow` 等 |

#### 定价参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `currency` | `str \| None` | 币种：`BTC`、`LTC`、`ETH`、`DOGE`、`BCH`。默认 `BTC`。 |
| `price_min` | `float \| None` | 最低价格。 |
| `price_max` | `float \| None` | 最高价格。 |
| `price_type` | `str \| None` | 价格的算力类型（例如 `mh`、`gh`）。 |

#### 时间参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `minhours_min` | `int \| None` | 最短时间下限。 |
| `minhours_max` | `int \| None` | 最短时间上限。 |
| `maxhours_min` | `int \| None` | 最长时间下限。 |
| `maxhours_max` | `int \| None` | 最长时间上限。 |

#### 算力参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `hash_min` | `int \| None` | 最低算力。 |
| `hash_max` | `int \| None` | 最高算力。 |
| `hash_type` | `str \| None` | 算力类型：`hash`、`kh`、`mh`、`gh`、`th`、`ph`、`eh`。默认 `mh`。 |

#### 性能参数（RPI）

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `rpi_min` | `int \| None` | 最低 RPI（0-100）。 |
| `rpi_max` | `int \| None` | 最高 RPI（0-100）。 |

#### 状态过滤

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `offline` | `bool \| None` | 显示离线矿机。默认 `false`。 |
| `rented` | `bool \| None` | 显示已出租矿机。默认 `false`。 |

#### 附加过滤

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `region_type` | `str \| None` | `'include'` 或 `'exclude'` 用于区域过滤。 |
| `expdiff` | `float \| None` | 预期 worker 难度。 |
| `islive` | `str \| None` | 过滤有算力的矿机（`yes`）。 |
| `xnonce` | `str \| None` | 按 xnonce 过滤（`yes`、`no`）。 |

#### 分页和排序参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `count` | `int \| None` | 结果数量（最大 100）。默认 `100`。 |
| `offset` | `int \| None` | 分页偏移量。默认 `0`。 |
| `orderby` | `str \| None` | 排序字段。默认 `score`。 |
| `orderdir` | `str \| None` | 排序方向：`asc`、`desc`。默认 `asc`。 |

### 返回值

`MRRResponse[list[RigInfo]]` — 包含矿机列表的响应：

- **成功时：** `MRRResponse(success=True, data=[RigInfo, ...])`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def search_available_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        # 搜索 kawpow 算法矿机，价格 0.001 到 0.01，按价格排序
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
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/08_advanced_search.py`

---

## get_mining_rigs

获取您的矿机列表。

### 签名

```python
async def get_mining_rigs(
    type: str | None = None,
    hashrate: bool | None = None
) -> MRRResponse[list[RigInfo]]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `type` | `str \| None` | 按算法过滤。 |
| `hashrate` | `bool \| None` | 显示算力计算。 |

### 返回值

`MRRResponse[list[RigInfo]]` — 包含您的矿机列表的响应：

- **成功时：** `MRRResponse(success=True, data=[RigInfo, ...])`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def list_my_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_mining_rigs(type="scrypt", hashrate=True)
        
        if response.success:
            print(f"找到矿机数: {len(response.data)}")
            for rig in response.data:
                print(f"{rig.id}: {rig.name} - {rig.hash}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## get_rigs

按 ID 获取一个或多个矿机。

### 签名

```python
async def get_rigs(
    ids: list[int],
    fields: list[str] | None = None
) -> MRRResponse[list[RigInfo]]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要获取的矿机 ID 列表。示例：`[12345, 12346]`。 |
| `fields` | `list[str] \| None` | 根级别字段过滤（例如 `["name", "status"]`）。 |

### 返回值

`MRRResponse[list[RigInfo]]` — 包含矿机列表的响应：

- **成功时：** `MRRResponse(success=True, data=[RigInfo, ...])`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def get_rigs_by_id():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        # 仅获取 name 和 status 字段
        response = await client.rig.get_rigs(
            ids=[12345, 12346],
            fields=["name", "status"]
        )
        
        if response.success:
            for rig in response.data:
                print(f"{rig.id}: {rig.name} - {rig.status}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## create_rig

创建新矿机。

### 签名

```python
async def create_rig(
    body: RigCreateBody
) -> MRRResponse[dict[str, Any]]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `body` | `RigCreateBody` | 包含创建矿机参数的请求体。 |

`RigCreateBody` 字段：

| 字段 | 类型 | 必填 | 描述 |
|------|-----|------|------|
| `name` | `str` | 是 | 矿机名称。 |
| `server` | `str` | 是 | 服务器（例如 `us-east01.miningrigrentals.com`）。 |
| `description` | `str \| None` | 否 | 矿机描述。 |
| `status` | `str \| None` | 否 | 矿机状态。 |
| `price_btc_enabled` | `bool \| None` | 否 | 启用 BTC 支付。 |
| `price_btc_price` | `float \| None` | 否 | BTC 价格。 |
| `price_btc_autoprice` | `bool \| None` | 否 | BTC 自动定价。 |
| `price_btc_minimum` | `float \| None` | 否 | BTC 最低价格。 |
| `price_type` | `str \| None` | 否 | 价格类型（例如 `mh`）。 |
| `minhours` | `float \| None` | 否 | 最短租赁时间。 |
| `maxhours` | `float \| None` | 否 | 最长租赁时间。 |
| `extensions` | `bool \| None` | 否 | 允许续期。 |
| `hash_hash` | `float \| None` | 否 | 算力。 |
| `hash_type` | `str \| None` | 否 | 算力类型。 |
| `suggested_diff` | `float \| None` | 否 | 建议难度。 |
| `ndevices` | `int \| None` | 否 | 设备数量。 |

### 返回值

`MRRResponse[dict[str, Any]]` — 包含已创建矿机 ID 的响应：

- **成功时：** `MRRResponse(success=True, data={"id": 12345})`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient
from aio_mrr.models.rig.request import RigCreateBody

async def create_new_rig():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        body = RigCreateBody(
            name="我的 Scrypt 矿机",
            server="us-east01.miningrigrentals.com",
            price_type="mh",
            minhours=1.0,
            maxhours=24.0,
            extensions=True,
        )
        
        response = await client.rig.create_rig(body)
        
        if response.success:
            print(f"矿机已创建，ID: {response.data['id']}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## batch_update_rigs

批量更新矿机。

### 签名

```python
async def batch_update_rigs(
    body: RigBatchBody
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `body` | `RigBatchBody` | 包含要更新矿机列表的请求体。 |

`RigBatchBody` 字段：

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigs` | `list[dict[str, object]]` | 包含要更新矿机数据的字典列表。 |

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient
from aio_mrr.models.rig.request import RigBatchBody

async def batch_update():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        body = RigBatchBody(
            rigs=[
                {"id": 12345, "name": "更新名称 1"},
                {"id": 12346, "name": "更新名称 2"},
            ]
        )
        
        response = await client.rig.batch_update_rigs(body)
        
        if response.success:
            print("矿机更新成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## delete_rigs

按 ID 删除一个或多个矿机。

### 签名

```python
async def delete_rigs(
    ids: list[int]
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要删除的矿机 ID 列表。 |

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def delete_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.delete_rigs(ids=[12345, 12346])
        
        if response.success:
            print("矿机删除成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## extend_rigs

续期矿机租赁（面向所有者）。

### 签名

```python
async def extend_rigs(
    ids: list[int],
    hours: float | None = None,
    minutes: float | None = None
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要续期的矿机 ID 列表。 |
| `hours` | `float \| None` | 续期小时数。 |
| `minutes` | `float \| None` | 续期分钟数。 |

!!! note "注意"
    请至少指定 `hours` 或 `minutes` 中的一个参数。

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def extend_rigs():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.extend_rigs(ids=[12345], hours=24)
        
        if response.success:
            print("矿机续期成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## batch_extend_rigs

批量续期多个矿机的租赁。

### 签名

```python
async def batch_extend_rigs(
    rig_hours: dict[int, float]
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `rig_hours` | `dict[int, float]` | `{矿机ID: 小时数}` 字典用于续期。 |

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def batch_extend():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.batch_extend_rigs({12345: 24, 12346: 48})
        
        if response.success:
            print("矿机批量续期成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## update_rig_profile

将矿池配置文件应用到一个或多个矿机。

### 签名

```python
async def update_rig_profile(
    ids: list[int],
    profile: int
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要更新的矿机 ID 列表。 |
| `profile` | `int` | 要应用的配置文件 ID。 |

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def apply_profile():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.update_rig_profile(ids=[12345], profile=678)
        
        if response.success:
            print("配置文件应用成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## get_rig_pools

获取分配给矿机的矿池。

### 签名

```python
async def get_rig_pools(
    ids: list[int]
) -> MRRResponse[list[Pool]]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要获取矿池的矿机 ID 列表。 |

### 返回值

`MRRResponse[list[Pool]]` — 包含矿池列表的响应：

- **成功时：** `MRRResponse(success=True, data=[Pool, ...])`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def get_rig_pools():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_pools(ids=[12345])
        
        if response.success:
            for pool in response.data:
                print(f"{pool.name}: {pool.host}:{pool.port}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## update_rig_pool

在矿机上添加或替换矿池。

### 签名

```python
async def update_rig_pool(
    ids: list[int],
    body: RigPoolBody
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要更新的矿机 ID 列表。 |
| `body` | `RigPoolBody` | 包含矿池数据的请求体。 |

`RigPoolBody` 字段：

| 字段 | 类型 | 必填 | 描述 |
|------|-----|------|------|
| `host` | `str` | 是 | 矿池主机。 |
| `port` | `int` | 是 | 矿池端口。 |
| `user` | `str` | 是 | worker 用户名。 |
| `password` | `str` | 是 | 矿池密码。 |
| `priority` | `int \| None` | 否 | 矿池优先级（0-4）。 |

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

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
            print("矿池更新成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## delete_rig_pool

从矿机删除矿池。

从指定矿机删除指定优先级的矿池。

### 签名

```python
async def delete_rig_pool(
    ids: list[int]
) -> MRRResponse[None]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要删除矿池的矿机 ID 列表。 |

### 返回值

`MRRResponse[None]` — 响应：

- **成功时：** `MRRResponse(success=True, data=None)`
- **失败时：** `MRRResponse(success=False, error=...)`

### 使用示例

```python
from aio_mrr import MRRClient

async def delete_rig_pool():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.delete_rig_pool(ids=[12345])
        
        if response.success:
            print("矿池删除成功")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/03_manage_rigs.py`

---

## get_rig_ports

获取连接到服务器的直接端口号。

### 签名

```python
async def get_rig_ports(
    ids: list[int]
) -> MRRResponse[RigPortInfo]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 矿机 ID 列表（使用第一个 ID）。 |

### 返回值

`MRRResponse[RigPortInfo]` — 包含端口信息的响应：

- **成功时：** `MRRResponse(success=True, data=RigPortInfo)`
- **失败时：** `MRRResponse(success=False, error=...)`

`RigPortInfo` 字段：

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigid` | `str \| None` | 矿机 ID。 |
| `port` | `int` | 端口号。 |
| `server` | `str \| None` | 服务器名称。 |
| `worker` | `str \| None` | 连接用的 worker 名称。 |

### 使用示例

```python
from aio_mrr import MRRClient

async def get_rig_port():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_ports(ids=[12345])
        
        if response.success:
            print(f"矿机: {response.data.rigid}")
            print(f"端口: {response.data.port}")
            print(f"服务器: {response.data.server}")
            print(f"Worker: {response.data.worker}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/08_advanced_search.py`

---

## get_rig_threads

获取矿机的活动线程列表。

### 签名

```python
async def get_rig_threads(
    ids: list[int]
) -> MRRResponse[list[RigThreadInfo]]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 要获取线程的矿机 ID 列表。 |

### 返回值

`MRRResponse[list[RigThreadInfo]]` — 包含矿机线程组的响应：

- **成功时：** `MRRResponse(success=True, data=[RigThreadInfo, ...])`
- **失败时：** `MRRResponse(success=False, error=...)`

`RigThreadInfo` 字段：

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigid` | `str \| None` | 矿机 ID。 |
| `access` | `str \| None` | 访问级别（owner/renter）。 |
| `threads` | `list[RigThreadDetail]` | 线程详情列表。 |

`RigThreadDetail` 字段：

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `int \| None` | 线程 ID。 |
| `worker` | `str \| None` | Worker 名称。 |
| `status` | `str \| None` | 线程状态。 |
| `hashrate` | `float \| None` | 算力。 |
| `last_share` | `str \| None` | 最后一次提交 share 的时间。 |

### 使用示例

```python
from aio_mrr import MRRClient

async def get_rig_threads():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_threads(ids=[12345])
        
        if response.success:
            for group in response.data:
                print(f"矿机: {group.rigid}, 访问: {group.access}")
                for thread in group.threads:
                    print(f"  {thread.worker}: {thread.status} - {thread.hashrate}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/08_advanced_search.py`

---

## get_rig_graph

获取矿机的图表数据（历史算力、停机时间）。

### 签名

```python
async def get_rig_graph(
    ids: list[int],
    hours: float | None = None,
    deflate: bool | None = None
) -> MRRResponse[RigGraphData]
```

### 参数

| 参数 | 类型 | 描述 |
|----------|-----|------|
| `ids` | `list[int]` | 矿机 ID 列表（使用第一个 ID）。 |
| `hours` | `float \| None` | 数据小时数（最大 2 周）。默认 `168`。 |
| `deflate` | `bool \| None` | Base64 编码。默认 `false`。 |

### 返回值

`MRRResponse[RigGraphData]` — 包含图表数据的响应：

- **成功时：** `MRRResponse(success=True, data=RigGraphData)`
- **失败时：** `MRRResponse(success=False, error=...)`

`RigGraphData` 字段：

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigid` | `str \| None` | 矿机 ID。 |
| `chartdata` | `dict \| None` | 图表数据（time_start、time_end、timestamp_start、timestamp_end、bars）。 |

`chartdata` 字段包含：

| 字段 | 类型 | 描述 |
|------|-----|------|
| `time_start` | `str` | 图表开始时间。 |
| `time_end` | `str` | 图表结束时间。 |
| `timestamp_start` | `str` | 开始 Unix 时间戳。 |
| `timestamp_end` | `int` | 结束 Unix 时间戳。 |
| `bars` | `str` | 图表数据，格式 `"[ts,val],[ts,val],..."`。 |

### 使用示例

```python
from aio_mrr import MRRClient

async def get_rig_graph():
    async with MRRClient(api_key="your_key", api_secret="your_secret") as client:
        response = await client.rig.get_rig_graph(ids=[12345], hours=24)
        
        if response.success:
            data = response.data.chartdata
            if data:
                print(f"开始: {data['time_start']}")
                print(f"结束: {data['time_end']}")
                bars = data.get('bars', '')
                bar_count = bars.count('],[') + 1 if bars else 0
                print(f"数据点数: {bar_count}")
        else:
            print(f"错误: {response.error}")
```

### 示例链接

参见：`examples/08_advanced_search.py`

---

## 链接

- [« 返回首页](../../index.zh.md)
- [AccountClient 参考](./account.zh.md)
- [RentalClient 参考](./rentals.zh.md)
- [RigGroupClient 参考](./rig-groups.zh.md)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

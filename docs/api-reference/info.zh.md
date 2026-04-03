# InfoClient — API 参考

`InfoClient` 所有方法的参考文档，用于获取 MiningRigRentals 服务器、挖矿算法和可用支付币种的信息。

## 概述

`InfoClient` 提供以下方法：
- 获取 MRR 服务器列表
- 查看所有挖矿算法
- 获取特定算法的信息
- 查看可用支付币种

---

## 方法

### 1. `get_servers()`

获取所有 MiningRigRentals 服务器列表。

**签名：**
```python
async def get_servers(self) -> MRRResponse[ServersList]
```

**返回：**
- `MRRResponse[ServersList]` — 包含服务器列表的响应
  - 成功时：`MRRResponse(success=True, data=ServersList)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`ServersList` 包含：**
- `servers` — `ServerInfo` 对象列表

**`ServerInfo` 包含：**
- `id` — 服务器标识符（例如 "EU-01"）
- `name` — 服务器名称
- `region` — 服务器区域
- `port` — 服务器端口（可选）
- `ethereum_port` — Ethereum 端口（可选）

**使用示例：**
```python
response = await client.info.get_servers()
if response.success:
    print("MRR 服务器:")
    for server in response.data.servers:
        print(f"  - {server.name} ({server.id}): {server.region}")
        if server.port:
            print(f"    端口: {server.port}")
        if server.ethereum_port:
            print(f"    Ethereum 端口: {server.ethereum_port}")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 2. `get_algos()`

获取所有挖矿算法列表及其信息。

**签名：**
```python
async def get_algos(currency: str | None = None) -> MRRResponse[list[AlgoInfo]]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `currency` | `str \| None` | 否 | 按币种过滤。默认返回所有算法。 |

**返回：**
- `MRRResponse[list[AlgoInfo]]` — 包含算法列表的响应
  - 成功时：`MRRResponse(success=True, data=[AlgoInfo, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`AlgoInfo` 包含：**
- `name` — 算法内部名称（例如 "scrypt"、"sha256"）
- `display` — 显示名称
- `suggested_price` — 建议价格（`PriceInfo`）
- `stats` — 算法统计（`AlgoStats`）

**`PriceInfo` 包含：**
- `amount` — 价格值
- `currency` — 价格币种
- `unit` — 计量单位

**`AlgoStats` 包含：**
- `available` — 可用算力（`AvailableHashInfo`）
- `rented` — 已租算力（`RentedHashInfo`）
- `prices` — 价格信息（`PricesInfo`）

**`AvailableHashInfo` 包含：**
- `rigs` — 可用矿机数量
- `hash` — 可用算力（`HashInfo`）

**`RentedHashInfo` 包含：**
- `rigs` — 已租矿机数量
- `hash` — 已租算力（`HashInfo`）

**`HashInfo` 包含：**
- `hash` — 算力值
- `unit` — 计量单位（例如 "GH/s"）
- `nice` — 格式化显示

**`PricesInfo` 包含：**
- `lowest` — 最低价格
- `last_10` — 最近 10 次租赁的平均价格
- `last` — 最新价格

!!! note
    此方法可用于获取平台上所有可用挖矿算法的总体概览。

**使用示例：**
```python
# 获取所有算法
response = await client.info.get_algos()
if response.success:
    print("挖矿算法:")
    for algo in response.data:
        print(f"\n{algo.display} ({algo.name})")
        print(f"  建议价格: {algo.suggested_price.amount} {algo.suggested_price.currency}")
        print(f"  可用: {algo.stats.available.hash.nice}")
        print(f"  已租: {algo.stats.rented.hash.nice}")
        print(f"  最低价格: {algo.stats.prices.lowest.amount}")
        print(f"  最新价格: {algo.stats.prices.last.amount}")
else:
    print(f"错误: {response.error.message}")

# 获取特定币种的算法
response = await client.info.get_algos(currency="BTC")
```

**示例链接：** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 3. `get_algo()`

获取特定挖矿算法的详细信息。

**签名：**
```python
async def get_algo(name: str, currency: str | None = None) -> MRRResponse[AlgoInfo]
```

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `name` | `str` | 是 | 算法名称（例如 "scrypt"、"sha256"、"x11"） |
| `currency` | `str \| None` | 否 | 按币种过滤。默认返回无过滤的信息。 |

**返回：**
- `MRRResponse[AlgoInfo]` — 包含算法信息的响应
  - 成功时：`MRRResponse(success=True, data=AlgoInfo)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`AlgoInfo` 包含：**
- `name` — 算法内部名称
- `display` — 显示名称
- `suggested_price` — 建议价格（`PriceInfo`）
- `stats` — 算法统计（`AlgoStats`）

!!! tip
    当您需要特定算法的信息时使用此方法，例如在界面中展示或计算租赁费用。

**使用示例：**
```python
# 获取 scrypt 算法信息
response = await client.info.get_algo(name="scrypt")
if response.success:
    algo = response.data
    print(f"算法: {algo.display}")
    print(f"建议价格: {algo.suggested_price.amount} {algo.suggested_price.currency}")
    print(f"可用算力: {algo.stats.available.hash.nice}")
    print(f"已租算力: {algo.stats.rented.hash.nice}")
    print(f"最低价格: {algo.stats.prices.lowest.amount}")
    print(f"最新价格: {algo.stats.prices.last.amount}")
else:
    print(f"错误: {response.error.message}")

# 获取带币种过滤的信息
response = await client.info.get_algo(name="sha256", currency="BTC")
```

**示例链接：** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

### 4. `get_currencies()`

获取可用于支付租赁的币种列表。

**签名：**
```python
async def get_currencies(self) -> MRRResponse[list[CurrencyInfo]]
```

**返回：**
- `MRRResponse[list[CurrencyInfo]]` — 包含币种列表的响应
  - 成功时：`MRRResponse(success=True, data=[CurrencyInfo, ...])`
  - 失败时：`MRRResponse(success=False, error=...)`

**`CurrencyInfo` 包含：**
- `name` — 币种名称（BTC、LTC、ETH、DOGE、BCH）
- `enabled` — 币种启用状态
- `txfee` — 币种交易手续费

!!! note
    此方法返回平台上可用于支付租赁的币种，与 `AccountClient.get_currencies()` 不同，后者返回特定账户的币种状态。

**使用示例：**
```python
response = await client.info.get_currencies()
if response.success:
    print("可用支付币种:")
    for currency in response.data:
        status = "已启用" if currency.enabled else "已禁用"
        print(f"  - {currency.name}: {status} (手续费: {currency.txfee})")
else:
    print(f"错误: {response.error.message}")
```

**示例链接：** [`examples/06_info_and_pricing.py`](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py)

---

## 方法汇总表

| # | 方法 | 描述 | 返回类型 | 示例 |
|---|-------|------|----------|------|
| 1 | `get_servers()` | MRR 服务器列表 | `MRRResponse[ServersList]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 2 | `get_algos(currency)` | 所有挖矿算法 | `MRRResponse[list[AlgoInfo]]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 3 | `get_algo(name, currency)` | 算法信息 | `MRRResponse[AlgoInfo]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |
| 4 | `get_currencies()` | 可用支付币种 | `MRRResponse[list[CurrencyInfo]]` | [06_info_and_pricing.py](https://github.com/GRinvest/aio-mrr/blob/main/examples/06_info_and_pricing.py) |

---

## 附加资源

- [首页](../../index.zh.md)
- [错误处理](../error-handling.zh.md)
- [数据模型](../models.zh.md)
- [认证](../authentication.zh.md)
- [PricingClient](pricing.zh.md)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

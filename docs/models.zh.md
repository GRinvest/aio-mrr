# Pydantic 数据模型

`aio-mrr` 库中所有 Pydantic 模型的完整参考。模型按照 API 功能领域分类分组。

---

## 目录

- [基础模型](#基础模型)
- [账户模型](#账户模型)
- [信息模型](#信息模型)
- [定价模型](#定价模型)
- [租赁模型](#租赁模型)
- [矿机模型](#矿机模型)
- [矿机组模型](#矿机组模型)
- [请求体模型](#请求体模型)

---

## 基础模型

### BaseMRRModel

库中所有 Pydantic 模型的基础模型。使用 `extra="ignore"` 配置，使模型对 API 变更具有容错性 — API 返回的额外字段将被忽略，不会引发验证错误。

```python
from pydantic import BaseModel, ConfigDict

class BaseMRRModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
```

---

### MRRResponseError

请求失败时返回的错误对象。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `code` | `str` | 错误类型：`"network_error"`、`"api_error"`、`"validation_error"`、`"timeout"` |
| `message` | `str` | 人类可读的错误描述 |
| `details` | `dict[str, Any] \| None` | 错误的附加数据 |
| `http_status` | `int \| None` | HTTP 状态码（401、429、500 等） |

详情请参阅：[error-handling.zh.md](./error-handling.zh.md)

---

### MRRResponse[T]

API 响应的通用包装器。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `success` | `bool` | 请求成功时为 `True` |
| `data` | `T \| None` | 类型化数据（错误时为 `None`） |
| `error` | `MRRResponseError \| None` | 错误对象（成功时为 `None`） |
| `http_status` | `int \| None` | HTTP 响应状态码 |
| `retry_count` | `int` | 重试次数 |

详情请参阅：[error-handling.zh.md](./error-handling.zh.md)

---

## 账户模型

用于处理账户、配置文件、矿池和交易的模型。

### AccountInfo

账户详细信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `username` | `str` | 用户名 |
| `email` | `str` | 电子邮件地址 |
| `withdraw` | `dict[str, WithdrawCurrencyInfo]` | 各币种提现信息 |
| `deposit` | `dict[str, DepositCurrencyInfo]` | 各币种充值信息 |
| `notifications` | `NotificationsInfo` | 通知设置 |
| `settings` | `SettingsInfo` | 账户设置 |

---

### BalanceInfo

各币种余额信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `confirmed` | `str` | 已确认余额 |
| `pending` | `float` | 待确认余额 |
| `unconfirmed` | `str` | 未确认余额 |

---

### Transaction

交易记录。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `str` | 交易 ID |
| `type` | `str` | 交易类型 |
| `currency` | `str \| None` | 交易币种 |
| `amount` | `str` | 交易金额 |
| `when` | `str` | 日期/时间（ISO 格式） |
| `rental` | `str \| None` | 租赁 ID（如适用） |
| `rig` | `str \| None` | 矿机 ID（如适用） |
| `txid` | `str \| None` | 区块链交易 ID |
| `txfee` | `str \| None` | 交易手续费 |
| `payout_address` | `str \| None` | 提现地址 |
| `sent` | `str \| None` | 已发送 |
| `status` | `str` | 交易状态 |
| `pending_seconds` | `int \| None` | 等待秒数 |
| `info` | `str \| None` | 附加信息 |

---

### TransactionsList

带分页元数据的交易列表。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `total` | `str` | 交易总数 |
| `returned` | `int` | 返回的记录数 |
| `start` | `int` | 起始位置 |
| `limit` | `int` | 记录限制 |
| `transactions` | `list[Transaction]` | 交易列表 |

---

### Profile

用户的矿池配置文件。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `str` | 配置文件 ID |
| `name` | `str` | 配置文件名称 |
| `algo` | `AlgoProfileInfo` | 配置文件算法信息 |
| `pools` | `list[PoolProfileInfo] \| None` | 配置文件中的矿池列表（可选） |

---

### Pool

已保存矿池的信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `int` | 矿池 ID |
| `type` | `str` | 连接类型（例如 `stratum+tcp`） |
| `name` | `str` | 矿池名称 |
| `host` | `str` | 矿池主机 |
| `port` | `int` | 矿池端口 |
| `user` | `str` | 用户名/工作线程名 |
| `password` | `str` | 密码（别名：`pass`） |
| `notes` | `str \| None` | 备注 |
| `algo` | `AlgoPoolInfo \| None` | 算法信息 |

---

### PoolCreateBody

创建矿池的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `type` | `str` | 连接类型（必填） |
| `name` | `str` | 矿池名称（必填） |
| `host` | `str` | 矿池主机（必填） |
| `port` | `int` | 矿池端口（必填） |
| `user` | `str` | 用户名（必填） |
| `password` | `str \| None` | 密码（别名：`pass`） |
| `notes` | `str \| None` | 备注 |

---

### PoolTestBody

测试矿池的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `method` | `str` | 测试方法：`"simple"` 或 `"full"`（必填） |
| `extramethod` | `str \| None` | 附加方法 |
| `type` | `str \| None` | 连接类型 |
| `host` | `str \| None` | 矿池主机 |
| `port` | `int \| None` | 矿池端口 |
| `user` | `str \| None` | 用户名 |
| `password` | `str \| None` | 密码（别名：`pass`） |
| `source` | `str \| None` | 测试来源 |

---

### PoolTestResult

矿池测试结果。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `result` | `list[PoolTestResultItem]` | 测试结果 |
| `error` | `list[str]` | 错误列表 |

---

### PoolTestResultItem

矿池连接的单项测试结果。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `source` | `str` | 测试来源 |
| `dest` | `str` | 连接目标 |
| `error` | `str` | 连接错误 |
| `connection` | `bool` | 连接是否成功 |
| `executiontime` | `float` | 执行时间（秒） |
| `protocol` | `str \| None` | 协议 |
| `sub` | `bool \| None` | 是否支持 subscription |
| `auth` | `bool \| None` | 认证是否成功 |
| `red` | `bool \| None` | Red 连接 |
| `diffs` | `bool \| None` | 是否支持 diff |
| `diff` | `float \| None` | 难度值 |
| `work` | `bool \| None` | 是否支持 work |
| `xnonce` | `bool \| None` | 是否支持 xnonce |
| `ssl` | `bool \| None` | SSL 连接 |

---

### PoolCreateResponse

创建矿池的响应。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `int` | 已创建矿池的 ID |

---

### ProfileCreateBody

创建配置文件的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 配置文件名称（必填） |
| `algo` | `str` | 算法（必填） |

---

### ProfileCreateResponse

创建配置文件的响应。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `pid` | `str` | 已创建配置文件的 ID |

---

### ProfileDeleteResponse

删除配置文件的响应。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `str` | 已删除配置文件的 ID |
| `success` | `bool` | 删除是否成功 |
| `message` | `str` | 结果消息 |

---

### CurrencyStatus

账户币种状态。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 币种名称 |
| `enabled` | `bool` | 币种是否已启用 |

---

### WithdrawCurrencyInfo

币种提现信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `address` | `str` | 提现地址 |
| `label` | `str` | 币种标签 |
| `auto_pay_threshold` | `str` | 自动支付阈值 |
| `txfee` | `float` | 交易手续费 |

---

### DepositCurrencyInfo

币种充值信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `address` | `str` | 充值地址 |

---

### NotificationsInfo

账户通知设置。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rental_comm` | `str` | 租赁评论通知 |
| `new_rental` | `str` | 新租赁通知 |
| `offline` | `str` | 离线通知 |
| `news` | `str` | 新闻通知 |
| `deposit` | `str` | 充值通知 |

---

### SettingsInfo

账户设置。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `live_data` | `str` | 实时数据模式 |
| `public_profile` | `str` | 公开个人资料 |
| `two_factor_auth` | `str` | 双因素认证 |

---

### AlgoProfileInfo

配置文件中的算法信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 算法名称 |
| `display` | `str` | 显示名称 |
| `suggested_price` | `PriceInfo` | 建议价格 |

---

### PoolProfileInfo

配置文件中的矿池信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `priority` | `int` | 矿池优先级（0-4） |
| `type` | `str` | 连接类型 |
| `host` | `str` | 矿池主机 |
| `port` | `str` | 矿池端口 |
| `user` | `str` | 用户名 |
| `password` | `str` | 密码（别名：`pass`） |
| `status` | `str` | 矿池状态 |

---

### AlgoPoolInfo

矿池的算法信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 算法名称 |
| `display` | `str` | 显示名称 |

---

## 信息模型

用于获取服务器、算法和币种信息的模型。

### AlgoInfo

挖矿算法信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 算法名称 |
| `display` | `str` | 显示名称 |
| `suggested_price` | `PriceInfo` | 建议价格 |
| `stats` | `AlgoStats` | 算法统计 |

---

### AlgoStats

挖矿算法统计。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `available` | `AvailableHashInfo` | 可用算力 |
| `rented` | `RentedHashInfo` | 已租算力 |
| `prices` | `PricesInfo` | 价格信息 |

---

### AvailableHashInfo

可用哈希算力。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigs` | `str` | 矿机数量 |
| `hash` | `HashInfo` | 算力信息 |

---

### RentedHashInfo

已租哈希算力。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigs` | `str` | 矿机数量 |
| `hash` | `HashInfo` | 算力信息 |

---

### PricesInfo

价格信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `lowest` | `PriceInfo` | 最低价格 |
| `last_10` | `PriceInfo` | 最近 10 次租赁的价格 |
| `last` | `PriceInfo` | 最新价格 |

---

### PriceInfo

价格信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `amount` | `str` | 价格金额 |
| `currency` | `str` | 价格币种 |
| `unit` | `str` | 计量单位 |

---

### HashInfo

算力信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `hash` | `float` | 算力值 |
| `unit` | `str` | 计量单位 |
| `nice` | `str` | 格式化显示 |

---

### ServerInfo

MRR 服务器信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `str` | 服务器 ID |
| `name` | `str` | 服务器名称 |
| `region` | `str` | 区域 |
| `port` | `str \| None` | 端口（通用） |
| `ethereum_port` | `str \| None` | Ethereum 端口 |

---

### ServersList

MRR 服务器列表。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `servers` | `list[ServerInfo]` | 服务器列表 |

---

### CurrencyInfo

支付币种信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 币种名称 |
| `enabled` | `bool` | 币种是否已启用 |
| `txfee` | `str` | 交易手续费 |

---

## 定价模型

用于获取汇率和算法市场价格的模型。

### PricingInfo

定价总体信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `conversion_rates` | `ConversionRates` | 币种汇率 |
| `market_rates` | `MarketRates` | 算法市场价格 |

---

### ConversionRates

加密货币之间的汇率。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `LTC` | `str` | LTC 汇率 |
| `ETH` | `str` | ETH 汇率 |
| `BCH` | `str` | BCH 汇率 |
| `DOGE` | `str` | DOGE 汇率 |

---

### MarketRate

算法按币种划分的市场价格。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `BTC` | `str` | BTC 价格 |
| `LTC` | `str` | LTC 价格 |
| `ETH` | `str` | ETH 价格 |
| `BCH` | `str` | BCH 价格 |
| `DOGE` | `str` | DOGE 价格 |

---

### MarketRates

所有算法的市场价格。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `allium` | `MarketRate` | allium 价格 |
| `argon2dchukwa` | `MarketRate` | argon2dchukwa 价格 |
| `autolykosv2` | `MarketRate` | autolykosv2 价格 |
| `kawpow` | `MarketRate` | kawpow 价格 |
| `kheavyhash` | `MarketRate` | kheavyhash 价格 |
| `randomx` | `MarketRate` | randomx 价格 |
| `scrypt` | `MarketRate` | scrypt 价格 |
| `sha256` | `MarketRate` | sha256 价格 |
| `x11` | `MarketRate` | x11 价格 |

---

## 租赁模型

用于处理租赁的模型。

### RentalInfo

租赁信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `str` | 租赁 ID |
| `rig_id` | `str \| None` | 矿机 ID（可选） |
| `rig_name` | `str \| None` | 矿机名称 |
| `owner` | `str \| None` | 矿机所有者 |
| `renter` | `str \| None` | 承租人 |
| `status` | `str \| None` | 租赁状态 |
| `started` | `str \| None` | 开始时间 |
| `ends` | `str \| None` | 结束时间 |
| `length` | `float \| None` | 时长（小时） |
| `currency` | `str \| None` | 支付币种 |
| `rate` | `RateInfo \| None` | 费率信息 |
| `hash` | `RentalHashInfo \| None` | 算力信息 |
| `cost` | `RentalCostInfo \| None` | 费用信息 |

---

### RentalLogEntry

租赁日志记录。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `time` | `str` | 事件时间 |
| `message` | `str` | 事件消息 |

---

### RentalMessage

租赁消息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `time` | `str` | 消息时间 |
| `user` | `str` | 发送者 |
| `message` | `str` | 消息内容 |

---

### GraphData

租赁算力图表数据。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `hashrate_data` | `list[GraphDataPoint] \| None` | 算力数据 |
| `downtime_data` | `list[GraphDataPoint] \| None` | 停机数据 |
| `hours` | `float \| None` | 小时数 |

---

### GraphDataPoint

图表数据点。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `time` | `str \| None` | 数据点时间 |
| `hashrate` | `float \| None` | 数据点算力 |
| `downtime` | `bool \| None` | 数据点是否停机 |

---

### RateInfo

租赁费率信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `type` | `str \| None` | 费率类型（别名：`rate.type`） |
| `price` | `str \| None` | 费率价格（别名：`rate.price`） |

---

### RentalHashInfo

租赁算力信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `hash` | `float \| None` | 算力值 |
| `type` | `str \| None` | 算法类型 |

---

### RentalCostInfo

租赁费用信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `amount` | `str \| None` | 费用金额 |
| `currency` | `str \| None` | 费用币种 |

---

### RentalCreateBody

创建租赁的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rig` | `int` | 矿机 ID（必填） |
| `length` | `float` | 时长（小时，必填） |
| `profile` | `int` | 配置文件 ID（必填） |
| `currency` | `str \| None` | 支付币种 |
| `rate_type` | `str \| None` | 费率类型（别名：`rate.type`） |
| `rate_price` | `float \| None` | 费率价格（别名：`rate.price`） |

---

### RentalPoolBody

更新租赁矿池的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `host` | `str` | 矿池主机（必填） |
| `port` | `int` | 矿池端口（必填） |
| `user` | `str` | 用户名（必填） |
| `password` | `str` | 密码（别名：`pass`，必填） |
| `priority` | `int \| None` | 矿池优先级 |

---

## 矿机模型

用于处理矿机的模型。

### RigInfo

矿机信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `int` | 矿机 ID |
| `name` | `str` | 矿机名称 |
| `description` | `str \| None` | 矿机描述 |
| `server` | `str \| None` | 矿机服务器 |
| `status` | `dict[str, Any] \| str \| None` | 矿机状态（可能是字符串或字典） |
| `price` | `dict[str, RigPriceInfo] \| None` | 价格信息（按币种） |
| `price_type` | `str \| None` | 价格类型（别名：`price.type`） |
| `minhours` | `float \| None` | 最小租赁时间 |
| `maxhours` | `float \| None` | 最大租赁时间 |
| `extensions` | `bool \| None` | 是否可续期 |
| `hash` | `RigHashInfo \| None` | 算力信息 |
| `suggested_diff` | `float \| None` | 建议难度 |
| `ndevices` | `int \| None` | 设备数量 |
| `type` | `str \| None` | 矿机类型 |
| `region` | `str \| None` | 区域 |
| `online` | `bool \| None` | 在线状态 |
| `rented` | `bool \| None` | 是否已出租 |
| `last_hashrate` | `float \| None` | 最新算力 |
| `rpi` | `int \| None` | RPI 指数 |
| `owner` | `str \| None` | 所有者 |

---

### RigPortInfo

矿机服务器端口信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigid` | `str \| None` | 矿机 ID（可选） |
| `port` | `int` | 服务器端口 |
| `server` | `str \| None` | 服务器名称（可选） |
| `worker` | `str \| None` | 连接用的 worker 名称（可选） |

---

### RigThreadInfo

矿机工作线程信息（按矿机分组）。

GET /rig/{ids}/threads 的响应返回矿机组及其线程的列表。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigid` | `str \| None` | 矿机 ID |
| `access` | `str \| None` | 访问级别（owner/renter） |
| `threads` | `list[RigThreadDetail]` | 线程详情列表 |

### RigThreadDetail

单个矿机线程的详情。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `int \| None` | 线程 ID |
| `worker` | `str \| None` | Worker 名称 |
| `status` | `str \| None` | 线程状态 |
| `hashrate` | `float \| None` | 线程算力 |
| `last_share` | `str \| None` | 最后一次提交 share 的时间 |

---

### RigGraphData

矿机算力图表数据。

GET /rig/{ids}/graph 的响应以 chartdata 的新格式返回数据。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigid` | `str \| None` | 矿机 ID |
| `chartdata` | `dict[str, Any] \| None` | 图表数据（time_start、time_end、timestamp_start、timestamp_end、bars） |

**`chartdata` 结构：**

| 字段 | 类型 | 描述 |
|------|-----|------|
| `time_start` | `str` | 时间范围起始 |
| `time_end` | `str` | 时间范围结束 |
| `timestamp_start` | `int` | 起始时间戳 |
| `timestamp_end` | `int` | 结束时间戳 |
| `bars` | `str` | 数据格式为 "[ts,val],[ts,val],..." |

---

### RigGraphDataPoint

矿机图表数据点。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `time` | `str` | 数据点时间 |
| `hashrate` | `float \| None` | 数据点算力 |
| `downtime` | `bool \| None` | 数据点是否停机 |

---

### RigPriceInfo

矿机按币种的价格信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `enabled` | `bool \| None` | 币种是否已启用 |
| `price` | `float \| None` | 价格 |
| `autoprice` | `bool \| None` | 自动定价 |
| `minimum` | `float \| None` | 最低价格 |
| `modifier` | `str \| None` | 价格修正系数 |

---

### RigHashInfo

矿机算力信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `hash` | `float \| None` | 算力值 |
| `type` | `str \| None` | 算法类型 |

---

### RigCreateBody

创建矿机的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 矿机名称（必填） |
| `description` | `str \| None` | 矿机描述 |
| `status` | `str \| None` | 矿机状态 |
| `server` | `str` | 矿机服务器（必填） |
| `price_btc_enabled` | `bool \| None` | 是否启用 BTC（别名：`price.btc.enabled`） |
| `price_btc_price` | `float \| None` | BTC 价格（别名：`price.btc.price`） |
| `price_btc_autoprice` | `bool \| None` | BTC 自动定价（别名：`price.btc.autoprice`） |
| `price_btc_minimum` | `float \| None` | BTC 最低价格（别名：`price.btc.minimum`） |
| `price_btc_modifier` | `str \| None` | BTC 修正系数（别名：`price.btc.modifier`） |
| `price_ltc_enabled` | `bool \| None` | 是否启用 LTC（别名：`price.ltc.enabled`） |
| `price_eth_enabled` | `bool \| None` | 是否启用 ETH（别名：`price.eth.enabled`） |
| `price_doge_enabled` | `bool \| None` | 是否启用 DOGE（别名：`price.doge.enabled`） |
| `price_type` | `str \| None` | 价格类型（别名：`price.type`） |
| `minhours` | `float \| None` | 最短时间 |
| `maxhours` | `float \| None` | 最长时间 |
| `extensions` | `bool \| None` | 是否可续期 |
| `hash_hash` | `float \| None` | 算力（别名：`hash.hash`） |
| `hash_type` | `str \| None` | 算法类型（别名：`hash.type`） |
| `suggested_diff` | `float \| None` | 建议难度 |
| `ndevices` | `int \| None` | 设备数量 |

---

### RigBatchBody

批量更新矿机的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `rigs` | `list[dict[str, object]]` | 要更新的矿机列表（必填） |

---

### RigPoolBody

更新矿机矿池的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `host` | `str` | 矿池主机（必填） |
| `port` | `int` | 矿池端口（必填） |
| `user` | `str` | 用户名（必填） |
| `password` | `str` | 密码（别名：`pass`，必填） |
| `priority` | `int \| None` | 矿池优先级 |

---

## 矿机组模型

用于处理矿机组的模型。

### RigGroupInfo

矿机组信息。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `id` | `str` | 组 ID |
| `name` | `str` | 组名称 |
| `enabled` | `bool` | 组是否启用 |
| `rental_limit` | `int` | 租赁限制 |
| `rigs` | `list[int]` | 组内矿机 ID 列表 |
| `algo` | `str \| None` | 组算法 |

---

### RigGroupCreateBody

创建矿机组的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str` | 组名称（必填） |
| `enabled` | `bool` | 是否启用组（默认 `True`） |
| `rental_limit` | `int` | 租赁限制（默认 `1`） |

---

### RigGroupUpdateBody

更新矿机组的请求体。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `name` | `str \| None` | 新组名称 |
| `enabled` | `bool \| None` | 新启用状态 |
| `rental_limit` | `int \| None` | 新租赁限制 |

---

## 请求体模型

用于请求参数的附加模型。

### TransactionsQueryParams

获取交易的查询参数。

| 字段 | 类型 | 描述 |
|------|-----|------|
| `start` | `int \| None` | 起始位置 |
| `limit` | `int \| None` | 记录限制 |
| `algo` | `str \| None` | 按算法过滤 |
| `type` | `str \| None` | 按类型过滤 |
| `rig` | `int \| None` | 按矿机过滤 |
| `rental` | `int \| None` | 按租赁过滤 |
| `txid` | `str \| None` | 按 txid 过滤 |
| `time_greater_eq` | `str \| None` | 时间 >=（ISO） |
| `time_less_eq` | `str \| None` | 时间 <=（ISO） |

---

## 另请参阅

- [« 返回首页](./index.zh.md)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

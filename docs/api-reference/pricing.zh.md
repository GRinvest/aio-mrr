# PricingClient — API 参考

`PricingClient` 方法的参考文档，用于获取 MiningRigRentals 上加密货币汇率和挖矿算法市场价格的信息。

## 概述

`PricingClient` 提供以下方法：

- 获取加密货币（LTC、ETH、BCH、DOGE）之间的实时汇率
- 查看所有挖矿算法的市场价格

---

## 方法

### 1. `get_pricing()`

获取实时汇率和挖矿算法市场价格。

**签名：**

```python
async def get_pricing(self) -> MRRResponse[PricingInfo]
```

**返回：**

- `MRRResponse[PricingInfo]` — 包含定价信息的响应
  - 成功时：`MRRResponse(success=True, data=PricingInfo)`
  - 失败时：`MRRResponse(success=False, error=...)`

**`PricingInfo` 包含：**

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `conversion_rates` | `ConversionRates` | 加密货币之间的汇率 |
| `market_rates` | `MarketRates` | 挖矿算法的市场价格 |

### `ConversionRates` 结构

主要加密货币之间的汇率：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `LTC` | `str` | Litecoin 汇率（例如 "0.02345678"） |
| `ETH` | `str` | Ethereum 汇率（例如 "0.00123456"） |
| `BCH` | `str` | Bitcoin Cash 汇率（例如 "0.00098765"） |
| `DOGE` | `str` | Dogecoin 汇率（例如 "123.45678901"） |

!!! note
    汇率允许在租赁矿机时在不同币种之间转换价格。

### `MarketRates` 结构

每个挖矿算法的市场价格。每个算法提供 5 种币种的价格：

| 算法 | BTC | LTC | ETH | BCH | DOGE |
| --- | --- | --- | --- | --- | --- |
| `allium` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `argon2dchukwa` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `autolykosv2` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `kawpow` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `kheavyhash` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `randomx` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `scrypt` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `sha256` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |
| `x11` | BTC 价格 | LTC 价格 | ETH 价格 | BCH 价格 | DOGE 价格 |

### `MarketRate` 结构

每个算法可用以下结构：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `BTC` | `str` | Bitcoin 市场价格 |
| `LTC` | `str` | Litecoin 市场价格 |
| `ETH` | `str` | Ethereum 市场价格 |
| `BCH` | `str` | Bitcoin Cash 市场价格 |
| `DOGE` | `str` | Dogecoin 市场价格 |

!!! tip
    使用 `market_rates` 了解所选币种中特定算法矿机租赁的当前成本。

**使用示例：**

```python
response = await client.pricing.get_pricing()
if response.success:
    pricing = response.data
    
    # 输出汇率
    print("汇率:")
    print(f"  LTC: {pricing.conversion_rates.LTC}")
    print(f"  ETH: {pricing.conversion_rates.ETH}")
    print(f"  BCH: {pricing.conversion_rates.BCH}")
    print(f"  DOGE: {pricing.conversion_rates.DOGE}")
    
    # 输出 scrypt 算法的市场价格
    print("\nscrypt 市场价格:")
    scrypt_rates = pricing.market_rates.scrypt
    print(f"  BTC: {scrypt_rates.BTC}")
    print(f"  LTC: {scrypt_rates.LTC}")
    print(f"  ETH: {scrypt_rates.ETH}")
    print(f"  BCH: {scrypt_rates.BCH}")
    print(f"  DOGE: {scrypt_rates.DOGE}")
    
    # 输出所有算法
    print("\n所有算法市场价格:")
    for algo_name in ["allium", "argon2dchukwa", "autolykosv2", "kawpow",
                      "kheavyhash", "randomx", "scrypt", "sha256", "x11"]:
        algo_rates = getattr(pricing.market_rates, algo_name)
        print(f"  {algo_name}: BTC={algo_rates.BTC}, LTC={algo_rates.LTC}")
else:
    print(f"错误: {response.error.message}")
```

---

## 方法汇总表

| # | 方法 | 描述 | 返回类型 | 示例 |
| --- | --- | --- | --- | --- |
| 1 | `get_pricing()` | 汇率和市场价格 | `MRRResponse[PricingInfo]` | — |

---

## 附加资源

- [首页](../../index.zh.md)
- [错误处理](../error-handling.zh.md)
- [数据模型](../models.zh.md)
- [认证](../authentication.zh.md)
- [InfoClient](info.zh.md)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

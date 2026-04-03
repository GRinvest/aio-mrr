# aio-mrr 文档

用于 MiningRigRentals API v2 的异步 Python 库。

## 概述

`aio-mrr` 是一个现代化的异步客户端，用于与 MiningRigRentals API v2 集成。该库基于 Python 3.12+ 的现代特性，为全部 56 个公共 API 方法提供类型化接口。

该库的核心特性是完全不使用异常：所有响应都封装在统一的 `MRRResponse[T]` 类型中，这简化了错误处理并使代码更加可预测。

## 核心特性

- **async/await** — 基于 `aiohttp` 的完全异步 API
- **Pydantic v2** — 通过 Pydantic 模型对所有响应进行严格类型化
- **重试策略** — 在网络错误和速率限制时自动重试（通过 `tenacity`）
- **HMAC-SHA1 认证** — 安全的请求签名，支持密钥掩码
- **连接池** — 为高负载场景提供高效的连接管理
- **Result 模式** — 使用 Result 模式替代异常进行错误处理

## 系统要求

- **Python**: 3.12+
- **依赖项**:
  - `aiohttp>=3.13.0` — 异步 HTTP 客户端
  - `pydantic>=2.12.0` — 数据验证和类型化
  - `tenacity>=9.1.0` — 重试策略
  - `loguru>=0.7.0` — 日志记录

## 安装

### 稳定版本

```bash
pip install aio-mrr
```

### 开发版本

如需开发和测试，请以可编辑模式安装并附带额外依赖：

```bash
pip install -e ".[dev]"
```

---

## 快速开始

!!! tip "快速开始"

    客户端初始化和执行请求的最小示例：

    ```python
    import os
    import asyncio
    from aio_mrr import MRRClient

    async def main():
        # 从环境变量加载密钥
        api_key = os.environ.get("MRR_API_KEY")
        api_secret = os.environ.get("MRR_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("必须设置 MRR_API_KEY 和 MRR_API_SECRET")

        # 使用上下文管理器初始化客户端
        async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
            # 验证认证
            response = await client.whoami()
            if not response.success:
                print(f"认证错误: {response.error}")
                return

            print(f"登录为: {response.data}")

            # 获取余额
            balance = await client.account.get_balance()
            if balance.success:
                print(f"余额: {balance.data}")

    asyncio.run(main())
    ```

    另请参阅: [`examples/01_quickstart.py`](examples/01_quickstart.py)

---

## 目录

### 入门指南

- **[安装与认证](authentication.zh.md)** — 获取 API 密钥、初始化客户端、HMAC-SHA1 认证
- **[错误处理](error-handling.zh.md)** — Result 模式、错误类型、重试策略
- **[数据模型](models.zh.md)** — 库中所有 Pydantic 模型的完整说明

### API 参考

- **[账户与配置文件](api-reference/account.zh.md)** — 16 个管理账户、矿池和配置文件的方法
- **[矿机](api-reference/rigs.zh.md)** — 15 个管理矿机的方法（CRUD、搜索、图表）
- **[租赁](api-reference/rentals.zh.md)** — 12 个管理租赁的方法（创建、续期、日志）
- **[矿机组](api-reference/rig-groups.zh.md)** — 7 个管理矿机组的方法
- **[信息](api-reference/info.zh.md)** — 4 个获取服务器和算法信息的方法
- **[定价](api-reference/pricing.zh.md)** — 1 个获取汇率和市场价格的方法

---

## 示例

仓库中提供了 10 个即用示例，涵盖各种使用场景：

| 文件 | 描述 |
| --- | --- |
| [`examples/01_quickstart.py`](examples/01_quickstart.py) | 基本初始化、whoami、余额查询 |
| [`examples/02_account_balance.py`](examples/02_account_balance.py) | 配置文件、余额、交易记录 |
| [`examples/03_manage_rigs.py`](examples/03_manage_rigs.py) | 获取、创建、删除矿机 |
| [`examples/04_create_rental.py`](examples/04_create_rental.py) | 创建租赁、续期、日志 |
| [`examples/05_rig_groups.py`](examples/05_rig_groups.py) | 矿机组 CRUD、添加/删除 |
| [`examples/06_info_and_pricing.py`](examples/06_info_and_pricing.py) | 服务器、算法、汇率、价格 |
| [`examples/07_error_handling_demo.py`](examples/07_error_handling_demo.py) | 所有错误类型演示 |
| [`examples/08_advanced_search.py`](examples/08_advanced_search.py) | 带过滤条件的矿机搜索 |
| [`examples/09_pool_management.py`](examples/09_pool_management.py) | 矿池 CRUD、矿池测试 |
| [`examples/10_profile_management.py`](examples/10_profile_management.py) | 配置文件 CRUD、优先级 |

!!! note "注意"

    所有示例都使用环境变量存储 API 密钥。请勿将密钥硬编码在代码中！

    ```bash
    export MRR_API_KEY="your_api_key"
    export MRR_API_SECRET="your_api_secret"
    ```

---

## 安全

- **请勿将 API 密钥存储在代码中** — 始终使用环境变量
- 库通过 `SecretMasker` 自动在日志中掩码密钥
- 运行前请检查密钥是否存在：`if not api_key: raise ValueError(...)`

---

## 链接

- 源代码: [GitHub](https://github.com/GRinvest/aio-mrr)
- 示例仓库: [examples/](https://github.com/GRinvest/aio-mrr/tree/main/examples/)
- MiningRigRentals API: [https://miningrigrentals.com](https://miningrigrentals.com)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

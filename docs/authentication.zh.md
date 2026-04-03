# 客户端认证与初始化

## 获取 API 密钥

使用 `aio-mrr` 库需要 MiningRigRentals 账户的 API 密钥。

### 在哪里找到 API 密钥

1. 登录您的 [MiningRigRentals.com](https://www.miningrigrentals.com) 账户
2. 进入 **个人中心** → **API Keys**（在顶部菜单中）
3. 点击 **Create New API Key**
4. 为密钥命名（例如 "aio-mrr integration"）
5. 复制并保存：
   - **API Key**（公开标识符）
   - **API Secret**（密钥 — 仅显示一次！）

> !!! warning "安全提示"
> 切勿分享您的 API Secret，也不要将其上传到公开仓库。

---

## 初始化 MRRClient

`MRRClient` 类是与 API 交互的主要入口点。

### 构造函数参数

| 参数 | 类型 | 必填 | 描述 |
|----------|-----|------|------|
| `api_key` | `str` | **是** | MRR 个人账户中的公开 API 密钥 |
| `api_secret` | `str` | **是** | MRR 个人账户中的密钥 |
| `connect_timeout` | `float` | 否 | 连接超时（默认：`30.0` 秒） |
| `read_timeout` | `float` | 否 | 读取响应超时（默认：`60.0` 秒） |
| `max_retries` | `int` | 否 | 网络错误时的最大重试次数（默认：`3`） |

### 使用上下文管理器（推荐）

上下文管理器自动管理客户端的生命周期 — 打开和关闭连接。

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    # 从环境变量加载密钥（切勿硬编码！）
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("未找到 API 密钥。请设置环境变量 MRR_API_KEY 和 MRR_API_SECRET")

    # 使用上下文管理器
    async with MRRClient(
        api_key=api_key,
        api_secret=api_secret,
        connect_timeout=30.0,
        read_timeout=60.0,
        max_retries=3
    ) as client:
        # 所有请求在块内执行
        response = await client.whoami()
        if response.success:
            print(f"认证成功: {response.data}")
        else:
            print(f"错误: {response.error}")

asyncio.run(main())
```

### 不使用上下文管理器

如果您需要对客户端生命周期进行更多控制：

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("未找到 API 密钥")

    # 手动创建客户端
    client = MRRClient(
        api_key=api_key,
        api_secret=api_secret
    )

    try:
        # 执行请求
        response = await client.whoami()
        if response.success:
            print(f"用户: {response.data}")
    finally:
        # 重要：务必手动关闭客户端
        await client.close()

asyncio.run(main())
```

---

## HMAC-SHA1 认证

库使用 HMAC-SHA1 对请求进行签名，以确保数据的完整性和真实性。

### 工作原理

对于每个 API 请求，库自动生成以下请求头：

| 请求头 | 描述 | 示例 |
|-----------|------|------|
| `x-api-key` | 公开 API 密钥 | `x-api-key: "abc123..."` |
| `x-api-nonce` | 唯一请求编号（时间戳 + 随机数） | `x-api-nonce: "1712345678901_xyz"` |
| `x-api-sign` | 请求体的 HMAC-SHA1 签名 | `x-api-sign: "sha1=..."` |

### 签名过程

1. 生成 **nonce**（唯一请求标识符）
2. 构建签名字符串：`method + path + nonce + body`
3. 使用 `api_secret` 计算 **HMAC-SHA1** 哈希
4. 将签名添加到 `x-api-sign` 请求头

> !!! note
> 您无需手动签名请求 — 库会自动完成。

---

## `whoami()` 方法

`whoami()` 方法是验证认证的基本方式。

### 签名

```python
async def whoami() -> MRRResponse[dict[str, str]]
```

### 返回值

认证成功后，该方法返回包含账户信息的字典：

```python
{
    "username": "your_username",
    "user_id": "12345"
}
```

### 使用示例

```python
response = await client.whoami()

if response.success:
    username = response.data["username"]
    print(f"欢迎, {username}!")
else:
    print(f"认证错误: {response.error.message}")
```

---

## 安全

### ⚠️ 切勿硬编码 API 密钥

**错误做法：**
```python
# ❌ 永远不要这样做！
client = MRRClient(
    api_key="your_real_api_key",
    api_secret="your_real_api_secret"
)
```

**正确做法：**
```python
# ✅ 使用环境变量
import os

api_key = os.environ.get("MRR_API_KEY")
api_secret = os.environ.get("MRR_API_SECRET")

client = MRRClient(
    api_key=api_key,
    api_secret=api_secret
)
```

### 设置环境变量

#### Linux / macOS：
```bash
export MRR_API_KEY="your_api_key_here"
export MRR_API_SECRET="your_api_secret_here"
```

#### Windows (PowerShell)：
```powershell
$env:MRR_API_KEY="your_api_key_here"
$env:MRR_API_SECRET="your_api_secret_here"
```

#### Windows (CMD)：
```cmd
set MRR_API_KEY=your_api_key_here
set MRR_API_SECRET=your_api_secret_here
```

> !!! tip "提示"
> 如果使用本地 `.env` 文件进行测试，请将 `.env` 添加到 `.gitignore` 中。

---

## 另请参阅

- [快速开始示例](../examples/01_quickstart.py) — 基本初始化和首次请求
- [错误处理](./error-handling.zh.md) — 如何处理 API 错误
- [首页](./index.zh.md) — 文档目录

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

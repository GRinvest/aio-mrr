# 错误处理

## 架构设计

`aio-mrr` 库使用 **Result 模式** 进行错误处理。所有方法都返回 `MRRResponse[T]` 包装器，其中包含请求的执行结果。

> **重要：** 库 **不会向外抛出异常**。所有错误（网络错误、超时、API 错误、验证错误）都通过 `MRRResponse` 结构返回。

这样做的好处：
- 无需 try/except 块即可显式处理错误
- 成功时获取类型化数据
- 失败时获取详细的错误信息
- 可追踪重试次数

---

## MRRResponse[T] 结构

所有库方法响应的通用包装器：

```python
from typing import Generic, TypeVar, Any

T = TypeVar('T')

class MRRResponse(BaseMRRModel, Generic[T]):
    """API 响应的通用包装器。"""
    
    success: bool              # 请求成功为 True，失败为 False
    data: T | None             # 类型化数据（错误时为 None）
    error: MRRResponseError | None  # 错误对象（成功时为 None）
    http_status: int | None    # HTTP 响应状态码
    retry_count: int           # 重试次数（未重试则为 0）
```

### MRRResponse 字段

| 字段 | 类型 | 描述 |
|------|-----|------|
| `success` | `bool` | 成功标志：请求成功时为 `True`，错误时为 `False` |
| `data` | `T \| None` | 类型化响应数据。成功时包含结果，错误时为 `None` |
| `error` | `MRRResponseError \| None` | 错误对象。成功时为 `None`，错误时包含详细信息 |
| `http_status` | `int \| None` | HTTP 响应状态码（200、401、429、500 等） |
| `retry_count` | `int` | 已执行的重试次数（首次请求成功则为 0） |

---

## MRRResponseError 结构

错误对象包含有关所发生错误的详细信息：

```python
class MRRResponseError(BaseMRRModel):
    """错误详情。"""
    
    code: str                          # 错误类型（见下文）
    message: str                       # 人类可读的错误描述
    details: dict[str, Any] | None     # 错误的附加数据
    http_status: int | None            # HTTP 状态码（如适用）
```

### MRRResponseError 字段

| 字段 | 类型 | 描述 |
|------|-----|------|
| `code` | `str` | 错误类型代码：`"network_error"`、`"timeout"`、`"api_error"`、`"validation_error"` |
| `message` | `str` | 人类可读的错误描述 |
| `details` | `dict[str, Any] \| None` | 附加数据（例如异常或验证详情） |
| `http_status` | `int \| None` | HTTP 状态码（如果错误与 HTTP 响应相关） |

---

## 错误类型

库定义了 4 种错误类型。每种类型在 `error.code` 字段中具有唯一代码。

### 1. 网络错误 (`"network_error"`)

**描述：** 网络错误 — 无法与 MRR 服务器建立连接。

**原因：**
- DNS 错误（未找到主机）
- 连接被拒绝（服务器无响应）
- 代理不可用
- 无网络连接

**错误示例：**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "network_error",
        "message": "Failed to establish connection: Name or service not known",
        "details": {"host": "api.miningrigrentals.com", "port": 443},
        "http_status": None
    },
    "http_status": None,
    "retry_count": 3
}
```

**处理示例：**
```python
from aio_mrr import MRRClient

async def check_connection():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.whoami()
        
        if not response.success:
            if response.error and response.error.code == "network_error":
                print(f"❌ 网络错误: {response.error.message}")
                print(f"   尝试次数: {response.retry_count}")
                return
            
            print(f"❌ 错误: {response.error}")
            return
        
        print(f"✅ 连接成功: {response.data}")
```

---

### 2. 超时 (`"timeout"`)

**描述：** 请求超过了设定的等待时间。

**原因：**
- 服务器在超时时间内未响应
- 网络连接缓慢
- MRR 服务器过载

**错误示例：**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "timeout",
        "message": "Request timed out after 60.0 seconds",
        "details": {"timeout": 60.0, "endpoint": "/api/v2/account"},
        "http_status": None
    },
    "http_status": None,
    "retry_count": 3
}
```

**处理示例：**
```python
async def get_account():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_account()
        
        if not response.success:
            if response.error and response.error.code == "timeout":
                print(f"⏱️ 请求超时: {response.error.message}")
                print(f"   请尝试增加 connect_timeout/read_timeout")
                return
            
            print(f"❌ 错误: {response.error}")
            return
        
        print(f"✅ 账户数据: {response.data.username}")
```

---

### 3. API 错误 (`"api_error"`)

**描述：** MRR API 返回的错误（4xx、5xx 状态码）。

**原因：**
- API 密钥无效（401）
- 权限不足（403）
- 资源未找到（404）
- 请求过于频繁 — 速率限制（429）
- MRR 服务器错误（500、502、503、504）
- 请求参数无效（400）

**错误示例：**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "api_error",
        "message": "Invalid API key",
        "details": {"endpoint": "/api/v2/account/whoami"},
        "http_status": 401
    },
    "http_status": 401,
    "retry_count": 0
}
```

**处理示例：**
```python
async def get_balance():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()
        
        if not response.success:
            if response.error and response.error.code == "api_error":
                status = response.error.http_status
                
                if status == 401:
                    print("🔐 认证错误: 请检查 API 密钥")
                elif status == 403:
                    print("🚫 访问被拒绝: 请检查 API 密钥权限")
                elif status == 404:
                    print("📭 资源未找到")
                elif status == 429:
                    print("⏳ 请求过于频繁: 请稍后重试")
                elif status and status >= 500:
                    print(f"🔧 MRR 服务器错误 (HTTP {status}): 请稍后重试")
                else:
                    print(f"❌ API 错误 (HTTP {status}): {response.error.message}")
                return
            
            print(f"❌ 错误: {response.error}")
            return
        
        print(f"✅ 余额: {response.data}")
```

---

### 4. 验证错误 (`"validation_error"`)

**描述：** 解析 API 响应时的 Pydantic 验证错误。

**原因：**
- API 返回了意外的数据格式
- 缺少必填字段
- 数据类型不匹配

**错误示例：**
```python
{
    "success": False,
    "data": None,
    "error": {
        "code": "validation_error",
        "message": "Validation error: field 'username' required but not found",
        "details": {"errors": [{"loc": ("username",), "msg": "field required"}]},
        "http_status": 200
    },
    "http_status": 200,
    "retry_count": 0
}
```

**处理示例：**
```python
async def get_rigs():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.rig.get_mining_rigs(type="gpu")
        
        if not response.success:
            if response.error and response.error.code == "validation_error":
                print("🔧 验证错误: API 返回了意外的数据格式")
                print(f"   {response.error.message}")
                print("   MRR API 可能已更改响应格式")
                return
            
            print(f"❌ 错误: {response.error}")
            return
        
        print(f"✅ 找到矿机数: {len(response.data)}")
```

---

## 结果处理模式

所有示例中推荐的响应处理模式：

```python
from aio_mrr import MRRClient

async def main():
    async with MRRClient(api_key="...", api_secret="...") as client:
        # 1. 调用方法
        response = await client.account.get_balance()
        
        # 2. 检查是否成功
        if not response.success:
            # 3. 处理错误
            print(f"错误: {response.error}")
            return
        
        # 4. 处理数据
        print(f"余额: {response.data}")
```

### 通用错误处理器

```python
from aio_mrr import MRRClient, MRRResponse

def handle_error(response: MRRResponse) -> bool:
    """
    通用错误处理。
    如果错误已处理则返回 True，否则返回 False 以便进一步处理。
    """
    if response.success:
        return True
    
    if response.error:
        error = response.error
        
        # 网络错误
        if error.code == "network_error":
            print(f"❌ 网络: {error.message}")
            return True
        
        # 超时
        if error.code == "timeout":
            print(f"⏱️ 超时: {error.message}")
            return True
        
        # API 错误
        if error.code == "api_error":
            status = error.http_status
            if status == 401:
                print("🔐 API 密钥无效")
            elif status == 429:
                print(f"⏳ 速率限制 (HTTP {status}): retry_count={response.retry_count}")
            elif status and status >= 500:
                print(f"🔧 MRR 服务器 (HTTP {status}): retry_count={response.retry_count}")
            else:
                print(f"❌ API 错误 (HTTP {status}): {error.message}")
            return True
        
        # 验证错误
        if error.code == "validation_error":
            print(f"🔧 验证: {error.message}")
            return True
    
    # 未知错误
    print(f"❌ 未知错误: {response.error}")
    return False

async def main():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()
        
        if not handle_error(response):
            return
        
        print(f"✅ 余额: {response.data}")
```

---

## HTTP 客户端重试策略

库在遇到临时错误时会自动重试请求。重试策略取决于错误类型：

### 重试策略

| 错误类型 | 状态码 | 重试次数 | 退避策略 | 抖动 |
|------------|------|----------|---------|------|
| 速率限制 (429) | 429 | 5 | 5-60 秒（指数） | ✅ 是 |
| 服务器错误 | 500, 502, 503, 504 | 3 | 1-8 秒（指数） | ✅ 是 |
| 连接错误 | DNS、连接被拒绝 | 3 | 1-8 秒（指数） | ✅ 是 |
| 超时 | aiohttp.ServerTimeoutError | 3 | 1-8 秒（指数） | ✅ 是 |
| API 错误 (4xx) | 400, 401, 403, 404 等 | 0 | — | — |

### 指数退避 + 抖动

**指数退避：** 每次重试之间的等待时间呈指数增长。

**抖动：** 在等待时间上添加随机值，以防止"惊群效应"。

#### 429（速率限制）示例：
```
尝试 1: 0 秒（首次请求）
尝试 2: ~5 秒  (5 + 抖动)
尝试 3: ~10 秒 (10 + 抖动)
尝试 4: ~20 秒 (20 + 抖动)
尝试 5: ~40 秒 (40 + 抖动)
尝试 6: ~60 秒 (60 + 抖动) — 最大值
```

#### 500/连接错误示例：
```
尝试 1: 0 秒（首次请求）
尝试 2: ~1 秒  (1 + 抖动)
尝试 3: ~2 秒  (2 + 抖动)
尝试 4: ~4 秒  (4 + 抖动)
尝试 5: ~8 秒  (8 + 抖动) — 最大值
```

### 在响应中检查重试

```python
async def check_retry():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()
        
        if not response.success:
            if response.error and response.error.code == "api_error":
                status = response.error.http_status
                
                if status == 429:
                    print(f"⏳ 速率限制！已执行 {response.retry_count} 次重试")
                    print(f"   请稍后重试")
                elif status and status >= 500:
                    print(f"🔧 服务器错误 (HTTP {status})")
                    print(f"   重试次数: {response.retry_count}")
                    if response.retry_count >= 3:
                        print(f"   已达到最大重试次数 — 请稍后重试")
```

---

## 代码示例

### 处理所有错误类型的完整示例

示例演示：
- 处理 `network_error`
- 处理 `timeout`
- 处理 `api_error`（401、429、500）
- 处理 `validation_error`
- 重试时检查 `retry_count`

---

## 链接

- [« 返回首页](./index.zh.md)

- [认证](./authentication.zh.md)

---

<hr />
<p align="center">
  <i>aio-mrr 是 <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT 许可</a> 的代码。</i><br/>
  <i>由 <a href="https://sibneuro.tech">SibNeuroTech</a> 在俄罗斯新西伯利亚设计与构建</i><br/>
  <i>联系方式: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

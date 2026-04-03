# Error Handling

## Architectural Decision

The `aio-mrr` library uses the **Result pattern** for error handling. All methods return an `MRRResponse[T]` wrapper containing the request result.

> **Important:** The library **does NOT throw exceptions** outward. All errors (network, timeouts, API errors, validation errors) are returned through the `MRRResponse` structure.

This allows you to:
- Handle errors explicitly without try/except blocks
- Receive typed data on success
- Receive detailed error information on failure
- Track the number of retry attempts

---

## MRRResponse[T] Structure

Universal response wrapper for all library methods:

```python
from typing import Generic, TypeVar, Any

T = TypeVar('T')

class MRRResponse(BaseMRRModel, Generic[T]):
    """Universal API response wrapper."""

    success: bool              # True if the request succeeded, False on error
    data: T | None             # Typed data (None on error)
    error: MRRResponseError | None  # Error object (None on success)
    http_status: int | None    # HTTP status code of the response
    retry_count: int           # Number of retry attempts (0 if no retry occurred)
```

### MRRResponse Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Success flag: `True` on successful request, `False` on error |
| `data` | `T \| None` | Typed response data. Contains the result on success, `None` on error |
| `error` | `MRRResponseError \| None` | Error object. `None` on success, detailed information on error |
| `http_status` | `int \| None` | HTTP status code of the response (200, 401, 429, 500, etc.) |
| `retry_count` | `int` | Number of retry attempts performed (0 if the request succeeded on the first try) |

---

## MRRResponseError Structure

The error object contains detailed information about what went wrong:

```python
class MRRResponseError(BaseMRRModel):
    """Error details."""

    code: str                          # Error type (see below)
    message: str                       # Human-readable error description
    details: dict[str, Any] | None     # Additional error data
    http_status: int | None            # HTTP status code (if applicable)
```

### MRRResponseError Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Error type code: `"network_error"`, `"timeout"`, `"api_error"`, `"validation_error"` |
| `message` | `str` | Human-readable error description |
| `details` | `dict[str, Any] \| None` | Additional data (e.g., exception details or validation errors) |
| `http_status` | `int \| None` | HTTP status code, if the error is related to an HTTP response |

---

## Error Types

The library defines 4 error types. Each type has a unique code in the `error.code` field.

### 1. Network Error (`"network_error"`)

**Description:** Network error — inability to establish a connection to the MRR server.

**Causes:**
- DNS error (host not found)
- Connection refused (server not responding)
- Proxy unavailable
- No internet connection

**Error Example:**
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

**Handling Example:**
```python
from aio_mrr import MRRClient

async def check_connection():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.whoami()

        if not response.success:
            if response.error and response.error.code == "network_error":
                print(f"Network error: {response.error.message}")
                print(f"   Attempts: {response.retry_count}")
                return

            print(f"Error: {response.error}")
            return

        print(f"Connection successful: {response.data}")
```

---

### 2. Timeout (`"timeout"`)

**Description:** The request exceeded the configured timeout.

**Causes:**
- Server not responding within the timeout period
- Slow internet connection
- MRR server overload

**Error Example:**
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

**Handling Example:**
```python
async def get_account():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_account()

        if not response.success:
            if response.error and response.error.code == "timeout":
                print(f"Request timeout: {response.error.message}")
                print(f"   Try increasing connect_timeout/read_timeout")
                return

            print(f"Error: {response.error}")
            return

        print(f"Account data: {response.data.username}")
```

---

### 3. API Error (`"api_error"`)

**Description:** Error returned by the MRR API (4xx, 5xx status codes).

**Causes:**
- Invalid API key (401)
- Insufficient permissions (403)
- Resource not found (404)
- Rate limiting — too many requests (429)
- MRR server error (500, 502, 503, 504)
- Invalid request parameters (400)

**Error Example:**
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

**Handling Example:**
```python
async def get_balance():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()

        if not response.success:
            if response.error and response.error.code == "api_error":
                status = response.error.http_status

                if status == 401:
                    print("Authentication error: check your API keys")
                elif status == 403:
                    print("Access denied: check API key permissions")
                elif status == 404:
                    print("Resource not found")
                elif status == 429:
                    print("Too many requests: wait and retry")
                elif status and status >= 500:
                    print(f"MRR server error (HTTP {status}): try again later")
                else:
                    print(f"API error (HTTP {status}): {response.error.message}")
                return

            print(f"Error: {response.error}")
            return

        print(f"Balance: {response.data}")
```

---

### 4. Validation Error (`"validation_error"`)

**Description:** Pydantic validation error when parsing the API response.

**Causes:**
- API returned an unexpected data format
- Missing required fields
- Data type mismatch

**Error Example:**
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

**Handling Example:**
```python
async def get_rigs():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.rig.get_mining_rigs(type="gpu")

        if not response.success:
            if response.error and response.error.code == "validation_error":
                print("Validation error: API returned unexpected data format")
                print(f"   {response.error.message}")
                print("   The MRR API may have changed its response format")
                return

            print(f"Error: {response.error}")
            return

        print(f"Rigs found: {len(response.data)}")
```

---

## Result Handling Pattern

The recommended pattern for handling responses in all examples:

```python
from aio_mrr import MRRClient

async def main():
    async with MRRClient(api_key="...", api_secret="...") as client:
        # 1. Call the method
        response = await client.account.get_balance()

        # 2. Check success
        if not response.success:
            # 3. Handle error
            print(f"Error: {response.error}")
            return

        # 4. Work with data
        print(f"Balance: {response.data}")
```

### Universal Error Handler

```python
from aio_mrr import MRRClient, MRRResponse

def handle_error(response: MRRResponse) -> bool:
    """
    Universal error handler.
    Returns True if the error was handled, False if it should be propagated.
    """
    if response.success:
        return True

    if response.error:
        error = response.error

        # Network errors
        if error.code == "network_error":
            print(f"Network: {error.message}")
            return True

        # Timeouts
        if error.code == "timeout":
            print(f"Timeout: {error.message}")
            return True

        # API errors
        if error.code == "api_error":
            status = error.http_status
            if status == 401:
                print("Invalid API key")
            elif status == 429:
                print(f"Rate limit (HTTP {status}): retry_count={response.retry_count}")
            elif status and status >= 500:
                print(f"MRR server (HTTP {status}): retry_count={response.retry_count}")
            else:
                print(f"API error (HTTP {status}): {error.message}")
            return True

        # Validation
        if error.code == "validation_error":
            print(f"Validation: {error.message}")
            return True

    # Unknown error
    print(f"Unknown error: {response.error}")
    return False

async def main():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()

        if not handle_error(response):
            return

        print(f"Balance: {response.data}")
```

---

## HTTP Client Retry Strategy

The library automatically retries requests on transient errors. The retry strategy depends on the error type:

### Retry Policy

| Error Type | Codes | Attempts | Backoff | Jitter |
|------------|-------|----------|---------|--------|
| Rate limit (429) | 429 | 5 | 5-60s (exponential) | Yes |
| Server errors | 500, 502, 503, 504 | 3 | 1-8s (exponential) | Yes |
| Connection errors | DNS, connection refused | 3 | 1-8s (exponential) | Yes |
| Timeout | aiohttp.ServerTimeoutError | 3 | 1-8s (exponential) | Yes |
| API errors (4xx) | 400, 401, 403, 404, etc. | 0 | — | — |

### Exponential Backoff + Jitter

**Exponential backoff:** The wait time increases exponentially between attempts.

**Jitter:** A random addition to the wait time to prevent "thundering herd" problems.

#### Example for 429 (Rate Limit):
```
Attempt 1: 0s (first request)
Attempt 2: ~5s  (5 + jitter)
Attempt 3: ~10s (10 + jitter)
Attempt 4: ~20s (20 + jitter)
Attempt 5: ~40s (40 + jitter)
Attempt 6: ~60s (60 + jitter) — max. time
```

#### Example for 500/Connection errors:
```
Attempt 1: 0s (first request)
Attempt 2: ~1s  (1 + jitter)
Attempt 3: ~2s  (2 + jitter)
Attempt 4: ~4s  (4 + jitter)
Attempt 5: ~8s  (8 + jitter) — max. time
```

### Checking Retries in the Response

```python
async def check_retry():
    async with MRRClient(api_key="...", api_secret="...") as client:
        response = await client.account.get_balance()

        if not response.success:
            if response.error and response.error.code == "api_error":
                status = response.error.http_status

                if status == 429:
                    print(f"Rate limit! {response.retry_count} retry attempts were made")
                    print(f"   Wait and retry the request later")
                elif status and status >= 500:
                    print(f"Server error (HTTP {status})")
                    print(f"   Retry attempts: {response.retry_count}")
                    if response.retry_count >= 3:
                        print(f"   Maximum attempts reached — wait and retry later")
```

---

## Code Examples

### Complete Example Handling All Error Types

This example demonstrates:
- Handling `network_error`
- Handling `timeout`
- Handling `api_error` (401, 429, 500)
- Handling `validation_error`
- Checking `retry_count` on retry attempts

---

## Links

- [« Back to Home](./index.md)

- [Authentication](./authentication.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

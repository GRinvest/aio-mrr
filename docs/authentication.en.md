# Client Authentication and Initialization

## Obtaining API Keys

To use the `aio-mrr` library, you need API keys from a MiningRigRentals account.

### Where to Find API Keys

1. Log in to your account on [MiningRigRentals.com](https://www.miningrigrentals.com)
2. Navigate to **Dashboard** → **API Keys** (in the top menu)
3. Click **Create New API Key**
4. Set a name for the key (e.g., "aio-mrr integration")
5. Copy and save:
   - **API Key** (public identifier)
   - **API Secret** (secret key — shown only once!)

> !!! warning "Security"
> Never share your API Secret or upload it to public repositories.

---

## Initializing MRRClient

The `MRRClient` class is the main entry point for working with the API.

### Constructor Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `api_key` | `str` | **Yes** | Public API key from your MRR account |
| `api_secret` | `str` | **Yes** | Secret API key from your MRR account |
| `connect_timeout` | `float` | No | Connection timeout (default: `30.0` seconds) |
| `read_timeout` | `float` | No | Response read timeout (default: `60.0` seconds) |
| `max_retries` | `int` | No | Maximum number of retry attempts on network errors (default: `3`) |

### Context Manager Example (Recommended)

The context manager automatically manages the client lifecycle — opening and closing the connection.

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    # Load keys from environment variables (NEVER hardcode!)
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API keys not found. Set MRR_API_KEY and MRR_API_SECRET environment variables")

    # Using context manager
    async with MRRClient(
        api_key=api_key,
        api_secret=api_secret,
        connect_timeout=30.0,
        read_timeout=60.0,
        max_retries=3
    ) as client:
        # All requests are made inside this block
        response = await client.whoami()
        if response.success:
            print(f"Successfully authenticated: {response.data}")
        else:
            print(f"Error: {response.error}")

asyncio.run(main())
```

### Example Without Context Manager

If you need more control over the client lifecycle:

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API keys not found")

    # Manual client creation
    client = MRRClient(
        api_key=api_key,
        api_secret=api_secret
    )

    try:
        # Making requests
        response = await client.whoami()
        if response.success:
            print(f"User: {response.data}")
    finally:
        # IMPORTANT: always close the client manually
        await client.close()

asyncio.run(main())
```

---

## HMAC-SHA1 Authentication

The library uses HMAC-SHA1 for request signing. This ensures data integrity and authenticity.

### How It Works

For each API request, the library automatically generates the following headers:

| Header | Description | Example |
|--------|-------------|---------|
| `x-api-key` | Public API key | `x-api-key: "abc123..."` |
| `x-api-nonce` | Unique request number (timestamp + random value) | `x-api-nonce: "1712345678901_xyz"` |
| `x-api-sign` | HMAC-SHA1 signature of the request body | `x-api-sign: "sha1=..."` |

### Signing Process

1. A **nonce** is generated (unique request identifier)
2. A signing string is formed: `method + path + nonce + body`
3. An **HMAC-SHA1** hash is computed using `api_secret`
4. The signature is added to the `x-api-sign` header

> !!! note
> You don't need to manually sign requests — the library does this automatically.

---

## The `whoami()` Method

The `whoami()` method is the basic way to verify authentication.

### Signature

```python
async def whoami() -> MRRResponse[dict[str, str]]
```

### Return Value

On successful authentication, the method returns a dictionary with account information:

```python
{
    "username": "your_username",
    "user_id": "12345"
}
```

### Usage Example

```python
response = await client.whoami()

if response.success:
    username = response.data["username"]
    print(f"Welcome, {username}!")
else:
    print(f"Authentication error: {response.error.message}")
```

---

## Security

### ⚠️ Never Hardcode API Keys

**WRONG:**
```python
# ❌ NEVER do this!
client = MRRClient(
    api_key="your_real_api_key",
    api_secret="your_real_api_secret"
)
```

**RIGHT:**
```python
# ✅ Use environment variables
import os

api_key = os.environ.get("MRR_API_KEY")
api_secret = os.environ.get("MRR_API_SECRET")

client = MRRClient(
    api_key=api_key,
    api_secret=api_secret
)
```

### Setting Up Environment Variables

#### Linux / macOS:
```bash
export MRR_API_KEY="your_api_key_here"
export MRR_API_SECRET="your_api_secret_here"
```

#### Windows (PowerShell):
```powershell
$env:MRR_API_KEY="your_api_key_here"
$env:MRR_API_SECRET="your_api_secret_here"
```

#### Windows (CMD):
```cmd
set MRR_API_KEY=your_api_key_here
set MRR_API_SECRET=your_api_secret_here
```

> !!! tip "Tip"
> Add `.env` to `.gitignore` if you use a local environment variables file for testing.

---

## See Also

- [Quick Start Example](../examples/01_quickstart.py) — basic initialization and first request
- [Error Handling](./error-handling.md) — how to handle API errors
- [Home Page](./index.md) — documentation table of contents

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

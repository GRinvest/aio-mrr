# aio-mrr Documentation

Asynchronous library for working with MiningRigRentals API v2.

## Description

`aio-mrr` is a modern async client for integration with MiningRigRentals API v2. The library provides a typed interface to all 56 public API methods, leveraging modern Python 3.12+ features.

A key feature of the library is the complete absence of exceptions: all responses are wrapped in the universal `MRRResponse[T]` type, which simplifies error handling and makes code more predictable.

## Key Features

- **async/await** — fully asynchronous API powered by `aiohttp`
- **Pydantic v2** — strict typing of all responses via Pydantic models
- **Retry strategy** — automatic retries on network errors and rate limiting (via `tenacity`)
- **HMAC-SHA1 authentication** — secure request signing with secret masking
- **Connection pooling** — efficient connection management for high-load scenarios
- **Result pattern** — Result pattern instead of exceptions for error handling

## Requirements

- **Python**: 3.12+
- **Dependencies**:
  - `aiohttp>=3.13.0` — async HTTP client
  - `pydantic>=2.12.0` — data validation and typing
  - `tenacity>=9.1.0` — retry strategy
  - `loguru>=0.7.0` — logging

## Installation

### Stable Release

```bash
pip install aio-mrr
```

### Development

For development and testing, install the package in editable mode with additional dependencies:

```bash
pip install -e ".[dev]"
```

---

## Quick Start

!!! tip "Quick Start"

    Minimal example of client initialization and making a request:

    ```python
    import os
    import asyncio
    from aio_mrr import MRRClient

    async def main():
        # Load keys from environment variables
        api_key = os.environ.get("MRR_API_KEY")
        api_secret = os.environ.get("MRR_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("MRR_API_KEY and MRR_API_SECRET must be set")

        # Initialize client with context manager
        async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
            # Check authentication
            response = await client.whoami()
            if not response.success:
                print(f"Authentication error: {response.error}")
                return

            print(f"Logged in as: {response.data}")

            # Get balance
            balance = await client.account.get_balance()
            if balance.success:
                print(f"Balance: {balance.data}")

    asyncio.run(main())
    ```

    See also: [`examples/01_quickstart.py`](examples/01_quickstart.py)

---

## Table of Contents

### Getting Started

- **[Installation and Authentication](authentication.md)** — obtaining API keys, client initialization, HMAC-SHA1 authentication
- **[Error Handling](error-handling.md)** — Result pattern, error types, retry strategy
- **[Data Models](models.md)** — complete description of all library Pydantic models

### API Reference

- **[Account and Profiles](api-reference/account.md)** — 16 methods for managing account, pools, and profiles
- **[Rigs](api-reference/rigs.md)** — 15 methods for rig management (CRUD, search, graphs)
- **[Rentals](api-reference/rentals.md)** — 12 methods for rental management (create, extend, logs)
- **[Rig Groups](api-reference/rig-groups.md)** — 7 methods for rig group management
- **[Info](api-reference/info.md)** — 4 methods for obtaining server and algorithm information
- **[Pricing](api-reference/pricing.md)** — 1 method for obtaining conversion rates and market prices

---

## Examples

The repository includes 10 ready-to-use examples for various usage scenarios:

| File | Description |
| --- | --- |
| [`examples/01_quickstart.py`](examples/01_quickstart.py) | Basic initialization, whoami, balance |
| [`examples/02_account_balance.py`](examples/02_account_balance.py) | Profile, balance, transactions |
| [`examples/03_manage_rigs.py`](examples/03_manage_rigs.py) | Fetching, creating, deleting rigs |
| [`examples/04_create_rental.py`](examples/04_create_rental.py) | Creating a rental, extending, logs |
| [`examples/05_rig_groups.py`](examples/05_rig_groups.py) | Rig group CRUD, adding/removing |
| [`examples/06_info_and_pricing.py`](examples/06_info_and_pricing.py) | Servers, algorithms, rates, prices |
| [`examples/07_error_handling_demo.py`](examples/07_error_handling_demo.py) | Demonstration of all error types |
| [`examples/08_advanced_search.py`](examples/08_advanced_search.py) | Rig search with filters |
| [`examples/09_pool_management.py`](examples/09_pool_management.py) | Pool CRUD, pool testing |
| [`examples/10_profile_management.py`](examples/10_profile_management.py) | Profile CRUD, priorities |

!!! note "Note"

    All examples use environment variables to store API keys. Never store keys in code!

    ```bash
    export MRR_API_KEY="your_api_key"
    export MRR_API_SECRET="your_api_secret"
    ```

---

## Security

- **DO NOT store API keys in code** — always use environment variables
- The library automatically masks secrets in logs via `SecretMasker`
- Check for keys before running: `if not api_key: raise ValueError(...)`

---

## Links

- Source code: [GitHub](https://github.com/GRinvest/aio-mrr)
- Examples repository: [examples/](https://github.com/GRinvest/aio-mrr/tree/main/examples/)
- MiningRigRentals API: [https://miningrigrentals.com](https://miningrigrentals.com)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

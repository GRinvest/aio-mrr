# aio-mrr

**Async Library for MiningRigRentals API v2**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black)](https://github.com/astral-sh/ruff)

## Overview

`aio-mrr` is an asynchronous Python client for the [MiningRigRentals API v2](https://miningrigrentals.com/), built on `aiohttp` and `pydantic`. The library provides a typed interface to all API methods with automatic error handling, retry logic, and HMAC-SHA1 authentication.

## Features

- **async/await** — fully asynchronous API
- **Pydantic models** — automatic validation and typed responses
- **Retry logic** — automatic retries on network errors
- **HMAC-SHA1 authentication** — secure API communication
- **Connection pooling** — efficient connection management
- **Secret masking** — API key protection in logs

## Installation

```bash
pip install aio-mrr
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
import asyncio
import os
from aio_mrr import MRRClient

async def main():
    api_key = os.environ.get("MRR_API_KEY")
    api_secret = os.environ.get("MRR_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("MRR_API_KEY and MRR_API_SECRET must be set")

    async with MRRClient(api_key, api_secret) as client:
        # Check authentication
        response = await client.whoami()
        if response.success:
            print(f"Logged in as: {response.data['username']}")

        # Get balance
        balance = await client.account.get_balance()
        if balance.success:
            print(f"Balance: {balance.data}")

asyncio.run(main())
```

## Documentation

Full documentation is available on [GitHub Pages](https://GRinvest.github.io/aio-mrr/):

- [Setup & Authentication](https://GRinvest.github.io/aio-mrr/authentication/)
- [Error Handling](https://GRinvest.github.io/aio-mrr/error-handling/)
- [Data Models](https://GRinvest.github.io/aio-mrr/models/)
- [API Reference](https://GRinvest.github.io/aio-mrr/api-reference/account/)

## Examples

Usage examples are available in the [`examples/`](examples/) directory:

- [`01_quickstart.py`](examples/01_quickstart.py) — basic initialization and simple request
- [`02_account_balance.py`](examples/02_account_balance.py) — account operations
- [`03_manage_rigs.py`](examples/03_manage_rigs.py) — rig management
- [`04_create_rental.py`](examples/04_create_rental.py) — rental creation
- [`05_rig_groups.py`](examples/05_rig_groups.py) — rig group management
- [`06_info_and_pricing.py`](examples/06_info_and_pricing.py) — info and pricing
- [`07_error_handling_demo.py`](examples/07_error_handling_demo.py) — error handling
- [`08_advanced_search.py`](examples/08_advanced_search.py) — advanced search
- [`09_pool_management.py`](examples/09_pool_management.py) — pool management
- [`10_profile_management.py`](examples/10_profile_management.py) — profile management

## Requirements

- Python 3.12+
- aiohttp >= 3.13.0
- pydantic >= 2.12.0
- tenacity >= 9.1.0
- loguru >= 0.7.0

## API Coverage

The library covers all 55 public methods of the MiningRigRentals API v2:

| Subclient | Methods | Description |
|-----------|---------|-------------|
| Client | 1 | Authentication check |
| AccountClient | 16 | Account, balance, pools, profiles |
| InfoClient | 4 | Servers, algorithms, currencies |
| PricingClient | 1 | Conversion rates and prices |
| RigClient | 15 | Rig management |
| RentalClient | 12 | Rental management |
| RigGroupClient | 7 | Rig groups |

## Contributing

Pull requests are welcome! Please open an issue to discuss changes before submitting a PR.

## License

[MIT License](LICENSE.md)

---

<hr />
<p align="center">
  <i>aio-mrr is <a href="https://github.com/GRinvest/aio-mrr/blob/main/LICENSE.md">MIT licensed</a> code.</i><br/>
  <i>Designed & built in Novosibirsk, Russia by <a href="https://sibneuro.tech">SibNeuroTech</a></i><br/>
  <i>Contact: <a href="https://t.me/GRinvest">@GRinvest</a></i>
</p>

"""aio-mrr — Async library for MiningRigRentals API v2.

This package provides a complete async interface to MRR API v2 with:
- Typing via Pydantic models
- Error handling via MRRResponse[T]
- Automatic retry and timeout
- HMAC SHA1 authentication

Author: GRinvest / SibNeuroTech
Website: https://sibneuro.tech
Contact: @GRinvest (Telegram)
License: MIT

Usage example:
    from aio_mrr import MRRClient

    async def main():
        async with MRRClient(
            api_key="YOUR_KEY",
            api_secret="YOUR_SECRET"
        ) as client:
            response = await client.account.get_balance()
            if response.success:
                print(response.data)

Attributes:
    __version__: Package version in "major.minor.patch" format
"""

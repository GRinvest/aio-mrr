"""Models for Account API.

This module contains models for /account/* endpoints:
- GET /account
- GET /account/balance
- GET /account/transactions
- GET /account/profile
- PUT /account/profile
- GET /account/profile/{id}
- PUT /account/profile/{id}
- PUT /account/profile/{id}/{priority}
- DELETE /account/profile/{id}
- GET /account/pool
- GET /account/pool/{ids}
- PUT /account/pool
- PUT /account/pool/{ids}
- DELETE /account/pool/{ids}
- PUT /account/pool/test
- GET /account/currencies

> Note: PUT /account/balance (withdrawal) — endpoint is disabled on the MRR side.
  NOT implemented.
"""

from aio_mrr.models.account.request import (
    PoolCreateBody,
    PoolTestBody,
    ProfileCreateBody,
    TransactionsQueryParams,
)
from aio_mrr.models.account.response import (
    AccountInfo,
    AlgoPoolInfo,
    AlgoProfileInfo,
    BalanceInfo,
    CurrencyStatus,
    DepositCurrencyInfo,
    NotificationsInfo,
    Pool,
    PoolCreateResponse,
    PoolProfileInfo,
    PoolTestResult,
    PoolTestResultItem,
    PriceInfo,
    Profile,
    ProfileCreateResponse,
    ProfileDeleteResponse,
    SettingsInfo,
    Transaction,
    TransactionsList,
    WithdrawCurrencyInfo,
)

__all__ = [
    "AccountInfo",
    "AlgoPoolInfo",
    "AlgoProfileInfo",
    "BalanceInfo",
    "CurrencyStatus",
    "DepositCurrencyInfo",
    "NotificationsInfo",
    "Pool",
    "PoolCreateBody",
    "PoolCreateResponse",
    "PoolProfileInfo",
    "PoolTestBody",
    "PoolTestResult",
    "PoolTestResultItem",
    "PriceInfo",
    "Profile",
    "ProfileCreateBody",
    "ProfileCreateResponse",
    "ProfileDeleteResponse",
    "SettingsInfo",
    "Transaction",
    "TransactionsList",
    "TransactionsQueryParams",
    "WithdrawCurrencyInfo",
]

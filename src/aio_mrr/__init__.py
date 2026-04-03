"""aio-mrr — Асинхронная библиотека для MiningRigRentals API v2.

Этот пакет предоставляет полный асинхронный интерфейс к API MRR v2 с:
- Типизацией через Pydantic модели
- Обработкой ошибок через MRRResponse[T]
- Автоматическим retry и timeout
- HMAC SHA1 аутентификацией

Автор: GRinvest / SibNeuroTech
Сайт: https://sibneuro.tech
Контакт: @GRinvest (Telegram)
Лицензия: MIT

Пример использования:
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
    __version__: Версия пакета в формате "major.minor.patch"
"""

from aio_mrr._version import __version__
from aio_mrr.client import MRRClient
from aio_mrr.exceptions import (
    MRRAPIError,
    MRRBaseError,
    MRRNetworkError,
    MRRTimeoutError,
    MRRValidationError,
)
from aio_mrr.models import (
    AccountInfo,
    AlgoInfo,
    AlgoPoolInfo,
    AlgoProfileInfo,
    BalanceInfo,
    BaseMRRModel,
    ConversionRates,
    CurrencyInfo,
    CurrencyStatus,
    DepositCurrencyInfo,
    GraphData,
    HashInfo,
    InfoAlgosQueryParams,
    MRRResponse,
    MRRResponseError,
    MarketRates,
    NotificationsInfo,
    Pool,
    PoolCreateBody,
    PoolCreateResponse,
    PoolInfo,
    PoolProfileInfo,
    PoolTestBody,
    PoolTestResult,
    PoolTestResultItem,
    PriceInfo,
    PricingInfo,
    Profile,
    ProfileCreateBody,
    ProfileCreateResponse,
    ProfileDeleteResponse,
    RentalCreateBody,
    RentalExtendBody,
    RentalInfo,
    RentalList,
    RentalListQueryParams,
    RentalLogEntry,
    RentalMessage,
    RentalPoolBody,
    RigBatchBody,
    RigCreateBody,
    RigExtendBody,
    RigGraphData,
    RigGraphDataPoint,
    RigGroupCreateBody,
    RigGroupInfo,
    RigGroupList,
    RigGroupUpdateBody,
    RigHashInfo,
    RigInfo,
    RigList,
    RigPoolBody,
    RigPortInfo,
    RigPriceInfo,
    RigSearchParams,
    RigThreadInfo,
    ServerInfo,
    ServersList,
    SettingsInfo,
    Transaction,
    TransactionsList,
    TransactionsQueryParams,
    WithdrawCurrencyInfo,
)

__all__ = [
    # Account models
    "AccountInfo",
    # Info models
    "AlgoInfo",
    "AlgoPoolInfo",
    "AlgoProfileInfo",
    "BalanceInfo",
    "BaseMRRModel",
    "ConversionRates",
    "CurrencyInfo",
    "CurrencyStatus",
    "DepositCurrencyInfo",
    "GraphData",
    "HashInfo",
    "InfoAlgosQueryParams",
    "MRRAPIError",
    # Исключения
    "MRRBaseError",
    "MRRClient",
    "MRRNetworkError",
    "MRRResponse",
    "MRRResponseError",
    "MRRTimeoutError",
    "MRRValidationError",
    "MarketRates",
    "NotificationsInfo",
    "Pool",
    "PoolCreateBody",
    "PoolCreateResponse",
    "PoolInfo",
    "PoolProfileInfo",
    "PoolTestBody",
    "PoolTestResult",
    "PoolTestResultItem",
    "PriceInfo",
    # Pricing models
    "PricingInfo",
    "Profile",
    "ProfileCreateBody",
    "ProfileCreateResponse",
    "ProfileDeleteResponse",
    "RentalCreateBody",
    "RentalExtendBody",
    # Rental models
    "RentalInfo",
    "RentalList",
    "RentalListQueryParams",
    "RentalLogEntry",
    "RentalMessage",
    "RentalPoolBody",
    "RigBatchBody",
    "RigCreateBody",
    "RigExtendBody",
    "RigGraphData",
    "RigGraphDataPoint",
    "RigGroupCreateBody",
    # RigGroup models
    "RigGroupInfo",
    "RigGroupList",
    "RigGroupUpdateBody",
    "RigHashInfo",
    # Rig models
    "RigInfo",
    "RigList",
    "RigPoolBody",
    "RigPortInfo",
    "RigPriceInfo",
    "RigSearchParams",
    "RigThreadInfo",
    "ServerInfo",
    "ServersList",
    "SettingsInfo",
    "Transaction",
    "TransactionsList",
    "TransactionsQueryParams",
    "WithdrawCurrencyInfo",
    "__version__",
]

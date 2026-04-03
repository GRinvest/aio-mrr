"""Модели для Rig API.

Этот пакет содержит Pydantic-модели для валидации request/response данных Rig API.
"""

from aio_mrr.models.rig.request import (
    RigBatchBody,
    RigCreateBody,
    RigExtendBody,
    RigPoolBody,
    RigSearchParams,
)
from aio_mrr.models.rig.response import (
    RigGraphData,
    RigGraphDataPoint,
    RigHashInfo,
    RigInfo,
    RigList,
    RigPortInfo,
    RigPriceInfo,
    RigThreadInfo,
)

__all__ = [
    "RigBatchBody",
    "RigCreateBody",
    "RigExtendBody",
    "RigGraphData",
    "RigGraphDataPoint",
    "RigHashInfo",
    "RigInfo",
    "RigList",
    "RigPoolBody",
    "RigPortInfo",
    "RigPriceInfo",
    "RigSearchParams",
    "RigThreadInfo",
]

"""Models for Rig API.

This package contains Pydantic models for validating request/response data of the Rig API.
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
    RigHashInfo,
    RigInfo,
    RigList,
    RigPortInfo,
    RigPriceInfo,
    RigThreadDetail,
    RigThreadInfo,
)

__all__ = [
    "RigBatchBody",
    "RigCreateBody",
    "RigExtendBody",
    "RigGraphData",
    "RigHashInfo",
    "RigInfo",
    "RigList",
    "RigPoolBody",
    "RigPortInfo",
    "RigPriceInfo",
    "RigSearchParams",
    "RigThreadDetail",
    "RigThreadInfo",
]

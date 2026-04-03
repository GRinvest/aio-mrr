"""Models for RigGroup API.

This package contains Pydantic models for validating request/response data
for RigGroup API endpoints (/riggroup/*).
"""

from aio_mrr.models.riggroup.request import RigGroupCreateBody, RigGroupUpdateBody
from aio_mrr.models.riggroup.response import RigGroupInfo, RigGroupList

__all__ = [
    "RigGroupCreateBody",
    "RigGroupInfo",
    "RigGroupList",
    "RigGroupUpdateBody",
]

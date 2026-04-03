"""Модели для RigGroup API.

Этот пакет содержит Pydantic-модели для валидации request/response данных
для эндпоинтов RigGroup API (/riggroup/*).
"""

from aio_mrr.models.riggroup.request import RigGroupCreateBody, RigGroupUpdateBody
from aio_mrr.models.riggroup.response import RigGroupInfo, RigGroupList

__all__ = [
    "RigGroupCreateBody",
    "RigGroupInfo",
    "RigGroupList",
    "RigGroupUpdateBody",
]

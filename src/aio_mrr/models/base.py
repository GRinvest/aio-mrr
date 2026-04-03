"""Базовые Pydantic-модели для библиотеки aio-mrr.

Этот модуль содержит:
- Базовый класс BaseModel с extra='ignore' для устойчивости к изменениям API MRR.
- MRRResponseError - модель для деталей ошибки.
- MRRResponse - универсальный generic Result-объект для ответов API.

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
"""

from __future__ import annotations
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseMRRModel(BaseModel):
    """Базовая модель для всех моделей aio-mrr.

    Использует extra='ignore' для устойчивости к изменениям API MRR (BETA).
    Все модели наследуются от этого класса.
    """

    model_config = ConfigDict(extra="ignore")


class MRRResponseError(BaseMRRModel):
    """Детали ошибки в ответе API.

    Attributes:
        code: Код ошибки (например, "network_error", "api_error",
              "validation_error", "timeout").
        message: Человекочитаемое описание ошибки.
        details: Дополнительные данные об ошибке (опционально).
        http_status: HTTP статус код если применимо (опционально).
    """

    code: str
    message: str
    details: dict[str, Any] | None = None
    http_status: int | None = None


class MRRResponse(BaseMRRModel, Generic[T]):
    """Универсальный ответ библиотеки aio-mrr.

    Обертка над ответами API MiningRigRentals с поддержкой типизации.

    Attributes:
        success: Флаг успешности запроса.
        data: Данные ответа (опционально, зависит от успешности).
        error: Детали ошибки при failure (опционально).
        http_status: HTTP статус код ответа (опционально).
        retry_count: Количество попыток retry (по умолчанию 0).
    """

    success: bool
    data: T | None = None
    error: MRRResponseError | None = None
    http_status: int | None = None
    retry_count: int = 0

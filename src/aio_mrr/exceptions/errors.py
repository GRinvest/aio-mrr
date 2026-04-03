"""Иерархия исключений для библиотеки aio-mrr.

Эти исключения предназначены для внутреннего использования и для опционального
try/except в родительском приложении. Все ошибки в библиотеке возвращаются
как MRRResponse(success=False, error=...), но исключения могут быть полезны
для отладки и специфичной обработки.
"""

from typing import Any


class MRRBaseError(Exception):
    """Базовый класс для всех исключений aio-mrr."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """
        Args:
            message: Человекочитаемое описание ошибки.
            details: Дополнительные данные об ошибке.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class MRRNetworkError(MRRBaseError):
    """Исключение для сетевых ошибок (aiohttp, connection errors)."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        """
        Args:
            message: Человекочитаемое описание ошибки.
            details: Дополнительные данные об ошибке.
            host: Хост, к которому не удалось подключиться.
            port: Порт, к которому не удалось подключиться.
        """
        error_details = details or {}
        if host is not None:
            error_details["host"] = host
        if port is not None:
            error_details["port"] = port
        super().__init__(message, error_details)


class MRRAPIError(MRRBaseError):
    """Исключение для ошибок API MRR (HTTP status >= 400)."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        http_status: int | None = None,
        error_code: str | None = None,
    ) -> None:
        """
        Args:
            message: Человекочитаемое описание ошибки.
            details: Дополнительные данные об ошибке.
            http_status: HTTP статус код ответа.
            error_code: Код ошибки от API.
        """
        error_details = details or {}
        if http_status is not None:
            error_details["http_status"] = http_status
        if error_code is not None:
            error_details["error_code"] = error_code
        super().__init__(message, error_details)
        self.http_status = http_status
        self.error_code = error_code


class MRRValidationError(MRRBaseError):
    """Исключение для ошибок валидации Pydantic."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        model_name: str | None = None,
        field: str | None = None,
    ) -> None:
        """
        Args:
            message: Человекочитаемое описание ошибки.
            details: Дополнительные данные об ошибке.
            model_name: Название модели Pydantic.
            field: Поле, которое не прошло валидацию.
        """
        error_details = details or {}
        if model_name is not None:
            error_details["model_name"] = model_name
        if field is not None:
            error_details["field"] = field
        super().__init__(message, error_details)
        self.model_name = model_name
        self.field = field


class MRRTimeoutError(MRRNetworkError):
    """Исключение для ошибок таймаута."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        timeout_type: str | None = None,
        timeout_value: float | None = None,
    ) -> None:
        """
        Args:
            message: Человекочитаемое описание ошибки.
            details: Дополнительные данные об ошибке.
            timeout_type: Тип таймаута ('connect' или 'read').
            timeout_value: Значение таймаута в секундах.
        """
        error_details = details or {}
        if timeout_type is not None:
            error_details["timeout_type"] = timeout_type
        if timeout_value is not None:
            error_details["timeout_value"] = timeout_value
        super().__init__(message, error_details)
        self.timeout_type = timeout_type
        self.timeout_value = timeout_value

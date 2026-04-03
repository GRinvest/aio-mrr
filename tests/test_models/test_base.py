"""Тесты для базовых моделей (BaseMRRModel, MRRResponse)."""

from __future__ import annotations
from pydantic import ValidationError
import pytest

from aio_mrr.models.base import BaseMRRModel, MRRResponse, MRRResponseError


class TestBaseMRRModel:
    """Тесты для базовой модели BaseMRRModel."""

    def test_extra_fields_ignored(self) -> None:
        """Тестирует, что лишние поля игнорируются."""

        class TestModel(BaseMRRModel):
            """Тестовая модель."""

            name: str
            value: int

        # Должно работать без ошибок
        data = {"name": "test", "value": 42, "extra_field": "ignored"}
        model = TestModel.model_validate(data)
        assert model.name == "test"
        assert model.value == 42
        assert "extra_field" not in model.model_dump()

    def test_required_fields_validation(self) -> None:
        """Тестирует валидацию обязательных полей."""

        class TestModel(BaseMRRModel):
            """Тестовая модель."""

            name: str
            value: int

        # Должно выбросить ошибку для отсутствующих обязательных полей
        with pytest.raises(ValidationError):
            TestModel(name="test")  # type: ignore

        with pytest.raises(ValidationError):
            TestModel(value=42)  # type: ignore

    def test_model_dump(self) -> None:
        """Тестирует сериализацию модели."""

        class TestModel(BaseMRRModel):
            """Тестовая модель."""

            name: str
            value: int

        model = TestModel(name="test", value=42)
        data = model.model_dump()

        assert data == {"name": "test", "value": 42}

    def test_model_dump_json(self) -> None:
        """Тестирует JSON сериализацию модели."""

        class TestModel(BaseMRRModel):
            """Тестовая модель."""

            name: str
            value: int

        model = TestModel(name="test", value=42)
        json_str = model.model_dump_json()

        assert '"name":"test"' in json_str
        assert '"value":42' in json_str

    def test_model_from_dict(self) -> None:
        """Тестирует создание модели из словаря."""

        class TestModel(BaseMRRModel):
            """Тестовая модель."""

            name: str
            value: int

        data = {"name": "test", "value": 42}
        model = TestModel.model_validate(data)

        assert model.name == "test"
        assert model.value == 42


class TestMRRResponseError:
    """Тесты для модели MRRResponseError."""

    def test_minimal_error(self) -> None:
        """Тестирует минимальную ошибку с обязательными полями."""
        error = MRRResponseError(code="api_error", message="Test error")

        assert error.code == "api_error"
        assert error.message == "Test error"
        assert error.details is None
        assert error.http_status is None

    def test_full_error(self) -> None:
        """Тестирует полную ошибку со всеми полями."""
        error = MRRResponseError(
            code="network_error",
            message="Connection failed",
            details={"host": "example.com", "port": 443},
            http_status=503,
        )

        assert error.code == "network_error"
        assert error.message == "Connection failed"
        assert error.details == {"host": "example.com", "port": 443}
        assert error.http_status == 503

    def test_error_from_api_response(self) -> None:
        """Тестирует создание ошибки из ответа API."""
        api_error_data = {
            "code": "validation_error",
            "message": "Invalid rig ID",
            "details": {"field": "rig_id", "reason": "not found"},
            "http_status": 404,
        }

        error = MRRResponseError.model_validate(api_error_data)

        assert error.code == "validation_error"
        assert error.message == "Invalid rig ID"
        assert error.details == {"field": "rig_id", "reason": "not found"}
        assert error.http_status == 404


class TestMRRResponse:
    """Тесты для модели MRRResponse."""

    def test_successful_response(self) -> None:
        """Тестирует успешный ответ."""
        response = MRRResponse[str](success=True, data="test_data")

        assert response.success is True
        assert response.data == "test_data"
        assert response.error is None
        assert response.http_status is None
        assert response.retry_count == 0

    def test_failed_response(self) -> None:
        """Тестирует ответ с ошибкой."""
        error = MRRResponseError(code="api_error", message="API error")
        response = MRRResponse[str](
            success=False,
            data=None,
            error=error,
            http_status=401,
            retry_count=0,
        )

        assert response.success is False
        assert response.data is None
        assert response.error is not None
        assert response.error.code == "api_error"
        assert response.error.message == "API error"
        assert response.http_status == 401

    def test_response_with_retry_count(self) -> None:
        """Тестирует ответ с retry count."""
        response = MRRResponse[str](
            success=True,
            data="data",
            retry_count=3,
        )

        assert response.retry_count == 3

    def test_response_from_api_success(self) -> None:
        """Тестирует парсинг успешного ответа API."""
        api_data = {
            "success": True,
            "data": {"confirmed": "0.1", "pending": 0, "unconfirmed": "0.0"},
        }

        # Используем Dict[str, object] как тип
        response = MRRResponse[dict[str, object]].model_validate(api_data)

        assert response.success is True
        assert response.data is not None
        assert response.data["confirmed"] == "0.1"

    def test_response_from_api_error(self) -> None:
        """Тестирует парсинг ответа API с ошибкой."""
        api_data = {
            "success": False,
            "data": None,
            "error": {
                "code": "api_error",
                "message": "Invalid signature",
                "http_status": 401,
            },
            "http_status": 401,
            "retry_count": 0,
        }

        response = MRRResponse[object].model_validate(api_data)

        assert response.success is False
        assert response.data is None
        assert response.error is not None
        assert response.error.code == "api_error"
        assert response.http_status == 401

    def test_response_with_http_status(self) -> None:
        """Тестирует ответ с HTTP статусом."""
        response = MRRResponse[str](
            success=True,
            data="data",
            http_status=200,
        )

        assert response.http_status == 200

    def test_generic_type_preservation(self) -> None:
        """Тестирует сохранение типа данных."""
        response = MRRResponse[int](success=True, data=42)

        assert response.data == 42
        assert isinstance(response.data, int)

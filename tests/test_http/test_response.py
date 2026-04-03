"""Tests for response parsing in http module."""

from __future__ import annotations
from typing import Any

from aio_mrr.http.response import ResponseParser, parse_response
from aio_mrr.models.base import MRRResponse


class TestParseResponse:
    """Tests for parse_response function."""

    def test_successful_response_with_dict_data(self) -> None:
        """Test parsing successful response with dict data."""
        json_data = {"success": True, "data": {"balance": "0.1", "confirmed": "0.05"}}

        result = parse_response(json_data, http_status=200)

        assert result.success is True
        assert result.data == {"balance": "0.1", "confirmed": "0.05"}
        assert result.error is None
        assert result.http_status == 200
        assert result.retry_count == 0

    def test_successful_response_with_list_data(self) -> None:
        """Test parsing successful response with list data."""
        json_data = {"success": True, "data": [{"id": 1}, {"id": 2}]}

        result = parse_response(json_data, http_status=200)

        assert result.success is True
        assert result.data == [{"id": 1}, {"id": 2}]
        assert result.error is None

    def test_successful_response_with_none_data(self) -> None:
        """Test parsing successful response with None data."""
        json_data = {"success": True, "data": None}

        result = parse_response(json_data, http_status=200)

        assert result.success is True
        assert result.data is None
        assert result.error is None

    def test_successful_response_with_string_data(self) -> None:
        """Test parsing successful response with string data."""
        json_data = {"success": True, "data": "some_string"}

        result = parse_response(json_data, http_status=200)

        assert result.success is True
        assert result.data == "some_string"
        assert result.error is None

    def test_successful_response_with_int_data(self) -> None:
        """Test parsing successful response with int data."""
        json_data = {"success": True, "data": 42}

        result = parse_response(json_data, http_status=200)

        assert result.success is True
        assert result.data == 42
        assert result.error is None

    def test_api_error_response_with_message(self) -> None:
        """Test parsing API error response with message."""
        json_data = {
            "success": False,
            "data": {"message": "Invalid API key or signature"},
        }

        result = parse_response(json_data, http_status=401)

        assert result.success is False
        assert result.data is None
        assert result.error is not None
        assert result.error.code == "api_error"
        assert "Invalid API key" in result.error.message
        assert result.http_status == 401

    def test_api_error_response_with_empty_data(self) -> None:
        """Test parsing API error response with empty data."""
        json_data = {"success": False, "data": {}}

        result = parse_response(json_data, http_status=200)

        assert result.success is False
        assert result.data is None
        assert result.error is not None
        assert result.error.code == "api_error"
        assert result.error.message == "Unknown API error"

    def test_api_error_response_with_none_data(self) -> None:
        """Test parsing API error response with None data."""
        json_data = {"success": False, "data": None}

        result = parse_response(json_data, http_status=200)

        assert result.success is False
        assert result.data is None
        assert result.error is not None
        assert result.error.code == "api_error"
        assert result.error.message == "Unknown API error"

    def test_api_error_response_with_string_data(self) -> None:
        """Test parsing API error response with string data (non-dict)."""
        json_data = {"success": False, "data": "error_string"}

        result = parse_response(json_data, http_status=200)

        assert result.success is False
        assert result.data is None
        assert result.error is not None
        assert result.error.code == "api_error"
        assert result.error.message == "Unknown API error"

    def test_api_error_response_with_details(self) -> None:
        """Test parsing API error response with additional details."""
        json_data = {
            "success": False,
            "data": {
                "message": "Validation failed",
                "field": "rig_id",
                "code": "invalid",
            },
        }

        result = parse_response(json_data, http_status=400)

        assert result.success is False
        assert result.error is not None
        assert result.error.code == "api_error"
        assert result.error.message == "Validation failed"
        assert result.error.details is not None
        assert result.error.details["field"] == "rig_id"

    def test_retry_count_in_response(self) -> None:
        """Test that retry_count is included in response."""
        json_data = {"success": True, "data": {"test": "value"}}

        result = parse_response(json_data, http_status=200, retry_count=3)

        assert result.success is True
        assert result.retry_count == 3

    def test_missing_success_field_defaults_to_false(self) -> None:
        """Test that missing success field defaults to False."""
        json_data = {"data": {"test": "value"}}

        result = parse_response(json_data, http_status=200)

        assert result.success is False
        assert result.error is not None


class TestResponseParser:
    """Tests for ResponseParser class."""

    def test_parser_init_with_defaults(self) -> None:
        """Test ResponseParser initialization with defaults."""
        parser: ResponseParser[Any] = ResponseParser()

        assert parser.http_status is None
        assert parser.retry_count == 0

    def test_parser_init_with_custom_values(self) -> None:
        """Test ResponseParser initialization with custom values."""
        parser: ResponseParser[Any] = ResponseParser(http_status=200, retry_count=5)

        assert parser.http_status == 200
        assert parser.retry_count == 5

    def test_parse_method(self) -> None:
        """Test parse method of ResponseParser."""
        parser: ResponseParser[Any] = ResponseParser(http_status=201, retry_count=2)
        json_data = {"success": True, "data": {"test": "value"}}

        result = parser.parse(json_data)

        assert result.success is True
        assert result.http_status == 201
        assert result.retry_count == 2

    def test_from_json_string_valid(self) -> None:
        """Test from_json_string with valid JSON."""
        json_string = '{"success": true, "data": {"balance": "0.1"}}'

        result = ResponseParser.from_json_string(json_string, http_status=200)

        assert result.success is True
        assert result.data == {"balance": "0.1"}
        assert result.http_status == 200

    def test_from_json_string_invalid(self) -> None:
        """Test from_json_string with invalid JSON."""
        json_string = "not valid json"

        result = ResponseParser.from_json_string(json_string, http_status=200)

        assert result.success is False
        assert result.error is not None
        assert result.error.code == "validation_error"
        assert "Invalid JSON" in result.error.message

    def test_from_json_string_empty_string(self) -> None:
        """Test from_json_string with empty string."""
        json_string = ""

        result = ResponseParser.from_json_string(json_string, http_status=200)

        assert result.success is False
        assert result.error is not None
        assert result.error.code == "validation_error"

    def test_from_json_string_array(self) -> None:
        """Test from_json_string with JSON array (expected object)."""
        json_string = '[{"id": 1}, {"id": 2}]'

        result = ResponseParser.from_json_string(json_string, http_status=200)

        assert result.success is False
        assert result.error is not None
        assert result.error.code == "validation_error"
        assert "expected JSON object" in result.error.message

    def test_from_json_string_null(self) -> None:
        """Test from_json_string with JSON null."""
        json_string = "null"

        result = ResponseParser.from_json_string(json_string, http_status=200)

        assert result.success is False
        assert result.error is not None
        assert result.error.code == "validation_error"

    def test_from_json_string_with_retry_count(self) -> None:
        """Test from_json_string with retry_count."""
        json_string = '{"success": true, "data": {}}'

        result = ResponseParser.from_json_string(json_string, retry_count=3)

        assert result.success is True
        assert result.retry_count == 3

    def test_from_json_string_error_response(self) -> None:
        """Test from_json_string with error response."""
        json_string = '{"success": false, "data": {"message": "API error"}}'

        result = ResponseParser.from_json_string(json_string, http_status=400)

        assert result.success is False
        assert result.error is not None
        assert result.error.message == "API error"
        assert result.http_status == 400


class TestMRRResponseStructure:
    """Tests for MRRResponse structure in parsed responses."""

    def test_response_has_required_fields_success(self) -> None:
        """Test that successful response has all required fields."""
        json_data = {"success": True, "data": {"test": "value"}}
        result = parse_response(json_data, http_status=200, retry_count=1)

        assert isinstance(result, MRRResponse)
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert hasattr(result, "error")
        assert hasattr(result, "http_status")
        assert hasattr(result, "retry_count")

    def test_response_has_required_fields_error(self) -> None:
        """Test that error response has all required fields."""
        json_data = {"success": False, "data": {"message": "Error"}}
        result = parse_response(json_data, http_status=400, retry_count=2)

        assert isinstance(result, MRRResponse)
        assert result.success is False
        assert result.data is None
        assert result.error is not None
        assert result.http_status == 400
        assert result.retry_count == 2

    def test_error_has_required_fields(self) -> None:
        """Test that error object has all required fields."""
        json_data = {"success": False, "data": {"message": "Test error"}}
        result = parse_response(json_data, http_status=400)

        assert result.error is not None
        assert hasattr(result.error, "code")
        assert hasattr(result.error, "message")
        assert hasattr(result.error, "details")
        assert hasattr(result.error, "http_status")

"""Tests for retry logic in http module."""

from __future__ import annotations
from typing import Protocol

from aio_mrr.http.http_client import (
    _get_retry_params,
    _is_retryable_result,
)


class MockResponseProtocol(Protocol):
    """Protocol for mock response objects."""

    status: int


class TestIsRetryableResult:
    """Tests for _is_retryable_result function."""

    def test_429_is_retryable(self) -> None:
        """Test that 429 status is retryable."""

        class MockResponse:
            status: int = 429

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is True
        )

    def test_500_is_retryable(self) -> None:
        """Test that 500 status is retryable."""

        class MockResponse:
            status: int = 500

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is True
        )

    def test_502_is_retryable(self) -> None:
        """Test that 502 status is retryable."""

        class MockResponse:
            status: int = 502

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is True
        )

    def test_503_is_retryable(self) -> None:
        """Test that 503 status is retryable."""

        class MockResponse:
            status: int = 503

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is True
        )

    def test_504_is_retryable(self) -> None:
        """Test that 504 status is retryable."""

        class MockResponse:
            status: int = 504

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is True
        )

    def test_200_is_not_retryable(self) -> None:
        """Test that 200 status is not retryable."""

        class MockResponse:
            status: int = 200

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is False
        )

    def test_401_is_not_retryable(self) -> None:
        """Test that 401 status is not retryable."""

        class MockResponse:
            status: int = 401

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is False
        )

    def test_404_is_not_retryable(self) -> None:
        """Test that 404 status is not retryable."""

        class MockResponse:
            status: int = 404

        assert (
            _is_retryable_result(
                MockResponse()  # type: ignore[arg-type]
            )
            is False
        )


class TestGetRetryParams:
    """Tests for _get_retry_params function."""

    def test_429_returns_stop_and_wait(self) -> None:
        """Test retry params for 429 status."""
        params = _get_retry_params(429)

        assert "stop" in params
        assert "wait" in params

    def test_500_returns_stop_and_wait(self) -> None:
        """Test retry params for 500 status."""
        params = _get_retry_params(500)

        assert "stop" in params
        assert "wait" in params

    def test_503_returns_stop_and_wait(self) -> None:
        """Test retry params for 503 status."""
        params = _get_retry_params(503)

        assert "stop" in params
        assert "wait" in params

    def test_none_returns_default_params(self) -> None:
        """Test retry params for None (connection errors)."""
        params = _get_retry_params(None)

        assert "stop" in params
        assert "wait" in params

    def test_502_returns_stop_and_wait(self) -> None:
        """Test retry params for 502 status."""
        params = _get_retry_params(502)

        assert "stop" in params
        assert "wait" in params

    def test_504_returns_stop_and_wait(self) -> None:
        """Test retry params for 504 status."""
        params = _get_retry_params(504)

        assert "stop" in params
        assert "wait" in params

    def test_400_returns_default_params(self) -> None:
        """Test retry params for 400 status (not in retry list)."""
        params = _get_retry_params(400)

        # Should use default params (connection error params)
        assert "stop" in params
        assert "wait" in params

    def test_401_returns_default_params(self) -> None:
        """Test retry params for 401 status (not in retry list)."""
        params = _get_retry_params(401)

        assert "stop" in params
        assert "wait" in params

    def test_429_has_different_params_than_500(self) -> None:
        """Test that 429 has different retry params than 500."""
        params_429 = _get_retry_params(429)
        params_500 = _get_retry_params(500)

        # Both should have stop and wait
        assert "stop" in params_429
        assert "stop" in params_500

        # The wait strategies should be different (different multipliers)
        # 429 uses multiplier=5, min=5, max=60
        # 500 uses multiplier=1, min=1, max=8
        assert params_429["wait"] != params_500["wait"]

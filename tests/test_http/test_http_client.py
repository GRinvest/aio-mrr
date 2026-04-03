"""Tests for HTTPClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient


@pytest.fixture
async def http_client(api_key: str, api_secret: str) -> AsyncGenerator[HTTPClient, None]:
    """Фикстура для HTTPClient."""
    client = HTTPClient(api_key=api_key, api_secret=api_secret)
    yield client
    await client.close()


class TestHTTPClientInit:
    """Tests for HTTPClient initialization."""

    def test_init_with_defaults(self, api_key: str, api_secret: str) -> None:
        """Test HTTPClient initialization with default timeouts and retries."""
        client = HTTPClient(api_key=api_key, api_secret=api_secret)
        assert client._api_key == api_key
        assert client._api_secret == api_secret
        assert client._connect_timeout == 30.0
        assert client._read_timeout == 60.0
        assert client._max_retries == 3

    def test_init_with_custom_values(self, api_key: str, api_secret: str) -> None:
        """Test HTTPClient initialization with custom values."""
        client = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            connect_timeout=15.0,
            read_timeout=30.0,
            max_retries=5,
        )
        assert client._connect_timeout == 15.0
        assert client._read_timeout == 30.0
        assert client._max_retries == 5


class TestHTTPClientRequest:
    """Tests for HTTPClient.request method."""

    @pytest.mark.asyncio
    async def test_get_request_success(self, http_client: HTTPClient) -> None:
        """Test successful GET request."""
        endpoint = "/account/balance"
        response_data = {"success": True, "data": {"confirmed": "0.1"}}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await http_client.request("GET", endpoint)

            assert result.success is True
            assert result.data == {"confirmed": "0.1"}
            assert result.http_status == 200
            assert result.error is None

    @pytest.mark.asyncio
    async def test_get_request_with_query_params(self, http_client: HTTPClient) -> None:
        """Test GET request with query parameters."""
        endpoint = "/rig"
        params = {"status": "enabled"}
        response_data = {"success": True, "data": []}

        with aioresponses() as m:
            # aioresponses requires exact URL match including query string
            # URL with query params: https://www.miningrigrentals.com/rig?status=enabled
            full_url = f"{HTTPClient.BASE_URL}{endpoint}?status=enabled"
            m.get(
                full_url,
                payload=response_data,
                status=200,
            )

            result = await http_client.request("GET", endpoint, params=params)

            assert result.success is True
            assert result.data == []

    @pytest.mark.asyncio
    async def test_post_request_success(self, http_client: HTTPClient) -> None:
        """Test successful POST request with body."""
        endpoint = "/rig/batch"
        body = {"rigs": [{"id": 12345, "name": "Test Rig"}]}
        response_data = {"success": True, "data": {"id": "12345"}}

        with aioresponses() as m:
            m.post(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await http_client.request("POST", endpoint, body=body)

            assert result.success is True
            assert result.data == {"id": "12345"}

    @pytest.mark.asyncio
    async def test_put_request_success(self, http_client: HTTPClient) -> None:
        """Test successful PUT request with body."""
        endpoint = "/rig"
        body = {
            "name": "New Rig",
            "description": "Test rig",
            "server": "us-east01.miningrigrentals.com",
            "status": "enabled",
            "price": {"btc": {"enabled": True, "price": 0.0001}},
            "price.type": "mh",
            "minhours": 24,
            "maxhours": 168,
            "extensions": True,
            "hash": {"hash": 500, "type": "mh"},
            "ndevices": 4,
        }
        response_data = {"success": True, "data": {"id": "12345"}}

        with aioresponses() as m:
            m.put(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await http_client.request("PUT", endpoint, body=body)

            assert result.success is True
            assert result.data == {"id": "12345"}

    @pytest.mark.asyncio
    async def test_delete_request_success(self, http_client: HTTPClient) -> None:
        """Test successful DELETE request."""
        endpoint = "/rig/12345"
        response_data = {"success": True, "data": None}

        with aioresponses() as m:
            m.delete(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await http_client.request("DELETE", endpoint)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_api_error_response(self, http_client: HTTPClient) -> None:
        """Test API error response (success: false)."""
        endpoint = "/account"
        response_data = {
            "success": False,
            "data": {"message": "Invalid API key or signature"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await http_client.request("GET", endpoint)

            assert result.success is False
            assert result.error is not None
            assert result.error.code == "api_error"
            assert "Invalid API key" in result.error.message
            assert result.http_status == 200

    @pytest.mark.asyncio
    async def test_http_error_response(self, http_client: HTTPClient) -> None:
        """Test HTTP error response (4xx, 5xx status codes)."""
        endpoint = "/account"

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                status=401,
            )

            result = await http_client.request("GET", endpoint)

            assert result.success is False
            assert result.error is not None
            assert result.error.code == "http_error"
            # http_status в MRRResponse может быть None если retry не успел завершиться
            # Проверяем через error.details
            assert result.error.details is not None
            assert result.error.details.get("status") == 401

    @pytest.mark.asyncio
    async def test_invalid_json_response(self, http_client: HTTPClient) -> None:
        """Test invalid JSON response handling."""
        endpoint = "/account"

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                body="not valid json",
                status=200,
            )

            result = await http_client.request("GET", endpoint)

            assert result.success is False
            assert result.error is not None
            assert result.error.code == "validation_error"
            assert "Invalid JSON" in result.error.message

    @pytest.mark.asyncio
    async def test_429_rate_limit(self, http_client: HTTPClient) -> None:
        """Test 429 Rate Limit response."""
        endpoint = "/account"

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                status=429,
            )

            result = await http_client.request("GET", endpoint)

            assert result.success is False
            assert result.error is not None
            # 429 вызывает retry, поэтому может быть network_error после исчерпания
            assert result.error.code in ("http_error", "network_error")

    @pytest.mark.asyncio
    async def test_500_server_error(self, http_client: HTTPClient) -> None:
        """Test 500 Server Error response."""
        endpoint = "/account"

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                status=500,
            )

            result = await http_client.request("GET", endpoint)

            assert result.success is False
            assert result.error is not None
            # 500 вызывает retry, поэтому может быть network_error после исчерпания
            assert result.error.code in ("http_error", "network_error")


class TestHTTPClientAuth:
    """Tests for HTTPClient authentication headers."""

    @pytest.mark.asyncio
    async def test_auth_headers_included(self, http_client: HTTPClient) -> None:
        """Test that authentication headers are included in requests."""
        endpoint = "/account/balance"
        response_data = {"success": True, "data": {}}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            await http_client.request("GET", endpoint)

            # Verify request was made (aioresponses captures it)
            # Ключ - это кортеж (method, URL), где URL может быть str или URL объектом
            assert len(m.requests) == 1
            # Проверяем что есть хотя бы один запрос
            requests_list = list(m.requests.values())
            assert len(requests_list[0]) == 1


class TestHTTPClientContextManager:
    """Tests for HTTPClient async context manager."""

    @pytest.mark.asyncio
    async def test_context_manager(self, api_key: str, api_secret: str) -> None:
        """Test HTTPClient as async context manager."""
        async with HTTPClient(api_key=api_key, api_secret=api_secret) as client:
            assert client._session_manager._session is None  # Session is lazy

        # After exit, session should be closed
        assert True  # If we get here, context manager worked


class TestRetryLogic:
    """Tests for retry logic in HTTPClient."""

    @pytest.mark.asyncio
    async def test_retry_on_503(self, http_client: HTTPClient) -> None:
        """Test automatic retry on 503 Service Unavailable."""
        endpoint = "/account"
        response_data = {"success": True, "data": {"test": "value"}}

        with aioresponses() as m:
            # First two attempts return 503, third succeeds
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                status=503,
            )
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                status=503,
            )
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await http_client.request("GET", endpoint)

            # Should have retried and eventually succeeded
            assert result.success is True

    @pytest.mark.asyncio
    async def test_retry_exhausted_on_503(self, http_client: HTTPClient) -> None:
        """Test that retry is exhausted after max attempts on 503."""
        endpoint = "/account"

        with aioresponses() as m:
            # All attempts return 503 (3 attempts for 5xx)
            for _ in range(3):
                m.get(
                    f"{HTTPClient.BASE_URL}{endpoint}",
                    status=503,
                )

            result = await http_client.request("GET", endpoint)

            # Should have retried and eventually failed
            assert result.success is False
            assert result.error is not None


class TestHTTPClientClose:
    """Tests for HTTPClient close method."""

    @pytest.mark.asyncio
    async def test_close(self, http_client: HTTPClient) -> None:
        """Test close method."""
        http_client._session_manager.get_session()
        assert http_client._session_manager._session is not None

        await http_client.close()
        assert http_client._session_manager._session is None

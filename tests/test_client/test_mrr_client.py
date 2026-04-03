"""Tests for MRRClient — the main facade of aio-mrr library.

This module tests the MRRClient class which serves as the primary entry point
for interacting with the MiningRigRentals API v2. Tests cover:
- Client initialization with various configurations
- Sub-client creation and dependency injection
- Context manager lifecycle (async with)
- whoami() method functionality
"""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.client.client import MRRClient
from aio_mrr.http.http_client import HTTPClient


@pytest.fixture
async def mrr_client(api_key: str, api_secret: str) -> AsyncGenerator[MRRClient, None]:
    """Fixture for MRRClient instance."""
    client = MRRClient(api_key=api_key, api_secret=api_secret)
    yield client
    await client._http_client.close()


class TestMRRClientInit:
    """Tests for MRRClient initialization."""

    def test_init_with_defaults(self, api_key: str, api_secret: str) -> None:
        """Test MRRClient initialization with default timeout and retry values."""
        client = MRRClient(api_key=api_key, api_secret=api_secret)

        assert client._api_key == api_key
        assert client._api_secret == api_secret
        assert client._connect_timeout == 30.0
        assert client._read_timeout == 60.0
        assert client._max_retries == 3
        assert isinstance(client._http_client, HTTPClient)

    def test_init_with_custom_values(self, api_key: str, api_secret: str) -> None:
        """Test MRRClient initialization with custom configuration."""
        client = MRRClient(
            api_key=api_key,
            api_secret=api_secret,
            connect_timeout=15.0,
            read_timeout=30.0,
            max_retries=5,
        )

        assert client._connect_timeout == 15.0
        assert client._read_timeout == 30.0
        assert client._max_retries == 5

    def test_subclients_created(self, api_key: str, api_secret: str) -> None:
        """Test that all sub-clients are created on initialization."""
        client = MRRClient(api_key=api_key, api_secret=api_secret)

        # Check all sub-clients exist
        assert hasattr(client, "info")
        assert hasattr(client, "account")
        assert hasattr(client, "rig")
        assert hasattr(client, "riggroup")
        assert hasattr(client, "rental")
        assert hasattr(client, "pricing")

        # Verify they are not None
        assert client.info is not None
        assert client.account is not None
        assert client.rig is not None
        assert client.riggroup is not None
        assert client.rental is not None
        assert client.pricing is not None

    def test_subclients_share_http_client(self, api_key: str, api_secret: str) -> None:
        """Test that all sub-clients share the same HTTPClient instance."""
        client = MRRClient(api_key=api_key, api_secret=api_secret)

        # All sub-clients should have the same _http_client reference
        assert client.info._http is client._http_client
        assert client.account._http is client._http_client
        assert client.rig._http is client._http_client
        assert client.riggroup._http is client._http_client
        assert client.rental._http is client._http_client
        assert client.pricing._http is client._http_client


class TestMRRClientContextManager:
    """Tests for MRRClient async context manager."""

    @pytest.mark.asyncio
    async def test_context_manager_entry(self, api_key: str, api_secret: str) -> None:
        """Test context manager entry returns the client."""
        async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
            assert isinstance(client, MRRClient)
            # Session is lazy, so it should be None before first request
            assert client._http_client._session_manager._session is None

    @pytest.mark.asyncio
    async def test_context_manager_exit_closes_session(self, api_key: str, api_secret: str) -> None:
        """Test context manager exit closes the HTTP session."""
        client = MRRClient(api_key=api_key, api_secret=api_secret)

        # First, create a session by making a request
        endpoint = "/whoami"
        response_data = {"success": True, "data": {"userid": "123", "username": "test"}}

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            # Make a request to create the session
            await client._http_client.request("GET", endpoint)

            # Session should now exist
            assert client._http_client._session_manager._session is not None

        # After exiting context manager, session should be closed (set to None)
        await client._http_client.close()
        assert client._http_client._session_manager._session is None


class TestMRRClientWhoami:
    """Tests for MRRClient.whoami() method."""

    @pytest.mark.asyncio
    async def test_whoami_success(self, mrr_client: MRRClient) -> None:
        """Test successful whoami request."""
        endpoint = "/whoami"
        response_data = {
            "success": True,
            "data": {"userid": "12345", "username": "testuser"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await mrr_client.whoami()

            assert result.success is True
            assert result.data is not None
            assert result.data["userid"] == "12345"
            assert result.data["username"] == "testuser"
            assert result.error is None
            assert result.http_status == 200

    @pytest.mark.asyncio
    async def test_whoami_api_error(self, mrr_client: MRRClient) -> None:
        """Test whoami with API error response."""
        endpoint = "/whoami"
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

            result = await mrr_client.whoami()

            assert result.success is False
            assert result.data is None
            assert result.error is not None
            assert result.error.code == "api_error"
            assert "Invalid API key" in result.error.message

    @pytest.mark.asyncio
    async def test_whoami_http_error(self, mrr_client: MRRClient) -> None:
        """Test whoami with HTTP error response (401)."""
        endpoint = "/whoami"

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                status=401,
            )

            result = await mrr_client.whoami()

            assert result.success is False
            assert result.data is None
            assert result.error is not None
            assert result.error.code == "http_error"

    @pytest.mark.asyncio
    async def test_whoami_invalid_json(self, mrr_client: MRRClient) -> None:
        """Test whoami with invalid JSON response."""
        endpoint = "/whoami"

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                body="not valid json",
                status=200,
            )

            result = await mrr_client.whoami()

            assert result.success is False
            assert result.data is None
            assert result.error is not None
            assert result.error.code == "validation_error"
            assert "Invalid JSON" in result.error.message


class TestMRRClientIntegration:
    """Integration tests for MRRClient with sub-clients."""

    @pytest.mark.asyncio
    async def test_whoami_then_account_balance(self, api_key: str, api_secret: str) -> None:
        """Test sequential calls through MRRClient facade."""
        async with MRRClient(api_key=api_key, api_secret=api_secret) as client:
            # Mock whoami response
            whoami_response = {
                "success": True,
                "data": {"userid": "123", "username": "test"},
            }

            # Mock account/balance response
            balance_response = {
                "success": True,
                "data": {"BTC": {"confirmed": "0.1", "pending": 0, "unconfirmed": "0.0"}},
            }

            with aioresponses() as m:
                m.get(
                    f"{HTTPClient.BASE_URL}/whoami",
                    payload=whoami_response,
                    status=200,
                )
                m.get(
                    f"{HTTPClient.BASE_URL}/account/balance",
                    payload=balance_response,
                    status=200,
                )

                # Call whoami
                whoami_result = await client.whoami()
                assert whoami_result.success is True
                assert whoami_result.data is not None
                assert whoami_result.data["username"] == "test"

                # Call account.get_balance through the facade
                balance_result = await client.account.get_balance()
                assert balance_result.success is True
                assert "BTC" in balance_result.data  # type: ignore[operator]

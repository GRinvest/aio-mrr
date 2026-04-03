"""Tests for PricingClient."""

from __future__ import annotations
from collections.abc import AsyncGenerator
from aioresponses import aioresponses
import pytest

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.subclients.pricing_client import PricingClient


@pytest.fixture
async def pricing_client(api_key: str, api_secret: str) -> AsyncGenerator[PricingClient, None]:
    """Fixture for PricingClient."""
    http_client = HTTPClient(api_key=api_key, api_secret=api_secret)
    client = PricingClient(http_client=http_client)
    yield client
    await http_client.close()


class TestPricingClientGetPricing:
    """Tests for PricingClient.get_pricing method."""

    @pytest.mark.asyncio
    async def test_get_pricing_success(self, pricing_client: PricingClient) -> None:
        """Test successful get_pricing request."""
        endpoint = "/pricing"
        response_data = {
            "success": True,
            "data": {
                "conversion_rates": {
                    "LTC": "0.01",
                    "ETH": "0.0001",
                    "DOGE": "0.00001",
                    "BCH": "0.001",
                },
                "market_rates": {
                    "allium": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "argon2dchukwa": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "autolykosv2": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "kawpow": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "kheavyhash": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "randomx": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "scrypt": {"BTC": "0.0001", "LTC": "0.01", "ETH": "0.0001", "BCH": "0.001", "DOGE": "0.001"},
                    "sha256": {"BTC": "0.0002", "LTC": "0.02", "ETH": "0.0002", "BCH": "0.002", "DOGE": "0.002"},
                    "x11": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                },
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await pricing_client.get_pricing()

            assert result.success is True
            assert result.data is not None
            assert result.data.conversion_rates.LTC == "0.01"
            assert result.data.market_rates.scrypt.BTC == "0.0001"
            assert result.data.market_rates.sha256.BTC == "0.0002"

    @pytest.mark.asyncio
    async def test_get_pricing_empty_rates(self, pricing_client: PricingClient) -> None:
        """Test get_pricing with empty rates."""
        endpoint = "/pricing"
        response_data = {
            "success": True,
            "data": {
                "conversion_rates": {
                    "LTC": "0.01",
                    "ETH": "0.0001",
                    "DOGE": "0.00001",
                    "BCH": "0.001",
                },
                "market_rates": {
                    "allium": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "argon2dchukwa": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "autolykosv2": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "kawpow": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "kheavyhash": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "randomx": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                    "scrypt": {"BTC": "0.0001", "LTC": "0.01", "ETH": "0.0001", "BCH": "0.001", "DOGE": "0.001"},
                    "sha256": {"BTC": "0.0002", "LTC": "0.02", "ETH": "0.0002", "BCH": "0.002", "DOGE": "0.002"},
                    "x11": {"BTC": "0.0", "LTC": "0.0", "ETH": "0.0", "BCH": "0.0", "DOGE": "0.0"},
                },
            },
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await pricing_client.get_pricing()

            assert result.success is True
            assert result.data is not None
            # Check that objects are created correctly even with empty data

    @pytest.mark.asyncio
    async def test_get_pricing_api_error(self, pricing_client: PricingClient) -> None:
        """Test get_pricing with API error response."""
        endpoint = "/pricing"
        response_data = {
            "success": False,
            "data": {"message": "Internal server error"},
        }

        with aioresponses() as m:
            m.get(
                f"{HTTPClient.BASE_URL}{endpoint}",
                payload=response_data,
                status=200,
            )

            result = await pricing_client.get_pricing()

            assert result.success is False
            assert result.error is not None
            assert result.error.code == "api_error"

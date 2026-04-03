"""Тесты для моделей Info API."""

from __future__ import annotations

from aio_mrr.models.info.request import InfoAlgosQueryParams
from aio_mrr.models.info.response import (
    AlgoInfo,
    AlgoStats,
    AvailableHashInfo,
    CurrencyInfo,
    HashInfo,
    PriceInfo,
    PricesInfo,
    RentedHashInfo,
    ServerInfo,
    ServersList,
)


class TestInfoAlgosQueryParams:
    """Тесты для модели InfoAlgosQueryParams."""

    def test_minimal_params(self) -> None:
        """Тестирует минимальные параметры (нет обязательных полей)."""
        params = InfoAlgosQueryParams()

        assert params.currency is None

    def test_with_currency(self) -> None:
        """Тестирует параметры с валютой."""
        params = InfoAlgosQueryParams(currency="LTC")

        assert params.currency == "LTC"

    def test_currency_none(self) -> None:
        """Тестирует явное задание None."""
        params = InfoAlgosQueryParams(currency=None)

        assert params.currency is None


class TestHashInfo:
    """Тесты для модели HashInfo."""

    def test_hash_info_valid(self) -> None:
        """Тестирует валидную информацию о хешрейте."""
        hash_info = HashInfo(hash=882.7, unit="gh", nice="882.70G")

        assert hash_info.hash == 882.7
        assert hash_info.unit == "gh"
        assert hash_info.nice == "882.70G"

    def test_hash_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"hash": 500.0, "unit": "mh", "nice": "500.00M"}

        hash_info = HashInfo.model_validate(api_data)

        assert hash_info.hash == 500.0
        assert hash_info.unit == "mh"
        assert hash_info.nice == "500.00M"


class TestPriceInfo:
    """Тесты для модели PriceInfo."""

    def test_price_info_valid(self) -> None:
        """Тестирует валидную информацию о цене."""
        price_info = PriceInfo(amount="0.0001", currency="BTC", unit="mh*day")

        assert price_info.amount == "0.0001"
        assert price_info.currency == "BTC"
        assert price_info.unit == "mh*day"

    def test_price_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"amount": "0.00005", "currency": "LTC", "unit": "th*day"}

        price_info = PriceInfo.model_validate(api_data)

        assert price_info.amount == "0.00005"
        assert price_info.currency == "LTC"
        assert price_info.unit == "th*day"


class TestAvailableHashInfo:
    """Тесты для модели AvailableHashInfo."""

    def test_available_hash_info_valid(self) -> None:
        """Тестирует валидную информацию о доступном хешрейте."""
        hash_info = HashInfo(hash=1000.0, unit="mh", nice="1.00T")
        available = AvailableHashInfo(rigs="50", hash=hash_info)

        assert available.rigs == "50"
        assert available.hash.hash == 1000.0
        assert available.hash.unit == "mh"


class TestRentedHashInfo:
    """Тесты для модели RentedHashInfo."""

    def test_rented_hash_info_valid(self) -> None:
        """Тестирует валидную информацию об арендованном хешрейте."""
        hash_info = HashInfo(hash=500.0, unit="gh", nice="500.00G")
        rented = RentedHashInfo(rigs="25", hash=hash_info)

        assert rented.rigs == "25"
        assert rented.hash.hash == 500.0


class TestPricesInfo:
    """Тесты для модели PricesInfo."""

    def test_prices_info_valid(self) -> None:
        """Тестирует валидную информацию о ценах."""
        lowest = PriceInfo(amount="0.00001", currency="BTC", unit="mh*day")
        last_10 = PriceInfo(amount="0.00005", currency="BTC", unit="mh*day")
        last = PriceInfo(amount="0.0001", currency="BTC", unit="mh*day")

        prices = PricesInfo(lowest=lowest, last_10=last_10, last=last)

        assert prices.lowest.amount == "0.00001"
        assert prices.last_10.amount == "0.00005"
        assert prices.last.amount == "0.0001"


class TestAlgoStats:
    """Тесты для модели AlgoStats."""

    def test_algo_stats_valid(self) -> None:
        """Тестирует валидную статистику алгоритма."""
        available = AvailableHashInfo(rigs="100", hash=HashInfo(hash=1000.0, unit="mh", nice="1.00T"))
        rented = RentedHashInfo(rigs="50", hash=HashInfo(hash=500.0, unit="mh", nice="500.00G"))
        prices = PricesInfo(
            lowest=PriceInfo(amount="0.00001", currency="BTC", unit="mh*day"),
            last_10=PriceInfo(amount="0.00005", currency="BTC", unit="mh*day"),
            last=PriceInfo(amount="0.0001", currency="BTC", unit="mh*day"),
        )

        stats = AlgoStats(available=available, rented=rented, prices=prices)

        assert stats.available.rigs == "100"
        assert stats.rented.rigs == "50"
        assert stats.prices.lowest.amount == "0.00001"


class TestAlgoInfo:
    """Тесты для модели AlgoInfo."""

    def test_algo_info_valid(self) -> None:
        """Тестирует валидную информацию об алгоритме."""
        suggested_price = PriceInfo(amount="0.0001", currency="BTC", unit="mh*day")
        stats = AlgoStats(
            available=AvailableHashInfo(rigs="100", hash=HashInfo(hash=1000.0, unit="mh", nice="1.00T")),
            rented=RentedHashInfo(rigs="50", hash=HashInfo(hash=500.0, unit="mh", nice="500.00G")),
            prices=PricesInfo(
                lowest=PriceInfo(amount="0.00001", currency="BTC", unit="mh*day"),
                last_10=PriceInfo(amount="0.00005", currency="BTC", unit="mh*day"),
                last=PriceInfo(amount="0.0001", currency="BTC", unit="mh*day"),
            ),
        )

        algo = AlgoInfo(name="scrypt", display="Scrypt", suggested_price=suggested_price, stats=stats)

        assert algo.name == "scrypt"
        assert algo.display == "Scrypt"
        assert algo.suggested_price.amount == "0.0001"

    def test_algo_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "name": "sha256",
            "display": "SHA256",
            "suggested_price": {"amount": "0.0002", "currency": "BTC", "unit": "mh*day"},
            "stats": {
                "available": {"rigs": "200", "hash": {"hash": 2000.0, "unit": "th", "nice": "2.00P"}},
                "rented": {"rigs": "100", "hash": {"hash": 1000.0, "unit": "th", "nice": "1.00P"}},
                "prices": {
                    "lowest": {"amount": "0.0001", "currency": "BTC", "unit": "mh*day"},
                    "last_10": {"amount": "0.00015", "currency": "BTC", "unit": "mh*day"},
                    "last": {"amount": "0.0002", "currency": "BTC", "unit": "mh*day"},
                },
            },
        }

        algo = AlgoInfo.model_validate(api_data)

        assert algo.name == "sha256"
        assert algo.display == "SHA256"
        assert algo.stats.available.rigs == "200"


class TestServerInfo:
    """Тесты для модели ServerInfo."""

    def test_server_info_minimal(self) -> None:
        """Тестирует минимальную информацию о сервере."""
        server = ServerInfo(id="us-east01", name="us-east01.miningrigrentals.com", region="us-east")

        assert server.id == "us-east01"
        assert server.name == "us-east01.miningrigrentals.com"
        assert server.region == "us-east"
        assert server.port is None
        assert server.ethereum_port is None

    def test_server_info_full(self) -> None:
        """Тестирует полную информацию о сервере."""
        server = ServerInfo(
            id="eu-ru01",
            name="eu-ru01.miningrigrentals.com",
            region="eu-ru",
            port="443",
            ethereum_port="8080",
        )

        assert server.port == "443"
        assert server.ethereum_port == "8080"

    def test_server_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "id": "us-central01",
            "name": "us-central01.miningrigrentals.com",
            "region": "us-central",
            "port": "443",
        }

        server = ServerInfo.model_validate(api_data)

        assert server.id == "us-central01"
        assert server.port == "443"


class TestServersList:
    """Тесты для модели ServersList."""

    def test_servers_list_valid(self) -> None:
        """Тестирует валидный список серверов."""
        servers = ServersList(
            servers=[
                ServerInfo(id="us-east01", name="us-east01.miningrigrentals.com", region="us-east"),
                ServerInfo(id="eu-ru01", name="eu-ru01.miningrigrentals.com", region="eu-ru"),
            ]
        )

        assert len(servers.servers) == 2
        assert servers.servers[0].id == "us-east01"
        assert servers.servers[1].id == "eu-ru01"

    def test_servers_list_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "servers": [
                {
                    "id": "us-central01",
                    "name": "us-central01.miningrigrentals.com",
                    "region": "us-central",
                    "port": "443",
                    "ethereum_port": "8080",
                },
                {
                    "id": "eu-de01",
                    "name": "eu-de01.miningrigrentals.com",
                    "region": "eu-de",
                },
            ]
        }

        servers = ServersList.model_validate(api_data)

        assert len(servers.servers) == 2
        assert servers.servers[0].ethereum_port == "8080"
        assert servers.servers[1].ethereum_port is None


class TestCurrencyInfo:
    """Тесты для модели CurrencyInfo."""

    def test_currency_info_valid(self) -> None:
        """Тестирует валидную информацию о валюте."""
        currency = CurrencyInfo(name="BTC", enabled=True, txfee="0.0005")

        assert currency.name == "BTC"
        assert currency.enabled is True
        assert currency.txfee == "0.0005"

    def test_currency_info_disabled(self) -> None:
        """Тестирует отключённую валюту."""
        currency = CurrencyInfo(name="DOGE", enabled=False, txfee="10.0")

        assert currency.enabled is False
        assert currency.txfee == "10.0"

    def test_currency_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"name": "LTC", "enabled": True, "txfee": "0.001"}

        currency = CurrencyInfo.model_validate(api_data)

        assert currency.name == "LTC"
        assert currency.enabled is True
        assert currency.txfee == "0.001"

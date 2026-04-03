"""Тесты для моделей Pricing API."""

from __future__ import annotations

from aio_mrr.models.pricing.response import ConversionRates, MarketRate, MarketRates, PricingInfo


class TestConversionRates:
    """Тесты для модели ConversionRates."""

    def test_conversion_rates_valid(self) -> None:
        """Тестирует валидные курсы конвертации."""
        rates = ConversionRates(LTC="0.015", ETH="0.05", BCH="0.008", DOGE="0.00001")

        assert rates.LTC == "0.015"
        assert rates.ETH == "0.05"
        assert rates.BCH == "0.008"
        assert rates.DOGE == "0.00001"

    def test_conversion_rates_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"LTC": "0.0145", "ETH": "0.052", "BCH": "0.0078", "DOGE": "0.000012"}

        rates = ConversionRates.model_validate(api_data)

        assert rates.LTC == "0.0145"
        assert rates.ETH == "0.052"
        assert rates.BCH == "0.0078"
        assert rates.DOGE == "0.000012"


class TestMarketRate:
    """Тесты для модели MarketRate."""

    def test_market_rate_valid(self) -> None:
        """Тестирует валидную рыночную ставку."""
        rate = MarketRate(BTC="0.0001", LTC="0.0015", ETH="0.005", BCH="0.0008", DOGE="0.01")

        assert rate.BTC == "0.0001"
        assert rate.LTC == "0.0015"
        assert rate.ETH == "0.005"
        assert rate.BCH == "0.0008"
        assert rate.DOGE == "0.01"

    def test_market_rate_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"BTC": "0.00012", "LTC": "0.0018", "ETH": "0.0055", "BCH": "0.0009", "DOGE": "0.012"}

        rate = MarketRate.model_validate(api_data)

        assert rate.BTC == "0.00012"
        assert rate.DOGE == "0.012"


class TestMarketRates:
    """Тесты для модели MarketRates."""

    def test_market_rates_valid(self) -> None:
        """Тестирует валидные рыночные ставки по алгоритмам."""
        scrypt_rate = MarketRate(BTC="0.0001", LTC="0.0015", ETH="0.005", BCH="0.0008", DOGE="0.01")
        sha256_rate = MarketRate(BTC="0.0002", LTC="0.003", ETH="0.01", BCH="0.0016", DOGE="0.02")

        rates = MarketRates(
            allium=MarketRate(BTC="0.00001", LTC="0.00015", ETH="0.0005", BCH="0.00008", DOGE="0.001"),
            argon2dchukwa=MarketRate(BTC="0.00002", LTC="0.0003", ETH="0.001", BCH="0.00016", DOGE="0.002"),
            autolykosv2=MarketRate(BTC="0.00003", LTC="0.00045", ETH="0.0015", BCH="0.00024", DOGE="0.003"),
            kawpow=MarketRate(BTC="0.00004", LTC="0.0006", ETH="0.002", BCH="0.00032", DOGE="0.004"),
            kheavyhash=MarketRate(BTC="0.00005", LTC="0.00075", ETH="0.0025", BCH="0.0004", DOGE="0.005"),
            randomx=MarketRate(BTC="0.00006", LTC="0.0009", ETH="0.003", BCH="0.00048", DOGE="0.006"),
            scrypt=scrypt_rate,
            sha256=sha256_rate,
            x11=MarketRate(BTC="0.00007", LTC="0.00105", ETH="0.0035", BCH="0.00056", DOGE="0.007"),
        )

        assert rates.scrypt.BTC == "0.0001"
        assert rates.sha256.BTC == "0.0002"
        assert rates.allium.LTC == "0.00015"

    def test_market_rates_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "allium": {"BTC": "0.00001", "LTC": "0.00015", "ETH": "0.0005", "BCH": "0.00008", "DOGE": "0.001"},
            "argon2dchukwa": {"BTC": "0.00002", "LTC": "0.0003", "ETH": "0.001", "BCH": "0.00016", "DOGE": "0.002"},
            "autolykosv2": {"BTC": "0.00003", "LTC": "0.00045", "ETH": "0.0015", "BCH": "0.00024", "DOGE": "0.003"},
            "kawpow": {"BTC": "0.00004", "LTC": "0.0006", "ETH": "0.002", "BCH": "0.00032", "DOGE": "0.004"},
            "kheavyhash": {"BTC": "0.00005", "LTC": "0.00075", "ETH": "0.0025", "BCH": "0.0004", "DOGE": "0.005"},
            "randomx": {"BTC": "0.00006", "LTC": "0.0009", "ETH": "0.003", "BCH": "0.00048", "DOGE": "0.006"},
            "scrypt": {"BTC": "0.0001", "LTC": "0.0015", "ETH": "0.005", "BCH": "0.0008", "DOGE": "0.01"},
            "sha256": {"BTC": "0.0002", "LTC": "0.003", "ETH": "0.01", "BCH": "0.0016", "DOGE": "0.02"},
            "x11": {"BTC": "0.00007", "LTC": "0.00105", "ETH": "0.0035", "BCH": "0.00056", "DOGE": "0.007"},
        }

        rates = MarketRates.model_validate(api_data)

        assert rates.scrypt.BTC == "0.0001"
        assert rates.sha256.ETH == "0.01"
        assert rates.randomx.DOGE == "0.006"


class TestPricingInfo:
    """Тесты для модели PricingInfo."""

    def test_pricing_info_minimal(self) -> None:
        """Тестирует минимальную информацию о ценообразовании."""
        conversion_rates = ConversionRates(LTC="0.015", ETH="0.05", BCH="0.008", DOGE="0.00001")
        market_rates = MarketRates(
            allium=MarketRate(BTC="0.00001", LTC="0.00015", ETH="0.0005", BCH="0.00008", DOGE="0.001"),
            argon2dchukwa=MarketRate(BTC="0.00002", LTC="0.0003", ETH="0.001", BCH="0.00016", DOGE="0.002"),
            autolykosv2=MarketRate(BTC="0.00003", LTC="0.00045", ETH="0.0015", BCH="0.00024", DOGE="0.003"),
            kawpow=MarketRate(BTC="0.00004", LTC="0.0006", ETH="0.002", BCH="0.00032", DOGE="0.004"),
            kheavyhash=MarketRate(BTC="0.00005", LTC="0.00075", ETH="0.0025", BCH="0.0004", DOGE="0.005"),
            randomx=MarketRate(BTC="0.00006", LTC="0.0009", ETH="0.003", BCH="0.00048", DOGE="0.006"),
            scrypt=MarketRate(BTC="0.0001", LTC="0.0015", ETH="0.005", BCH="0.0008", DOGE="0.01"),
            sha256=MarketRate(BTC="0.0002", LTC="0.003", ETH="0.01", BCH="0.0016", DOGE="0.02"),
            x11=MarketRate(BTC="0.00007", LTC="0.00105", ETH="0.0035", BCH="0.00056", DOGE="0.007"),
        )

        pricing = PricingInfo(conversion_rates=conversion_rates, market_rates=market_rates)

        assert pricing.conversion_rates.LTC == "0.015"
        assert pricing.market_rates.scrypt.BTC == "0.0001"

    def test_pricing_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "conversion_rates": {"LTC": "0.0148", "ETH": "0.051", "BCH": "0.0079", "DOGE": "0.000011"},
            "market_rates": {
                "allium": {"BTC": "0.00001", "LTC": "0.00015", "ETH": "0.0005", "BCH": "0.00008", "DOGE": "0.001"},
                "argon2dchukwa": {"BTC": "0.00002", "LTC": "0.0003", "ETH": "0.001", "BCH": "0.00016", "DOGE": "0.002"},
                "autolykosv2": {"BTC": "0.00003", "LTC": "0.00045", "ETH": "0.0015", "BCH": "0.00024", "DOGE": "0.003"},
                "kawpow": {"BTC": "0.00004", "LTC": "0.0006", "ETH": "0.002", "BCH": "0.00032", "DOGE": "0.004"},
                "kheavyhash": {"BTC": "0.00005", "LTC": "0.00075", "ETH": "0.0025", "BCH": "0.0004", "DOGE": "0.005"},
                "randomx": {"BTC": "0.00006", "LTC": "0.0009", "ETH": "0.003", "BCH": "0.00048", "DOGE": "0.006"},
                "scrypt": {"BTC": "0.0001", "LTC": "0.0015", "ETH": "0.005", "BCH": "0.0008", "DOGE": "0.01"},
                "sha256": {"BTC": "0.0002", "LTC": "0.003", "ETH": "0.01", "BCH": "0.0016", "DOGE": "0.02"},
                "x11": {"BTC": "0.00007", "LTC": "0.00105", "ETH": "0.0035", "BCH": "0.00056", "DOGE": "0.007"},
            },
        }

        pricing = PricingInfo.model_validate(api_data)

        assert pricing.conversion_rates.LTC == "0.0148"
        assert pricing.market_rates.sha256.BTC == "0.0002"
        assert pricing.market_rates.randomx.ETH == "0.003"

    def test_pricing_info_all_algorithms_present(self) -> None:
        """Тестирует наличие всех алгоритмов."""
        conversion_rates = ConversionRates(LTC="0.015", ETH="0.05", BCH="0.008", DOGE="0.00001")

        # Создаем ставки для всех алгоритмов
        market_rates = MarketRates(
            allium=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            argon2dchukwa=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            autolykosv2=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            kawpow=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            kheavyhash=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            randomx=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            scrypt=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            sha256=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
            x11=MarketRate(BTC="0", LTC="0", ETH="0", BCH="0", DOGE="0"),
        )

        pricing = PricingInfo(conversion_rates=conversion_rates, market_rates=market_rates)

        # Проверяем все алгоритмы
        assert pricing.market_rates.allium is not None
        assert pricing.market_rates.argon2dchukwa is not None
        assert pricing.market_rates.autolykosv2 is not None
        assert pricing.market_rates.kawpow is not None
        assert pricing.market_rates.kheavyhash is not None
        assert pricing.market_rates.randomx is not None
        assert pricing.market_rates.scrypt is not None
        assert pricing.market_rates.sha256 is not None
        assert pricing.market_rates.x11 is not None

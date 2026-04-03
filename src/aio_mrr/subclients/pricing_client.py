"""Pricing Client для взаимодействия с Pricing API.

Этот модуль предоставляет PricingClient для работы с Pricing API endpoint:
- GET /pricing
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.pricing.response import ConversionRates, MarketRates, PricingInfo
from aio_mrr.subclients.base import BaseSubClient


class PricingClient(BaseSubClient):
    """Client для работы с Pricing API.

    Предоставляет методы для получения информации о рыночных ставках ценообразования:
    - текущие курсы конвертации валют
    - рыночные ставки по алгоритмам майнинга

    Пример использования:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.pricing_client.get_pricing()
        ...     if response.success:
        ...         print(response.data.market_rates.scrypt.BTC)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует PricingClient.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        super().__init__(http_client)

    async def get_pricing(self) -> MRRResponse[PricingInfo]:
        """Получает информацию о рыночных ставках ценообразования.

        Возвращает текущие курсы конвертации валют относительно BTC и
        рыночные ставки по всем доступным алгоритмам майнинга в разных валютах.

        Returns:
            MRRResponse[PricingInfo] — ответ с информацией о ценообразовании:
            - При успехе: MRRResponse(success=True, data=PricingInfo)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await pricing_client.get_pricing()
            >>> if response.success:
            ...     pricing = response.data
            ...     print(f"Scrypt BTC price: {pricing.market_rates.scrypt.BTC}")
            ...     print(f"LTC to BTC rate: {pricing.conversion_rates.LTC}")
        """
        endpoint = "/pricing"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            pricing_data: dict[str, Any] = result.data
            conversion_rates_data: dict[str, str] = pricing_data.get("conversion_rates", {})
            market_rates_data: dict[str, dict[str, str]] = pricing_data.get("market_rates", {})

            conversion_rates = ConversionRates.model_validate(conversion_rates_data)
            market_rates = MarketRates.model_validate(market_rates_data)

            return MRRResponse(
                success=True,
                data=PricingInfo(
                    conversion_rates=conversion_rates,
                    market_rates=market_rates,
                ),
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

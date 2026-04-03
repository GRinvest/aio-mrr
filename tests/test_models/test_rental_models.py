"""Тесты для моделей Rental API."""

from __future__ import annotations

from aio_mrr.models.rental.request import RentalCreateBody, RentalExtendBody, RentalListQueryParams, RentalPoolBody
from aio_mrr.models.rental.response import (
    GraphData,
    GraphDataPoint,
    RateInfo,
    RentalCostInfo,
    RentalHashInfo,
    RentalInfo,
    RentalList,
    RentalLogEntry,
    RentalMessage,
)


class TestRentalListQueryParams:
    """Тесты для модели RentalListQueryParams."""

    def test_minimal_params(self) -> None:
        """Тестирует минимальные параметры."""
        params = RentalListQueryParams()

        assert params.type is None
        assert params.algo is None

    def test_with_type(self) -> None:
        """Тестирует параметры с типом."""
        params = RentalListQueryParams(type="renter")

        assert params.type == "renter"

    def test_with_owner_type(self) -> None:
        """Тестирует параметры с типом owner."""
        params = RentalListQueryParams(type="owner")

        assert params.type == "owner"

    def test_with_filters(self) -> None:
        """Тестирует параметры с фильтрами."""
        params = RentalListQueryParams(
            algo="scrypt",
            history=True,
            rig=12345,
            currency="LTC",
        )

        assert params.algo == "scrypt"
        assert params.history is True
        assert params.rig == 12345
        assert params.currency == "LTC"

    def test_with_pagination(self) -> None:
        """Тестирует параметры пагинации."""
        params = RentalListQueryParams(start=10, limit=50)

        assert params.start == 10
        assert params.limit == 50


class TestRentalCreateBody:
    """Тесты для модели RentalCreateBody."""

    def test_create_body_minimal(self) -> None:
        """Тестирует минимальное тело запроса."""
        body = RentalCreateBody(rig=12345, length=24.0, profile=678)

        assert body.rig == 12345
        assert body.length == 24.0
        assert body.profile == 678
        assert body.currency is None

    def test_create_body_full(self) -> None:
        """Тестирует полное тело запроса."""
        data = {
            "rig": 12345,
            "length": 48.0,
            "profile": 678,
            "currency": "LTC",
            "rate.type": "mh",
            "rate.price": 0.0001,
        }
        body = RentalCreateBody.model_validate(data)

        assert body.currency == "LTC"
        assert body.rate_type == "mh"
        assert body.rate_price == 0.0001


class TestRentalExtendBody:
    """Тесты для модели RentalExtendBody."""

    def test_extend_body_minimal(self) -> None:
        """Тестирует минимальное тело запроса."""
        body = RentalExtendBody(length=12.0)

        assert body.length == 12.0
        assert body.getcost is None

    def test_extend_body_with_cost(self) -> None:
        """Тестирует тело запроса с getcost."""
        body = RentalExtendBody(length=24.0, getcost=True)

        assert body.length == 24.0
        assert body.getcost is True


class TestRentalPoolBody:
    """Тесты для модели RentalPoolBody."""

    def test_pool_body_minimal(self) -> None:
        """Тестирует минимальное тело запроса."""
        data = {"host": "pool.com", "port": 3333, "user": "worker", "pass": "pass"}
        body = RentalPoolBody.model_validate(data)

        assert body.host == "pool.com"
        assert body.port == 3333
        assert body.user == "worker"
        assert body.password == "pass"
        assert body.priority is None

    def test_pool_body_with_priority(self) -> None:
        """Тестирует тело запроса с приоритетом."""
        data = {
            "host": "pool.minergate.com",
            "port": 8080,
            "user": "worker1",
            "pass": "secret",
            "priority": 1,
        }
        body = RentalPoolBody.model_validate(data)

        assert body.priority == 1


class TestRateInfo:
    """Тесты для модели RateInfo."""

    def test_rate_info_minimal(self) -> None:
        """Тестирует минимальную информацию о ставке."""
        rate = RateInfo()

        assert rate.type is None
        assert rate.price is None

    def test_rate_info_full(self) -> None:
        """Тестирует полную информацию о ставке."""
        rate = RateInfo(**{"rate.type": "mh"}, **{"rate.price": "0.0001"})

        assert rate.type == "mh"
        assert rate.price == "0.0001"

    def test_rate_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API с alias."""
        api_data = {"rate.type": "gh", "rate.price": "0.00005"}

        rate = RateInfo.model_validate(api_data)

        assert rate.type == "gh"
        assert rate.price == "0.00005"


class TestRentalHashInfo:
    """Тесты для модели RentalHashInfo."""

    def test_hash_info_minimal(self) -> None:
        """Тестирует минимальную информацию о хешрейте."""
        hash_info = RentalHashInfo()

        assert hash_info.hash is None
        assert hash_info.type is None

    def test_hash_info_full(self) -> None:
        """Тестирует полную информацию о хешрейте."""
        hash_info = RentalHashInfo(hash=500.0, type="mh")

        assert hash_info.hash == 500.0
        assert hash_info.type == "mh"


class TestRentalCostInfo:
    """Тесты для модели RentalCostInfo."""

    def test_cost_info_minimal(self) -> None:
        """Тестирует минимальную информацию о стоимости."""
        cost = RentalCostInfo()

        assert cost.amount is None
        assert cost.currency is None

    def test_cost_info_full(self) -> None:
        """Тестирует полную информацию о стоимости."""
        cost = RentalCostInfo(amount="0.0024", currency="BTC")

        assert cost.amount == "0.0024"
        assert cost.currency == "BTC"


class TestRentalInfo:
    """Тесты для модели RentalInfo."""

    def test_rental_info_minimal(self) -> None:
        """Тестирует минимальную информацию об аренде."""
        rental = RentalInfo(id="rental123", rig_id="12345")

        assert rental.id == "rental123"
        assert rental.rig_id == "12345"
        assert rental.rig_name is None

    def test_rental_info_full(self) -> None:
        """Тестирует полную информацию об аренде."""
        rate_data = {"rate.type": "mh", "rate.price": "0.0001"}
        rate = RateInfo.model_validate(rate_data)
        hash_info = RentalHashInfo(hash=500.0, type="mh")
        cost = RentalCostInfo(amount="0.0024", currency="BTC")

        rental = RentalInfo(
            id="rental456",
            rig_id="12345",
            rig_name="My Rig",
            owner="rigowner",
            renter="renter1",
            status="active",
            started="2024-01-01T12:00:00Z",
            ends="2024-01-02T12:00:00Z",
            length=24.0,
            currency="BTC",
            rate=rate,
            hash=hash_info,
            cost=cost,
        )

        assert rental.rig_name == "My Rig"
        assert rental.owner == "rigowner"
        assert rental.renter == "renter1"
        assert rental.status == "active"
        assert rental.length == 24.0
        assert rental.rate is not None
        assert rental.hash is not None
        assert rental.cost is not None

    def test_rental_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "id": "api_rental",
            "rig_id": "67890",
            "rig_name": "API Rig",
            "owner": "api_owner",
            "renter": "api_renter",
            "status": "active",
            "started": "2024-01-01T00:00:00Z",
            "ends": "2024-01-01T23:59:59Z",
            "length": 24.0,
            "currency": "LTC",
            "rate": {"rate.type": "gh", "rate.price": "0.00005"},
            "hash": {"hash": 1000.0, "type": "gh"},
            "cost": {"amount": "0.0012", "currency": "LTC"},
        }

        rental = RentalInfo.model_validate(api_data)

        assert rental.id == "api_rental"
        assert rental.currency == "LTC"
        assert rental.rate is not None
        assert rental.rate.type == "gh"


class TestRentalList:
    """Тесты для модели RentalList."""

    def test_rental_list_valid(self) -> None:
        """Тестирует валидный список аренд."""
        rental1 = RentalInfo(id="rental1", rig_id="12345")
        rental2 = RentalInfo(id="rental2", rig_id="12346")

        rental_list = RentalList(rentals=[rental1, rental2])

        assert len(rental_list.rentals) == 2
        assert rental_list.rentals[0].id == "rental1"

    def test_rental_list_empty(self) -> None:
        """Тестирует пустой список аренд."""
        rental_list = RentalList(rentals=[])

        assert len(rental_list.rentals) == 0


class TestRentalLogEntry:
    """Тесты для модели RentalLogEntry."""

    def test_log_entry_valid(self) -> None:
        """Тестирует валидную запись журнала."""
        entry = RentalLogEntry(time="2024-01-01T12:00:00Z", message="Rental started")

        assert entry.time == "2024-01-01T12:00:00Z"
        assert entry.message == "Rental started"

    def test_log_entry_various_messages(self) -> None:
        """Тестирует различные сообщения."""
        messages = [
            "Rental created",
            "Rig connected",
            "Rig disconnected",
            "Rental extended",
            "Rental ended",
        ]

        for msg in messages:
            entry = RentalLogEntry(time="2024-01-01T12:00:00Z", message=msg)
            assert entry.message == msg


class TestRentalMessage:
    """Тесты для модели RentalMessage."""

    def test_message_valid(self) -> None:
        """Тестирует валидное сообщение."""
        message = RentalMessage(time="2024-01-01T12:00:00Z", user="testuser", message="Hello")

        assert message.time == "2024-01-01T12:00:00Z"
        assert message.user == "testuser"
        assert message.message == "Hello"

    def test_message_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"time": "2024-01-01T14:00:00Z", "user": "admin", "message": "System maintenance"}

        message = RentalMessage.model_validate(api_data)

        assert message.user == "admin"
        assert message.message == "System maintenance"


class TestGraphDataPoint:
    """Тесты для модели GraphDataPoint."""

    def test_graph_data_point_minimal(self) -> None:
        """Тестирует минимальную точку данных."""
        point = GraphDataPoint()

        assert point.time is None
        assert point.hashrate is None
        assert point.downtime is None

    def test_graph_data_point_with_hashrate(self) -> None:
        """Тестирует точку данных с хешрейтом."""
        point = GraphDataPoint(time="2024-01-01T12:00:00Z", hashrate=500.0, downtime=False)

        assert point.time == "2024-01-01T12:00:00Z"
        assert point.hashrate == 500.0
        assert point.downtime is False

    def test_graph_data_point_downtime(self) -> None:
        """Тестирует точку данных о простое."""
        point = GraphDataPoint(time="2024-01-01T13:00:00Z", downtime=True)

        assert point.downtime is True
        assert point.hashrate is None


class TestGraphData:
    """Тесты для модели GraphData."""

    def test_graph_data_minimal(self) -> None:
        """Тестирует минимальные графические данные."""
        graph_data = GraphData()

        assert graph_data.hashrate_data is None
        assert graph_data.downtime_data is None
        assert graph_data.hours is None

    def test_graph_data_full(self) -> None:
        """Тестирует полные графические данные."""
        hashrate_data = [
            GraphDataPoint(time="2024-01-01T12:00:00Z", hashrate=500.0),
            GraphDataPoint(time="2024-01-01T13:00:00Z", hashrate=498.5),
        ]
        downtime_data = [GraphDataPoint(time="2024-01-01T14:00:00Z", downtime=True)]

        graph_data = GraphData(hashrate_data=hashrate_data, downtime_data=downtime_data, hours=24.0)

        assert graph_data.hashrate_data is not None
        assert graph_data.downtime_data is not None
        assert len(graph_data.hashrate_data) == 2
        assert len(graph_data.downtime_data) == 1
        assert graph_data.hours == 24.0

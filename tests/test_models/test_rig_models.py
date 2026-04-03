"""Тесты для моделей Rig API."""

from __future__ import annotations

from aio_mrr.models.rig.request import (
    RigBatchBody,
    RigCreateBody,
    RigExtendBody,
    RigPoolBody,
    RigSearchParams,
)
from aio_mrr.models.rig.response import (
    RigGraphData,
    RigHashInfo,
    RigInfo,
    RigList,
    RigPortInfo,
    RigPriceInfo,
    RigThreadInfo,
    RigThreadDetail,
)


class TestRigSearchParams:
    """Тесты для модели RigSearchParams."""

    def test_minimal_params(self) -> None:
        """Тестирует минимальные параметры с только обязательным полем."""
        params = RigSearchParams(type="scrypt")

        assert params.type == "scrypt"
        assert params.currency is None

    def test_with_currency(self) -> None:
        """Тестирует параметры с валютой."""
        params = RigSearchParams(type="sha256", currency="LTC")

        assert params.currency == "LTC"

    def test_with_filters(self) -> None:
        """Тестирует параметры с фильтрами."""
        data = {
            "type": "scrypt",
            "minhours.min": 24,
            "minhours.max": 168,
            "hash.min": 100,
            "hash.max": 1000,
            "price.min": 0.0001,
            "price.max": 0.001,
        }
        params = RigSearchParams.model_validate(data)

        assert params.minhours_min == 24
        assert params.hash_min == 100
        assert params.price_min == 0.0001

    def test_with_status_filter(self) -> None:
        """Тестирует фильтры по статусу."""
        params = RigSearchParams(type="scrypt", offline=True, rented=False)

        assert params.offline is True
        assert params.rented is False

    def test_with_sorting(self) -> None:
        """Тестирует параметры сортировки."""
        params = RigSearchParams(type="scrypt", orderby="score", orderdir="desc")

        assert params.orderby == "score"
        assert params.orderdir == "desc"

    def test_with_pagination(self) -> None:
        """Тестирует параметры пагинации."""
        params = RigSearchParams(type="scrypt", count=50, offset=100)

        assert params.count == 50
        assert params.offset == 100


class TestRigCreateBody:
    """Тесты для модели RigCreateBody."""

    def test_create_body_minimal(self) -> None:
        """Тестирует минимальное тело запроса."""
        body = RigCreateBody(name="My Rig", server="us-east01.miningrigrentals.com")

        assert body.name == "My Rig"
        assert body.server == "us-east01.miningrigrentals.com"

    def test_create_body_full(self) -> None:
        """Тестирует полное тело запроса."""
        data = {
            "name": "My Scrypt Rig",
            "description": "High performance scrypt rig",
            "server": "us-east01.miningrigrentals.com",
            "status": "enabled",
            "price.btc.enabled": True,
            "price.btc.price": 0.0001,
            "price.btc.autoprice": False,
            "price.type": "mh",
            "minhours": 24.0,
            "maxhours": 168.0,
            "extensions": True,
            "hash.hash": 500.0,
            "hash.type": "mh",
            "suggested_diff": 1000.0,
            "ndevices": 4,
        }
        body = RigCreateBody.model_validate(data)

        assert body.description == "High performance scrypt rig"
        assert body.price_btc_price == 0.0001
        assert body.hash_hash == 500.0
        assert body.ndevices == 4


class TestRigBatchBody:
    """Тесты для модели RigBatchBody."""

    def test_batch_body_valid(self) -> None:
        """Тестирует валидное тело запроса."""
        body = RigBatchBody(
            rigs=[
                {"id": 12345, "name": "Updated Name", "status": "disabled"},
                {"id": 12346, "name": "Another Rig", "status": "enabled"},
            ]
        )

        assert len(body.rigs) == 2
        assert body.rigs[0]["id"] == 12345


class TestRigExtendBody:
    """Тесты для модели RigExtendBody."""

    def test_extend_body_hours(self) -> None:
        """Тестирует продление часами."""
        body = RigExtendBody(hours=24.0)

        assert body.hours == 24.0
        assert body.minutes is None

    def test_extend_body_minutes(self) -> None:
        """Тестирует продление минутами."""
        body = RigExtendBody(hours=1.0, minutes=30.0)

        assert body.hours == 1.0
        assert body.minutes == 30.0


class TestRigPoolBody:
    """Тесты для модели RigPoolBody."""

    def test_pool_body_valid(self) -> None:
        """Тестирует валидное тело запроса."""
        data = {
            "host": "pool.minergate.com",
            "port": 3333,
            "user": "worker1",
            "pass": "secret",
            "priority": 0,
        }
        body = RigPoolBody.model_validate(data)

        assert body.host == "pool.minergate.com"
        assert body.port == 3333
        assert body.password == "secret"
        assert body.priority == 0

    def test_pool_body_without_priority(self) -> None:
        """Тестирует тело запроса без приоритета."""
        data = {"host": "pool.com", "port": 8080, "user": "worker", "pass": "pass"}
        body = RigPoolBody.model_validate(data)

        assert body.priority is None


class TestRigPriceInfo:
    """Тесты для модели RigPriceInfo."""

    def test_price_info_minimal(self) -> None:
        """Тестирует минимальную информацию о цене."""
        price = RigPriceInfo()

        assert price.enabled is None
        assert price.price is None

    def test_price_info_full(self) -> None:
        """Тестирует полную информацию о цене."""
        price = RigPriceInfo(
            enabled=True,
            price=0.0001,
            autoprice=False,
            minimum=0.00005,
            modifier="+10%",
        )

        assert price.enabled is True
        assert price.price == 0.0001
        assert price.autoprice is False
        assert price.modifier == "+10%"


class TestRigHashInfo:
    """Тесты для модели RigHashInfo."""

    def test_hash_info_minimal(self) -> None:
        """Тестирует минимальную информацию о хешрейте."""
        hash_info = RigHashInfo()

        assert hash_info.hash is None
        assert hash_info.type is None

    def test_hash_info_full(self) -> None:
        """Тестирует полную информацию о хешрейте."""
        hash_info = RigHashInfo(hash=500.0, type="mh")

        assert hash_info.hash == 500.0
        assert hash_info.type == "mh"


class TestRigInfo:
    """Тесты для модели RigInfo."""

    def test_rig_info_minimal(self) -> None:
        """Тестирует минимальную информацию о rig."""
        rig = RigInfo(id=12345, name="My Rig")

        assert rig.id == 12345
        assert rig.name == "My Rig"
        assert rig.description is None

    def test_rig_info_full(self) -> None:
        """Тестирует полную информацию о rig."""
        price = {"BTC": RigPriceInfo(enabled=True, price=0.0001, autoprice=False)}
        hash_info = RigHashInfo(hash=500.0, type="mh")

        rig = RigInfo(
            id=12345,
            name="My Scrypt Rig",
            description="High performance rig",
            server="us-east01.miningrigrentals.com",
            status="enabled",
            price=price,
            **{"price.type": "mh"},
            minhours=24.0,
            maxhours=168.0,
            extensions=True,
            hash=hash_info,
            suggested_diff=1000.0,
            ndevices=4,
            type="scrypt",
            region="us-east",
            online=True,
            rented=False,
            last_hashrate=498.5,
            rpi=85,
            owner="testuser",
        )

        assert rig.description == "High performance rig"
        assert rig.price is not None
        assert rig.hash is not None
        assert rig.hash.hash == 500.0
        assert rig.rpi == 85

    def test_rig_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "id": 67890,
            "name": "API Rig",
            "description": "From API",
            "server": "eu-ru01.miningrigrentals.com",
            "status": "enabled",
            "price": {"BTC": {"enabled": True, "price": 0.0002, "autoprice": True}},
            "hash": {"hash": 1000.0, "type": "gh"},
            "type": "scrypt",
            "online": True,
            "rented": False,
            "rpi": 90,
        }

        rig = RigInfo.model_validate(api_data)

        assert rig.id == 67890
        assert rig.online is True
        assert rig.rpi == 90


class TestRigList:
    """Тесты для модели RigList."""

    def test_rig_list_valid(self) -> None:
        """Тестирует валидный список ригов."""
        rig1 = RigInfo(id=12345, name="Rig 1")
        rig2 = RigInfo(id=12346, name="Rig 2")

        rig_list = RigList(rigs=[rig1, rig2])

        assert len(rig_list.rigs) == 2
        assert rig_list.rigs[0].id == 12345

    def test_rig_list_empty(self) -> None:
        """Тестирует пустой список ригов."""
        rig_list = RigList(rigs=[])

        assert len(rig_list.rigs) == 0


class TestRigPortInfo:
    """Тесты для модели RigPortInfo."""

    def test_port_info_valid(self) -> None:
        """Тестирует валидную информацию о порте."""
        port_info = RigPortInfo(port=443)

        assert port_info.port == 443
        assert port_info.rigid is None

    def test_port_info_full(self) -> None:
        """Тестирует полную информацию о порте."""
        port_info = RigPortInfo(
            rigid="207563", port=51874, server="eu-de02.miningrigrentals.com", worker="KnsMiner.207563"
        )

        assert port_info.port == 51874
        assert port_info.rigid == "207563"
        assert port_info.server == "eu-de02.miningrigrentals.com"
        assert port_info.worker == "KnsMiner.207563"


class TestRigThreadInfo:
    """Тесты для модели RigThreadInfo."""

    def test_thread_info_minimal(self) -> None:
        """Тестирует минимальную информацию о thread."""
        thread = RigThreadInfo(rigid="207563", access="owner", threads=[])

        assert thread.rigid == "207563"
        assert thread.access == "owner"
        assert thread.threads == []

    def test_thread_info_full(self) -> None:
        """Тестирует полную информацию о thread."""
        detail = RigThreadDetail(id=1, worker="worker1", status="active", hashrate=250.0)
        thread = RigThreadInfo(rigid="207563", access="owner", threads=[detail])

        assert len(thread.threads) == 1
        assert thread.threads[0].worker == "worker1"
        assert thread.threads[0].hashrate == 250.0


class TestRigThreadDetail:
    """Тесты для модели RigThreadDetail."""

    def test_detail_minimal(self) -> None:
        """Тестирует минимальные детали thread."""
        detail = RigThreadDetail()
        assert detail.id is None
        assert detail.worker is None

    def test_detail_full(self) -> None:
        """Тестирует полные детали thread."""
        detail = RigThreadDetail(
            id=2, worker="worker2", status="active", hashrate=500.0, last_share="2024-01-01T12:00:00Z"
        )
        assert detail.hashrate == 500.0
        assert detail.last_share == "2024-01-01T12:00:00Z"


class TestRigGraphData:
    """Тесты для модели RigGraphData."""

    def test_graph_data_minimal(self) -> None:
        """Тестирует минимальные графические данные."""
        graph_data = RigGraphData()

        assert graph_data.rigid is None
        assert graph_data.chartdata is None

    def test_graph_data_full(self) -> None:
        """Тестирует полные графические данные."""
        chartdata = {
            "time_start": "2024-01-01 12:00:00",
            "time_end": "2024-01-02 12:00:00",
            "bars": "[1704110400000,500],[1704110460000,498]",
        }
        graph_data = RigGraphData(rigid="207563", chartdata=chartdata)

        assert graph_data.rigid == "207563"
        assert graph_data.chartdata is not None
        assert graph_data.chartdata["time_start"] == "2024-01-01 12:00:00"

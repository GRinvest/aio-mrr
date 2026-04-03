"""Тесты для моделей Account API."""

from __future__ import annotations
import pytest

from aio_mrr.models.account.request import (
    PoolCreateBody,
    PoolTestBody,
    ProfileCreateBody,
    TransactionsQueryParams,
)
from aio_mrr.models.account.response import (
    AccountInfo,
    AlgoPoolInfo,
    AlgoProfileInfo,
    BalanceInfo,
    CurrencyStatus,
    DepositCurrencyInfo,
    NotificationsInfo,
    Pool,
    PoolCreateResponse,
    PoolProfileInfo,
    PoolTestResult,
    PoolTestResultItem,
    PriceInfo,
    Profile,
    ProfileCreateResponse,
    ProfileDeleteResponse,
    SettingsInfo,
    Transaction,
    TransactionsList,
    WithdrawCurrencyInfo,
)


class TestTransactionsQueryParams:
    """Тесты для модели TransactionsQueryParams."""

    def test_minimal_params(self) -> None:
        """Тестирует минимальные параметры."""
        params = TransactionsQueryParams()

        assert params.start is None
        assert params.limit is None

    def test_with_pagination(self) -> None:
        """Тестирует параметры с пагинацией."""
        params = TransactionsQueryParams(start=10, limit=50)

        assert params.start == 10
        assert params.limit == 50

    def test_with_filters(self) -> None:
        """Тестирует параметры с фильтрами."""
        params = TransactionsQueryParams(
            algo="scrypt",
            type="credit",
            rig=12345,
            rental=67890,
        )

        assert params.algo == "scrypt"
        assert params.type == "credit"
        assert params.rig == 12345
        assert params.rental == 67890


class TestProfileCreateBody:
    """Тесты для модели ProfileCreateBody."""

    def test_create_body_valid(self) -> None:
        """Тестирует валидное тело запроса."""
        body = ProfileCreateBody(name="My Profile", algo="scrypt")

        assert body.name == "My Profile"
        assert body.algo == "scrypt"

    def test_create_body_missing_required(self) -> None:
        """Тестирует ошибку при отсутствии обязательных полей."""
        with pytest.raises(ValueError):
            ProfileCreateBody(name="My Profile")  # type: ignore


class TestPoolTestBody:
    """Тесты для модели PoolTestBody."""

    def test_simple_test(self) -> None:
        """Тестирует простой тест пула."""
        body = PoolTestBody(method="simple", host="de.minexmr.com:4444")

        assert body.method == "simple"
        assert body.host == "de.minexmr.com:4444"
        assert body.type is None
        assert body.user is None

    def test_full_test(self) -> None:
        """Тестирует полный тест пула."""
        body = PoolTestBody(
            method="full",
            type="cryptonote",
            host="de.minexmr.com",
            port=4444,
            user="test",
            **{"pass": "x"},
        )

        assert body.method == "full"
        assert body.type == "cryptonote"
        assert body.user == "test"
        assert body.password == "x"

    def test_with_source(self) -> None:
        """Тестирует тест с указанием сервера."""
        body = PoolTestBody(method="simple", host="pool.com:3333", source="us-central01")

        assert body.source == "us-central01"


class TestPoolCreateBody:
    """Тесты для модели PoolCreateBody."""

    def test_create_body_valid(self) -> None:
        """Тестирует валидное тело запроса."""
        body = PoolCreateBody(
            type="scrypt",
            name="My Pool",
            host="pool.minergate.com",
            port=3333,
            user="worker1",
            **{"pass": "secret"},
            notes="Primary pool",
        )

        assert body.type == "scrypt"
        assert body.name == "My Pool"
        assert body.host == "pool.minergate.com"
        assert body.port == 3333
        assert body.user == "worker1"
        assert body.password == "secret"
        assert body.notes == "Primary pool"

    def test_create_body_without_password(self) -> None:
        """Тестирует создание пула без пароля."""
        body = PoolCreateBody(
            type="sha256",
            name="Pool without pass",
            host="pool.com",
            port=8080,
            user="worker",
        )

        assert body.password is None


class TestWithdrawCurrencyInfo:
    """Тесты для модели WithdrawCurrencyInfo."""

    def test_withdraw_info_valid(self) -> None:
        """Тестирует валидную информацию о выводе."""
        info = WithdrawCurrencyInfo(
            address="bc1qexample",
            label="Main Wallet",
            auto_pay_threshold="0.01",
            txfee=0.0005,
        )

        assert info.address == "bc1qexample"
        assert info.label == "Main Wallet"
        assert info.auto_pay_threshold == "0.01"
        assert info.txfee == 0.0005


class TestDepositCurrencyInfo:
    """Тесты для модели DepositCurrencyInfo."""

    def test_deposit_info_valid(self) -> None:
        """Тестирует валидную информацию о депозите."""
        info = DepositCurrencyInfo(address="ltc1qexample")

        assert info.address == "ltc1qexample"


class TestNotificationsInfo:
    """Тесты для модели NotificationsInfo."""

    def test_notifications_valid(self) -> None:
        """Тестирует валидную информацию о уведомлениях."""
        info = NotificationsInfo(
            rental_comm="enabled",
            new_rental="enabled",
            offline="enabled",
            news="disabled",
            deposit="enabled",
        )

        assert info.rental_comm == "enabled"
        assert info.new_rental == "enabled"
        assert info.deposit == "enabled"


class TestSettingsInfo:
    """Тесты для модели SettingsInfo."""

    def test_settings_valid(self) -> None:
        """Тестирует валидную информацию о настройках."""
        info = SettingsInfo(
            live_data="enabled",
            public_profile="enabled",
            two_factor_auth="enabled",
        )

        assert info.live_data == "enabled"
        assert info.two_factor_auth == "enabled"

    def test_settings_with_alternate_field(self) -> None:
        """Тестирует маппинг поля 2factor_auth."""
        # API возвращает '2factor_auth' вместо 'two_factor_auth'
        info = SettingsInfo(live_data="enabled", public_profile="enabled", **{"2factor_auth": "enabled"})

        assert info.two_factor_auth == "enabled"


class TestAccountInfo:
    """Тесты для модели AccountInfo."""

    def test_account_info_valid(self) -> None:
        """Тестирует валидную информацию об аккаунте."""
        withdraw = {
            "BTC": WithdrawCurrencyInfo(address="bc1q", label="Wallet", auto_pay_threshold="0.01", txfee=0.0005)
        }
        deposit = {"BTC": DepositCurrencyInfo(address="bc1qdeposit")}
        notifications = NotificationsInfo(
            rental_comm="enabled", new_rental="enabled", offline="enabled", news="disabled", deposit="enabled"
        )
        settings = SettingsInfo(live_data="enabled", public_profile="enabled", two_factor_auth="enabled")

        account = AccountInfo(
            username="testuser",
            email="test@example.com",
            withdraw=withdraw,
            deposit=deposit,
            notifications=notifications,
            settings=settings,
        )

        assert account.username == "testuser"
        assert account.email == "test@example.com"
        assert "BTC" in account.withdraw
        assert account.notifications.news == "disabled"


class TestBalanceInfo:
    """Тесты для модели BalanceInfo."""

    def test_balance_info_valid(self) -> None:
        """Тестирует валидную информацию о балансе."""
        balance = BalanceInfo(confirmed="0.09449622", pending=0.0, unconfirmed="0.00000000")

        assert balance.confirmed == "0.09449622"
        assert balance.pending == 0.0
        assert balance.unconfirmed == "0.00000000"

    def test_balance_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {"confirmed": "1.5", "pending": 0.25, "unconfirmed": "0.1"}

        balance = BalanceInfo.model_validate(api_data)

        assert balance.confirmed == "1.5"
        assert balance.pending == 0.25
        assert balance.unconfirmed == "0.1"


class TestTransaction:
    """Тесты для модели Transaction."""

    def test_transaction_minimal(self) -> None:
        """Тестирует минимальную транзакцию."""
        tx = Transaction(id="tx123", type="credit", amount="0.1", when="2024-01-01T12:00:00Z", status="Cleared")

        assert tx.id == "tx123"
        assert tx.type == "credit"
        assert tx.amount == "0.1"
        assert tx.rig is None

    def test_transaction_full(self) -> None:
        """Тестирует полную транзакцию."""
        tx = Transaction(
            id="tx456",
            type="payout",
            currency="BTC",
            amount="-0.05",
            when="2024-01-02T14:30:00Z",
            txid="abc123def456",
            txfee="0.0001",
            payout_address="bc1qexample",
            sent="true",
            status="Cleared",
            info="Payout processed",
        )

        assert tx.txid == "abc123def456"
        assert tx.txfee == "0.0001"
        assert tx.payout_address == "bc1qexample"

    def test_transaction_with_rental(self) -> None:
        """Тестирует транзакцию с арендой."""
        tx = Transaction(
            id="tx789",
            type="payment",
            amount="-0.001",
            when="2024-01-03T10:00:00Z",
            rental="12345",
            rig="67890",
            status="Cleared",
        )

        assert tx.rental == "12345"
        assert tx.rig == "67890"


class TestTransactionsList:
    """Тесты для модели TransactionsList."""

    def test_transactions_list_valid(self) -> None:
        """Тестирует валидный список транзакций."""
        tx = Transaction(id="tx1", type="credit", amount="0.1", when="2024-01-01T12:00:00Z", status="Cleared")
        tx2 = Transaction(id="tx2", type="debit", amount="-0.05", when="2024-01-02T12:00:00Z", status="Cleared")

        tx_list = TransactionsList(total="100", returned=2, start=0, limit=100, transactions=[tx, tx2])

        assert tx_list.total == "100"
        assert tx_list.returned == 2
        assert len(tx_list.transactions) == 2


class TestPriceInfo:
    """Тесты для модели PriceInfo (в контексте Account)."""

    def test_price_info_valid(self) -> None:
        """Тестирует валидную информацию о цене."""
        price = PriceInfo(amount="0.0001", currency="BTC", unit="mh*day")

        assert price.amount == "0.0001"
        assert price.currency == "BTC"


class TestAlgoProfileInfo:
    """Тесты для модели AlgoProfileInfo (в контексте Account)."""

    def test_algo_profile_info_valid(self) -> None:
        """Тестирует валидную информацию об алгоритме."""
        suggested_price = PriceInfo(amount="0.0001", currency="BTC", unit="mh*day")
        algo = AlgoProfileInfo(name="scrypt", display="Scrypt", suggested_price=suggested_price)

        assert algo.name == "scrypt"
        assert algo.display == "Scrypt"


class TestPoolProfileInfo:
    """Тесты для модели PoolProfileInfo."""

    def test_pool_profile_info_valid(self) -> None:
        """Тестирует валидную информацию о пуле профиля."""
        pool = PoolProfileInfo(
            priority=0,
            type="scrypt",
            host="pool.minergate.com",
            port="3333",
            user="worker1",
            **{"pass": "secret"},
            status="active",
        )

        assert pool.priority == 0
        assert pool.host == "pool.minergate.com"
        assert pool.password == "secret"

    def test_pool_profile_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API с alias 'pass'."""
        api_data = {
            "priority": 1,
            "type": "sha256",
            "host": "pool.com",
            "port": "8080",
            "user": "worker",
            "pass": "password123",
            "status": "active",
        }

        pool = PoolProfileInfo.model_validate(api_data)

        assert pool.password == "password123"
        assert pool.priority == 1


class TestProfile:
    """Тесты для модели Profile."""

    def test_profile_valid(self) -> None:
        """Тестирует валидный профиль."""
        algo = AlgoProfileInfo(
            name="scrypt",
            display="Scrypt",
            suggested_price=PriceInfo(amount="0.0001", currency="BTC", unit="mh*day"),
        )
        pool = PoolProfileInfo(
            priority=0,
            type="scrypt",
            host="pool.com",
            port="3333",
            user="worker",
            **{"pass": "pass"},
            status="active",
        )

        profile = Profile(id="123", name="My Profile", algo=algo, pools=[pool])

        assert profile.id == "123"
        assert profile.name == "My Profile"
        assert len(profile.pools) == 1
        assert profile.pools[0].priority == 0


class TestPoolTestResultItem:
    """Тесты для модели PoolTestResultItem."""

    def test_result_item_simple(self) -> None:
        """Тестирует простой результат теста."""
        item = PoolTestResultItem(
            source="us-central01.miningrigrentals.com",
            dest="de.minexmr.com:4444",
            error="none",
            connection=True,
            executiontime=0.12031352,
        )

        assert item.source == "us-central01.miningrigrentals.com"
        assert item.connection is True
        assert item.executiontime == 0.12031352

    def test_result_item_full(self) -> None:
        """Тестирует полный результат теста."""
        item = PoolTestResultItem(
            source="ca-tor01.miningrigrentals.com",
            dest="de.minexmr.com:4444",
            error="none",
            connection=True,
            executiontime=0.728852493,
            protocol="stratum",
            sub=True,
            auth=True,
            red=False,
            diffs=True,
            diff=2000.0,
            work=True,
            xnonce=False,
            ssl=False,
        )

        assert item.protocol == "stratum"
        assert item.auth is True
        assert item.diff == 2000.0


class TestPoolTestResult:
    """Тесты для модели PoolTestResult."""

    def test_result_valid(self) -> None:
        """Тестирует валидный результат теста."""
        item = PoolTestResultItem(
            source="us-central01",
            dest="pool.com:3333",
            error="none",
            connection=True,
            executiontime=0.1,
        )

        result = PoolTestResult(result=[item], error=[])

        assert len(result.result) == 1
        assert len(result.error) == 0


class TestAlgoPoolInfo:
    """Тесты для модели AlgoPoolInfo."""

    def test_algo_pool_info_valid(self) -> None:
        """Тестирует валидную информацию об алгоритме пула."""
        algo = AlgoPoolInfo(name="scrypt", display="Scrypt")

        assert algo.name == "scrypt"
        assert algo.display == "Scrypt"


class TestPool:
    """Тесты для модели Pool."""

    def test_pool_valid(self) -> None:
        """Тестирует валидный пул."""
        algo = AlgoPoolInfo(name="scrypt", display="Scrypt")
        data = {
            "id": 123,
            "type": "scrypt",
            "name": "My Pool",
            "host": "pool.minergate.com",
            "port": 3333,
            "user": "worker1",
            "pass": "secret",
            "notes": "Primary",
            "algo": algo,
        }
        pool = Pool.model_validate(data)

        assert pool.id == 123
        assert pool.name == "My Pool"
        assert pool.notes == "Primary"

    def test_pool_from_api(self) -> None:
        """Тестирует парсинг из ответа API с alias 'pass'."""
        api_data = {
            "id": 456,
            "type": "sha256",
            "name": "SHA Pool",
            "host": "pool.com",
            "port": 8080,
            "user": "worker",
            "pass": "password",
        }

        pool = Pool.model_validate(api_data)

        assert pool.id == 456
        assert pool.password == "password"


class TestPoolCreateResponse:
    """Тесты для модели PoolCreateResponse."""

    def test_response_valid(self) -> None:
        """Тестирует валидный ответ."""
        response = PoolCreateResponse(id=789)

        assert response.id == 789


class TestProfileCreateResponse:
    """Тесты для модели ProfileCreateResponse."""

    def test_response_valid(self) -> None:
        """Тестирует валидный ответ."""
        response = ProfileCreateResponse(pid="123")

        assert response.pid == "123"


class TestProfileDeleteResponse:
    """Тесты для модели ProfileDeleteResponse."""

    def test_response_success(self) -> None:
        """Тестирует успешный ответ."""
        response = ProfileDeleteResponse(id="123", success=True, message="Profile deleted")

        assert response.success is True
        assert response.message == "Profile deleted"

    def test_response_failure(self) -> None:
        """Тестирует неуспешный ответ."""
        response = ProfileDeleteResponse(id="456", success=False, message="Profile not found")

        assert response.success is False
        assert response.message == "Profile not found"


class TestCurrencyStatus:
    """Тесты для модели CurrencyStatus."""

    def test_currency_status_valid(self) -> None:
        """Тестирует валидный статус валюты."""
        status = CurrencyStatus(name="BTC", enabled=True)

        assert status.name == "BTC"
        assert status.enabled is True

    def test_currency_status_disabled(self) -> None:
        """Тестирует отключённую валюту."""
        status = CurrencyStatus(name="DOGE", enabled=False)

        assert status.enabled is False

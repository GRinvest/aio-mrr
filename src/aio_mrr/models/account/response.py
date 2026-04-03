"""Response models for Account API.

This module contains models for responses from the Account API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel

# --- Sub-models for AccountInfo ---


class WithdrawCurrencyInfo(BaseMRRModel):
    """Withdrawal information for a currency.

    Attributes:
        address: Withdrawal address.
        label: Address label.
        auto_pay_threshold: Auto-pay threshold.
        txfee: Transaction fee.
    """

    address: str
    label: str
    auto_pay_threshold: str
    txfee: float


class DepositCurrencyInfo(BaseMRRModel):
    """Deposit information for a currency.

    Attributes:
        address: Deposit address.
    """

    address: str


class NotificationsInfo(BaseMRRModel):
    """Notification information.

    Attributes:
        rental_comm: Rental communication notifications.
        new_rental: New rental notifications.
        offline: Offline notifications.
        news: News notifications.
        deposit: Deposit notifications.
    """

    rental_comm: str
    new_rental: str
    offline: str
    news: str
    deposit: str


class SettingsInfo(BaseMRRModel):
    """Account settings information.

    Attributes:
        live_data: Real-time data.
        public_profile: Public profile.
        two_factor_auth: Two-factor authentication.
    """

    model_config = ConfigDict(populate_by_name=True)

    live_data: str
    public_profile: str
    two_factor_auth: str

    def __init__(self, **data: str) -> None:
        # Map '2factor_auth' from API to 'two_factor_auth'
        if "2factor_auth" in data and "two_factor_auth" not in data:
            data["two_factor_auth"] = data.pop("2factor_auth")
        super().__init__(**data)


# --- Main models ---


class AccountInfo(BaseMRRModel):
    """Account information.

    Response for GET /account.

    Attributes:
        username: Username.
        email: User email.
        withdraw: Withdrawal information by currency.
        deposit: Deposit information by currency.
        notifications: Notification information.
        settings: Settings information.
    """

    username: str
    email: str
    withdraw: dict[str, WithdrawCurrencyInfo]
    deposit: dict[str, DepositCurrencyInfo]
    notifications: NotificationsInfo
    settings: SettingsInfo


class BalanceInfo(BaseMRRModel):
    """Balance information.

    Used for GET /account/balance response.
    Returned as Dict[str, BalanceInfo] by currency.

    Attributes:
        confirmed: Confirmed balance.
        pending: Pending balance.
        unconfirmed: Unconfirmed balance.
    """

    confirmed: str
    pending: float = 0
    unconfirmed: str


class Transaction(BaseMRRModel):
    """Transaction information.

    Used for GET /account/transactions response.

    Attributes:
        id: Transaction identifier.
        type: Transaction type.
        currency: Transaction currency.
        amount: Amount (negative for debits).
        when: Transaction time (UTC).
        rental: Rental ID (if applicable).
        rig: Rig ID (if applicable).
        txid: Blockchain transaction ID (for Payout/Deposit).
        txfee: Fee (only for Payout).
        payout_address: Payout address (only for Payout).
        sent: Send status (only for Payout).
        status: Transaction status (Cleared or Pending).
        pending_seconds: Seconds waiting (if Pending).
        info: Additional information.
    """

    id: str
    type: str
    currency: str | None = None  # Optional field — documentation is contradictory
    amount: str | float
    when: str
    rental: str | None = None
    rig: str | None = None
    txid: str | None = None
    txfee: str | float | None = None
    payout_address: str | None = None
    sent: str | None = None
    status: str
    pending_seconds: int | None = None
    info: str | None = None


class TransactionsList(BaseMRRModel):
    """List of transactions.

    Response for GET /account/transactions.

    Attributes:
        total: Total number of transactions.
        returned: Number of returned transactions.
        start: Pagination start.
        limit: Record limit.
        transactions: List of transactions.
    """

    total: str
    returned: int
    start: int
    limit: int
    transactions: list[Transaction]


# --- Sub-models for Profile ---


class PriceInfo(BaseMRRModel):
    """Price information.

    Attributes:
        amount: Price value.
        currency: Currency.
        unit: Unit of measurement.
    """

    amount: str
    currency: str
    unit: str


class AlgoProfileInfo(BaseMRRModel):
    """Profile algorithm information.

    Attributes:
        name: Algorithm name.
        display: Display name.
        suggested_price: Suggested price.
    """

    name: str
    display: str
    suggested_price: PriceInfo


class PoolProfileInfo(BaseMRRModel):
    """Pool information in a profile.

    Attributes:
        priority: Pool priority (0-4).
        type: Pool type/algorithm.
        host: Pool host.
        port: Pool port.
        user: Username.
        password: Password (called 'pass' in API).
        status: Pool status.
    """

    model_config = ConfigDict(populate_by_name=True)

    priority: int
    type: str
    host: str
    port: str
    user: str
    password: str = Field(..., alias="pass")
    status: str


class Profile(BaseMRRModel):
    """Pool profile.

    Used for responses:
    - GET /account/profile
    - GET /account/profile/{id}

    Attributes:
        id: Profile identifier.
        name: Profile name.
        algo: Algorithm information.
        pools: List of profile pools.
    """

    id: str
    name: str
    algo: AlgoProfileInfo
    pools: list[PoolProfileInfo] | None = None


# --- Sub-models for PoolTestResult ---


class PoolTestResultItem(BaseMRRModel):
    """Pool connection test result.

    Attributes:
        source: MRR server from which the test was conducted.
        dest: Target pool host:port.
        error: Connection error (or "none").
        connection: true if connection successful.
        executiontime: Test execution time in seconds.
        protocol: Protocol (full test only).
        sub: true if subscription successful (full test only).
        auth: true if authorization accepted (full test only).
        red: true if pool sends reconnect (full test only).
        diffs: true if pool set difficulty (full test only).
        diff: Difficulty value (full test only).
        work: true if work received (full test only).
        xnonce: true if pool accepts extranonce (full test only).
        ssl: true if SSL/TLS (full test only).
    """

    source: str
    dest: str
    error: str
    connection: bool
    executiontime: float
    protocol: str | None = None
    sub: bool | None = None
    auth: bool | None = None
    red: bool | None = None
    diffs: bool | None = None
    diff: float | None = None
    work: bool | None = None
    xnonce: bool | None = None
    ssl: bool | None = None


class PoolTestResult(BaseMRRModel):
    """Pool test result.

    Response for PUT /account/pool/test.

    Attributes:
        result: List of connection test results.
        error: List of errors (usually empty).
    """

    result: list[PoolTestResultItem]
    error: list[str]


# --- Sub-models for Pool ---


class AlgoPoolInfo(BaseMRRModel):
    """Pool algorithm information.

    Attributes:
        name: Algorithm name.
        display: Display name.
    """

    name: str
    display: str


class Pool(BaseMRRModel):
    """Pool information.

    Used for responses:
    - GET /account/pool
    - GET /account/pool/{ids}
    - GET /rig/{ids}/pool

    Attributes:
        id: Pool identifier.
        type: Pool type/algorithm.
        name: Pool name.
        host: Pool host.
        port: Pool port.
        user: Username.
        password: Password (called 'pass' in API).
        notes: Notes.
        algo: Algorithm information.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: int
    type: str
    name: str
    host: str
    port: int
    user: str
    password: str = Field(..., alias="pass")
    notes: str | None = None
    algo: AlgoPoolInfo | None = None


class PoolCreateResponse(BaseMRRModel):
    """Pool creation response.

    Response for PUT /account/pool.

    Attributes:
        id: Created pool ID.
    """

    id: int


# --- Sub-models for ProfileCreateResponse ---


class ProfileCreateResponse(BaseMRRModel):
    """Profile creation response.

    Response for PUT /account/profile.

    Attributes:
        pid: Created profile ID.
    """

    pid: str


# --- Sub-models for ProfileDeleteResponse ---


class ProfileDeleteResponse(BaseMRRModel):
    """Profile deletion response.

    Response for DELETE /account/profile/{id}.

    Attributes:
        id: Deleted profile ID.
        success: Deletion success.
        message: Result message.
    """

    id: str
    success: bool
    message: str


# --- CurrencyStatus ---


class CurrencyStatus(BaseMRRModel):
    """Currency status for account.

    Used for GET /account/currencies response.

    Attributes:
        name: Currency name (e.g., "BTC", "LTC").
        enabled: Flag indicating currency availability for payments.
    """

    name: str
    enabled: bool

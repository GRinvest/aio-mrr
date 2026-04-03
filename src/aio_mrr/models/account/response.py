"""Response модели для Account API.

Этот модуль содержит модели для ответов от Account API.
"""

from pydantic import ConfigDict, Field

from aio_mrr.models.base import BaseMRRModel

# --- Sub-models для AccountInfo ---


class WithdrawCurrencyInfo(BaseMRRModel):
    """Информация о выводе средств для валюты.

    Attributes:
        address: Адрес для вывода.
        label: Метка адреса.
        auto_pay_threshold: Порог автоматической выплаты.
        txfee: Комиссия за транзакцию.
    """

    address: str
    label: str
    auto_pay_threshold: str
    txfee: float


class DepositCurrencyInfo(BaseMRRModel):
    """Информация о депозите для валюты.

    Attributes:
        address: Адрес для депозита.
    """

    address: str


class NotificationsInfo(BaseMRRModel):
    """Информация о уведомлениях.

    Attributes:
        rental_comm: Уведомления об аренде.
        new_rental: Уведомления о новой аренде.
        offline: Уведомления об оффлайне.
        news: Уведомления о новостях.
        deposit: Уведомления о депозитах.
    """

    rental_comm: str
    new_rental: str
    offline: str
    news: str
    deposit: str


class SettingsInfo(BaseMRRModel):
    """Информация о настройках аккаунта.

    Attributes:
        live_data: Данные в реальном времени.
        public_profile: Публичный профиль.
        two_factor_auth: Двухфакторная аутентификация.
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


# --- Основные модели ---


class AccountInfo(BaseMRRModel):
    """Информация об аккаунте.

    Ответ для GET /account.

    Attributes:
        username: Имя пользователя.
        email: Email пользователя.
        withdraw: Информация о выводе средств по валютам.
        deposit: Информация о депозитах по валютам.
        notifications: Информация об уведомлениях.
        settings: Информация о настройках.
    """

    username: str
    email: str
    withdraw: dict[str, WithdrawCurrencyInfo]
    deposit: dict[str, DepositCurrencyInfo]
    notifications: NotificationsInfo
    settings: SettingsInfo


class BalanceInfo(BaseMRRModel):
    """Информация о балансе.

    Используется для ответа GET /account/balance.
    Возвращается как Dict[str, BalanceInfo] по валютам.

    Attributes:
        confirmed: Подтверждённый баланс.
        pending: Ожидающий баланс.
        unconfirmed: неподтверждённый баланс.
    """

    confirmed: str
    pending: float
    unconfirmed: str


class Transaction(BaseMRRModel):
    """Информация о транзакции.

    Используется для ответа GET /account/transactions.

    Attributes:
        id: Идентификатор транзакции.
        type: Тип транзакции.
        currency: Валюта транзакции.
        amount: Сумма (отрицательная для списаний).
        when: Время транзакции (UTC).
        rental: ID аренды (если применимо).
        rig: ID рига (если применимо).
        txid: ID транзакции в блокчейне (для Payout/Deposit).
        txfee: Комиссия (только для Payout).
        payout_address: Адрес выплаты (только для Payout).
        sent: Статус отправки (только для Payout).
        status: Статус транзакции (Cleared или Pending).
        pending_seconds: Секунды ожидания (если Pending).
        info: Дополнительная информация.
    """

    id: str
    type: str
    currency: str | None = None  # Опциональное поле — документация противоречива
    amount: str
    when: str
    rental: str | None = None
    rig: str | None = None
    txid: str | None = None
    txfee: str | None = None
    payout_address: str | None = None
    sent: str | None = None
    status: str
    pending_seconds: int | None = None
    info: str | None = None


class TransactionsList(BaseMRRModel):
    """Список транзакций.

    Ответ для GET /account/transactions.

    Attributes:
        total: Общее количество транзакций.
        returned: Количество возвращённых транзакций.
        start: Старт пагинации.
        limit: Лимит записей.
        transactions: Список транзакций.
    """

    total: str
    returned: int
    start: int
    limit: int
    transactions: list[Transaction]


# --- Sub-models для Profile ---


class PriceInfo(BaseMRRModel):
    """Информация о цене.

    Attributes:
        amount: Значение цены.
        currency: Валюта.
        unit: Единица измерения.
    """

    amount: str
    currency: str
    unit: str


class AlgoProfileInfo(BaseMRRModel):
    """Информация об алгоритме профиля.

    Attributes:
        name: Название алгоритма.
        display: Отображаемое название.
        suggested_price: Рекомендуемая цена.
    """

    name: str
    display: str
    suggested_price: PriceInfo


class PoolProfileInfo(BaseMRRModel):
    """Информация о пуле в профиле.

    Attributes:
        priority: Приоритет пула (0-4).
        type: Тип/алгоритм пула.
        host: Хост пула.
        port: Порт пула.
        user: Имя пользователя.
        password: Пароль (в API называется 'pass').
        status: Статус пула.
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
    """Профиль пула.

    Используется для ответов:
    - GET /account/profile
    - GET /account/profile/{id}

    Attributes:
        id: Идентификатор профиля.
        name: Название профиля.
        algo: Информация об алгоритме.
        pools: Список пулов профиля.
    """

    id: str
    name: str
    algo: AlgoProfileInfo
    pools: list[PoolProfileInfo]


# --- Sub-models для PoolTestResult ---


class PoolTestResultItem(BaseMRRModel):
    """Результат теста подключения к пулу.

    Attributes:
        source: Сервер MRR, с которого проводился тест.
        dest: Целевой хост:порт пула.
        error: Ошибка подключения (или "none").
        connection: true если подключение успешно.
        executiontime: Время выполнения теста в секундах.
        protocol: Протокол (только для full теста).
        sub: true если подписка успешна (только для full теста).
        auth: true если авторизация принята (только для full теста).
        red: true если пул отправляет reconnect (только для full теста).
        diffs: true если пул установил сложность (только для full теста).
        diff: Значение сложности (только для full теста).
        work: true если получена работа (только для full теста).
        xnonce: true если пул принимает extranonce (только для full теста).
        ssl: true если SSL/TLS (только для full теста).
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
    """Результат теста пула.

    Ответ для PUT /account/pool/test.

    Attributes:
        result: Список результатов тестов подключения.
        error: Список ошибок (обычно пустой).
    """

    result: list[PoolTestResultItem]
    error: list[str]


# --- Sub-models для Pool ---


class AlgoPoolInfo(BaseMRRModel):
    """Информация об алгоритме пула.

    Attributes:
        name: Название алгоритма.
        display: Отображаемое название.
    """

    name: str
    display: str


class Pool(BaseMRRModel):
    """Информация о пуле.

    Используется для ответов:
    - GET /account/pool
    - GET /account/pool/{ids}
    - GET /rig/{ids}/pool

    Attributes:
        id: Идентификатор пула.
        type: Тип/алгоритм пула.
        name: Название пула.
        host: Хост пула.
        port: Порт пула.
        user: Имя пользователя.
        password: Пароль (в API называется 'pass').
        notes: Заметки.
        algo: Информация об алгоритме.
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
    """Ответ на создание пула.

    Ответ для PUT /account/pool.

    Attributes:
        id: ID созданного пула.
    """

    id: int


# --- Sub-models для ProfileCreateResponse ---


class ProfileCreateResponse(BaseMRRModel):
    """Ответ на создание профиля.

    Ответ для PUT /account/profile.

    Attributes:
        pid: ID созданного профиля.
    """

    pid: str


# --- Sub-models для ProfileDeleteResponse ---


class ProfileDeleteResponse(BaseMRRModel):
    """Ответ на удаление профиля.

    Ответ для DELETE /account/profile/{id}.

    Attributes:
        id: ID удалённого профиля.
        success: Успешность удаления.
        message: Сообщение о результате.
    """

    id: str
    success: bool
    message: str


# --- CurrencyStatus ---


class CurrencyStatus(BaseMRRModel):
    """Статус валюты для аккаунта.

    Используется для ответа GET /account/currencies.

    Attributes:
        name: Название валюты (например, "BTC", "LTC").
        enabled: Флаг доступности валюты для платежей.
    """

    name: str
    enabled: bool

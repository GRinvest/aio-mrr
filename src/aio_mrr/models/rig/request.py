"""Request модели для Rig API.

Этот модуль содержит модели для query параметров и body запросов к Rig API.
"""

from pydantic import Field

from aio_mrr.models.base import BaseMRRModel


class RigSearchParams(BaseMRRModel):
    """Query параметры для GET /rig.

    Используется для поиска rig'ов по алгоритму с фильтрацией и сортировкой.

    Attributes:
        currency: Валюта: [BTC,LTC,ETH,DOGE,BCH]. По умолчанию BTC.
        type: Алгоритм: sha256, scrypt, x11 и т.д. (обязательное).
        minhours_min: Минимальное количество часов.
        minhours_max: Максимальное количество часов.
        maxhours_min: Минимальное максимальное время.
        maxhours_max: Максимальное максимальное время.
        rpi_min: Минимальный RPI (0-100).
        rpi_max: Максимальный RPI (0-100).
        hash_min: Минимальный хешрейт.
        hash_max: Максимальный хешрейт.
        hash_type: Тип: [hash,kh,mh,gh,th,ph,eh]. По умолчанию mh.
        price_min: Минимальная цена.
        price_max: Максимальная цена.
        price_type: Тип хеша для цены.
        offline: Показывать оффлайн rig'и. По умолчанию false.
        rented: Показывать арендованные. По умолчанию false.
        region_type: 'include' или 'exclude'.
        expdiff: Ожидаемая сложность worker.
        count: Количество результатов (макс. 100). По умолчанию 100.
        islive: Фильтр по rig'ам с хешрейтом [yes].
        xnonce: Фильтр по xnonce [yes,no].
        offset: Смещение пагинации. По умолчанию 0.
        orderby: Сортировка. По умолчанию score.
        orderdir: Направление [asc,desc]. По умолчанию asc.
    """

    currency: str | None = Field(default=None, description="Валюта: [BTC,LTC,ETH,DOGE,BCH]")
    type: str = Field(..., description="Алгоритм: sha256, scrypt, x11 и т.д.")
    minhours_min: int | None = Field(default=None, alias="minhours.min", description="Минимальное количество часов")
    minhours_max: int | None = Field(default=None, alias="minhours.max", description="Максимальное количество часов")
    maxhours_min: int | None = Field(default=None, alias="maxhours.min", description="Минимальное максимальное время")
    maxhours_max: int | None = Field(default=None, alias="maxhours.max", description="Максимальное максимальное время")
    rpi_min: int | None = Field(default=None, alias="rpi.min", description="Минимальный RPI (0-100)")
    rpi_max: int | None = Field(default=None, alias="rpi.max", description="Максимальный RPI (0-100)")
    hash_min: int | None = Field(default=None, alias="hash.min", description="Минимальный хешрейт")
    hash_max: int | None = Field(default=None, alias="hash.max", description="Максимальный хешрейт")
    hash_type: str | None = Field(default=None, alias="hash.type", description="Тип: [hash,kh,mh,gh,th,ph,eh]")
    price_min: float | None = Field(default=None, alias="price.min", description="Минимальная цена")
    price_max: float | None = Field(default=None, alias="price.max", description="Максимальная цена")
    price_type: str | None = Field(default=None, alias="price.type", description="Тип хеша для цены")
    offline: bool | None = Field(default=None, description="Показывать оффлайн rig'и")
    rented: bool | None = Field(default=None, description="Показывать арендованные")
    region_type: str | None = Field(default=None, alias="region.type", description="'include' или 'exclude'")
    expdiff: float | None = Field(default=None, description="Ожидаемая сложность worker")
    count: int | None = Field(default=None, description="Количество результатов (макс. 100)")
    islive: str | None = Field(default=None, description="Filter for rigs with hashrate [yes]")
    xnonce: str | None = Field(default=None, description="Фильтр по xnonce [yes,no]")
    offset: int | None = Field(default=None, description="Смещение пагинации")
    orderby: str | None = Field(default=None, description="Сортировка")
    orderdir: str | None = Field(default=None, description="Направление [asc,desc]")


class RigCreateBody(BaseMRRModel):
    """Body запроса для PUT /rig.

    Используется для создания нового rig.

    Attributes:
        name: Название rig (обязательное).
        description: Описание rig.
        status: 'enabled' или 'disabled'.
        server: Имя сервера (обязательное, см. /info/servers).
        price_btc_enabled: Включить BTC ценообразование. По умолчанию true.
        price_btc_price: Цена rig в день (BTC).
        price_btc_autoprice: Включить автоценообразование.
        price_btc_minimum: Минимальная цена автоценообразователя.
        price_btc_modifier: Процент +/- для автоценообразования.
        price_ltc_enabled: Включить LTC ценообразование. По умолчанию true.
        price_eth_enabled: Включить ETH ценообразование. По умолчанию true.
        price_doge_enabled: Включить DOGE ценообразование. По умолчанию true.
        price_type: Тип хеша: [hash,kh,mh,gh,th,ph,eh]. По умолчанию mh.
        minhours: Минимальное количество часов.
        maxhours: Максимальное количество часов.
        extensions: Разрешить продление аренды. По умолчанию true.
        hash_hash: Рекламный хешрейт.
        hash_type: Тип хеша. По умолчанию mh.
        suggested_diff: Рекомендуемая сложность.
        ndevices: Количество устройств (workers).
    """

    name: str = Field(..., description="Название rig")
    description: str | None = Field(default=None, description="Описание")
    status: str | None = Field(default=None, description="'enabled' или 'disabled'")
    server: str = Field(..., description="Имя сервера")
    price_btc_enabled: bool | None = Field(
        default=None, alias="price.btc.enabled", description="Включить BTC ценообразование"
    )
    price_btc_price: float | None = Field(default=None, alias="price.btc.price", description="Цена rig в день (BTC)")
    price_btc_autoprice: bool | None = Field(
        default=None, alias="price.btc.autoprice", description="Включить автоценообразование"
    )
    price_btc_minimum: float | None = Field(
        default=None, alias="price.btc.minimum", description="Минимальная цена автоценообразователя"
    )
    price_btc_modifier: str | None = Field(
        default=None, alias="price.btc.modifier", description="Процент +/- для автоценообразования"
    )
    price_ltc_enabled: bool | None = Field(
        default=None, alias="price.ltc.enabled", description="Включить LTC ценообразование"
    )
    price_eth_enabled: bool | None = Field(
        default=None, alias="price.eth.enabled", description="Включить ETH ценообразование"
    )
    price_doge_enabled: bool | None = Field(
        default=None, alias="price.doge.enabled", description="Включить DOGE ценообразование"
    )
    price_type: str | None = Field(default=None, alias="price.type", description="Тип хеша: [hash,kh,mh,gh,th,ph,eh]")
    minhours: float | None = Field(default=None, description="Минимальное количество часов")
    maxhours: float | None = Field(default=None, description="Максимальное количество часов")
    extensions: bool | None = Field(default=None, description="Разрешить продление аренды")
    hash_hash: float | None = Field(default=None, alias="hash.hash", description="Рекламный хешрейт")
    hash_type: str | None = Field(default=None, alias="hash.type", description="Тип хеша")
    suggested_diff: float | None = Field(default=None, description="Рекомендуемая сложность")
    ndevices: int | None = Field(default=None, description="Количество устройств (workers)")


class RigBatchBody(BaseMRRModel):
    """Body запроса для POST /rig/batch.

    Используется для пакетного обновления rig'ов.

    Attributes:
        rigs: Список rig'ов для обновления с полями id, name, status и т.д.
    """

    rigs: list[dict[str, object]] = Field(..., description="Список rig'ов для обновления")


class RigExtendBody(BaseMRRModel):
    """Body запроса для PUT /rig/{ids}/extend.

    Используется для продления аренды rig'а (для владельцев).

    Attributes:
        hours: Часы для продления.
        minutes: Минуты для продления.
    """

    hours: float | None = Field(default=None, description="Часы для продления")
    minutes: float | None = Field(default=None, description="Минуты для продления")


class RigPoolBody(BaseMRRModel):
    """Body запроса для PUT /rig/{ids}/pool.

    Используется для добавления или замены пула на rig'ах.

    Attributes:
        host: Хост пула (обязательное).
        port: Порт пула (обязательное).
        user: Имя worker (обязательное).
        pass: Пароль worker (обязательное).
        priority: Приоритет (0-4).
    """

    host: str = Field(..., description="Хост пула")
    port: int = Field(..., description="Порт пула")
    user: str = Field(..., description="Имя worker")
    password: str = Field(..., alias="pass", description="Пароль worker")
    priority: int | None = Field(default=None, description="Приоритет (0-4)")

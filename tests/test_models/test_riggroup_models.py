"""Тесты для моделей RigGroup API."""

from __future__ import annotations

from aio_mrr.models.riggroup.request import RigGroupCreateBody, RigGroupUpdateBody
from aio_mrr.models.riggroup.response import RigGroupInfo, RigGroupList


class TestRigGroupCreateBody:
    """Тесты для модели RigGroupCreateBody."""

    def test_create_body_minimal(self) -> None:
        """Тестирует минимальное тело запроса."""
        body = RigGroupCreateBody(name="My Group")

        assert body.name == "My Group"
        assert body.enabled is True
        assert body.rental_limit == 1

    def test_create_body_full(self) -> None:
        """Тестирует полное тело запроса."""
        body = RigGroupCreateBody(
            name="My Group",
            enabled=False,
            rental_limit=5,
        )

        assert body.enabled is False
        assert body.rental_limit == 5

    def test_create_body_explicit_defaults(self) -> None:
        """Тестирует явное задание значений по умолчанию."""
        body = RigGroupCreateBody(
            name="Default Group",
            enabled=True,
            rental_limit=1,
        )

        assert body.enabled is True
        assert body.rental_limit == 1


class TestRigGroupUpdateBody:
    """Тесты для модели RigGroupUpdateBody."""

    def test_update_body_empty(self) -> None:
        """Тестирует пустое тело запроса (все поля опциональные)."""
        body = RigGroupUpdateBody()

        assert body.name is None
        assert body.enabled is None
        assert body.rental_limit is None

    def test_update_body_name_only(self) -> None:
        """Тестирует обновление только названия."""
        body = RigGroupUpdateBody(name="New Name")

        assert body.name == "New Name"
        assert body.enabled is None
        assert body.rental_limit is None

    def test_update_body_full(self) -> None:
        """Тестирует полное обновление."""
        body = RigGroupUpdateBody(
            name="Updated Group",
            enabled=False,
            rental_limit=10,
        )

        assert body.name == "Updated Group"
        assert body.enabled is False
        assert body.rental_limit == 10


class TestRigGroupInfo:
    """Тесты для модели RigGroupInfo."""

    def test_group_info_minimal(self) -> None:
        """Тестирует минимальную информацию о группе."""
        group = RigGroupInfo(
            id="group123",
            name="My Group",
            enabled=True,
            rental_limit=1,
            rigs=[12345, 12346],
        )

        assert group.id == "group123"
        assert group.name == "My Group"
        assert group.enabled is True
        assert group.rental_limit == 1
        assert group.rigs == [12345, 12346]
        assert group.algo is None

    def test_group_info_full(self) -> None:
        """Тестирует полную информацию о группе."""
        group = RigGroupInfo(
            id="group456",
            name="Scrypt Group",
            enabled=True,
            rental_limit=5,
            rigs=[11111, 22222, 33333],
            algo="scrypt",
        )

        assert group.algo == "scrypt"
        assert len(group.rigs) == 3

    def test_group_info_from_api(self) -> None:
        """Тестирует парсинг из ответа API."""
        api_data = {
            "id": "api_group",
            "name": "API Group",
            "enabled": True,
            "rental_limit": 3,
            "rigs": [100, 200, 300, 400],
            "algo": "sha256",
        }

        group = RigGroupInfo.model_validate(api_data)

        assert group.id == "api_group"
        assert group.algo == "sha256"
        assert len(group.rigs) == 4


class TestRigGroupList:
    """Тесты для модели RigGroupList."""

    def test_group_list_valid(self) -> None:
        """Тестирует валидный список групп."""
        group1 = RigGroupInfo(
            id="group1",
            name="Group 1",
            enabled=True,
            rental_limit=1,
            rigs=[12345],
        )
        group2 = RigGroupInfo(
            id="group2",
            name="Group 2",
            enabled=False,
            rental_limit=5,
            rigs=[12346, 12347],
            algo="scrypt",
        )

        group_list = RigGroupList(groups=[group1, group2])

        assert len(group_list.groups) == 2
        assert group_list.groups[0].id == "group1"
        assert group_list.groups[1].algo == "scrypt"

    def test_group_list_empty(self) -> None:
        """Тестирует пустой список групп."""
        group_list = RigGroupList(groups=[])

        assert len(group_list.groups) == 0

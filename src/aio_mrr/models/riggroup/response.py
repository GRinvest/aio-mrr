"""Response models for RigGroup API.

This module contains models for responses from the RigGroup API:
- RigGroupInfo — rig group information
- RigGroupList — list of rig groups
"""

from aio_mrr.models.base import BaseMRRModel


class RigGroupInfo(BaseMRRModel):
    """Rig group information.

    Used for responses:
    - GET /riggroup (in list)
    - GET /riggroup/{id} (single group)

    Attributes:
        id: Group identifier.
        name: Group name.
        enabled: Group enabled flag.
        rental_limit: Maximum active rentals.
        rigs: List of rig IDs in the group.
        algo: Mining algorithm of the group (optional).
    """

    id: str
    name: str
    enabled: bool
    rental_limit: int
    rigs: list[int]
    algo: str | None = None


class RigGroupList(BaseMRRModel):
    """List of rig groups.

    Response for GET /riggroup.

    Attributes:
        groups: List of rig group information.
    """

    groups: list[RigGroupInfo]

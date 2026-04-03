"""Request models for RigGroup API.

This module contains models for request data of the RigGroup API:
- RigGroupCreateBody — request body for PUT /riggroup
- RigGroupUpdateBody — request body for PUT /riggroup/{id}
"""

from pydantic import Field

from aio_mrr.models.base import BaseMRRModel


class RigGroupCreateBody(BaseMRRModel):
    """Request body for creating a new rig group (PUT /riggroup).

    Attributes:
        name: Group name. Required field.
        enabled: Group enabled flag. Default True.
        rental_limit: Maximum active rentals. Default 1.
    """

    name: str = Field(..., description="Group name")
    enabled: bool = Field(default=True, description="Group enabled/disabled")
    rental_limit: int = Field(default=1, description="Maximum active rentals")


class RigGroupUpdateBody(BaseMRRModel):
    """Request body for updating a rig group (PUT /riggroup/{id}).

    All fields are optional — you can update only the fields you need.

    Attributes:
        name: New group name (optional).
        enabled: New enabled status (optional).
        rental_limit: New rental limit (optional).
    """

    name: str | None = Field(default=None, description="New group name")
    enabled: bool | None = Field(default=None, description="New enabled status")
    rental_limit: int | None = Field(default=None, description="New rental limit")

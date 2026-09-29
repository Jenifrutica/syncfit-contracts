"""Gym membership and joined-gym models.

These describe the athlete side of gyms. A ``GymMembership`` links a profile to
a gym; a ``JoinedGym`` is the resolved view returned to the client, where the
machines are read live from the admin's inventory. ``GymStation`` is a machine
added by a gym admin and is distinct from the shared catalog ``GymMachine``.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .common import BaseContractModel, LocalizedText


class GymStation(BaseContractModel):
    """A machine added by a gym admin (not the shared catalog).

    ``name`` and ``purpose`` are localized: the admin may type in any language
    and the backend fills the other locales (AI-assisted, with a fallback).
    ``exercise_ids`` are the catalog exercises the machine covers.
    """

    id: str
    gym_id: str
    name: LocalizedText
    weight_factor: float = Field(ge=0)
    purpose: LocalizedText | None = None
    exercise_ids: list[str] = Field(default_factory=list)
    equipment_key: str | None = None
    equipment_type: str | None = None
    image_url: str | None = None


class GymMembership(BaseContractModel):
    """One row per (profile, gym) membership."""

    profile_id: str
    gym_id: str
    created_at: datetime | None = None


class JoinedGym(BaseContractModel):
    """A joined gym with its machines resolved live."""

    gym_id: str
    name: str
    code: str
    active: bool = False
    joined_at: datetime | None = None
    machines: list[GymStation] = Field(default_factory=list)


__all__ = ["GymMembership", "GymStation", "JoinedGym"]

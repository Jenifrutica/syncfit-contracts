"""Gym machine catalog models."""

from __future__ import annotations

from pydantic import Field

from .common import BaseContractModel, EquipmentType, LocalizedText


class GymMachine(BaseContractModel):
    """A gym machine or station with its weight factor.

    The same movement loads differently across machines, so `weight_factor`
    scales the free-weight estimate to suggest a machine load.
    """

    id: str
    name: LocalizedText
    type: EquipmentType
    exercises: list[str] = Field(default_factory=list)
    weight_factor: float = Field(ge=0)
    unit: str | None = None
    notes: LocalizedText
    image_url: str | None = None


__all__ = ["GymMachine"]

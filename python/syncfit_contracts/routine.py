"""Structured, adapted training prescription delivered to the frontend."""

from __future__ import annotations

from pydantic import Field

from .common import BaseContractModel, ExerciseAdaptation, FatigueLevel, InferredPhase
from .version import SCHEMA_VERSION


class AdaptedRoutine(BaseContractModel):
    """Adapted routine produced by the reasoning layer."""

    schema_version: str = SCHEMA_VERSION
    session_id: str
    phase_inferred: InferredPhase
    fatigue_level: FatigueLevel
    k_load_multiplier: float = Field(ge=0.70, le=1.05)
    alerts: list[str] = Field(default_factory=list)
    adapted_routine: list[ExerciseAdaptation] = Field(default_factory=list)


__all__ = ["AdaptedRoutine"]

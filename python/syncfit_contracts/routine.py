"""Structured, adapted training prescription delivered to the frontend."""

from __future__ import annotations

from pydantic import Field

from .common import (
    BaseContractModel,
    EnergyLevel,
    ExerciseAdaptation,
    FatigueLevel,
    InferredPhase,
    Language,
    Modality,
    MuscleGroup,
    UserObjective,
)
from .telemetry import TelemetryFrame
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


class RoutineRequest(BaseContractModel):
    """Request to generate a routine for one or more muscle groups."""

    schema_version: str = SCHEMA_VERSION
    session_id: str | None = None
    muscle_groups: list[MuscleGroup] = Field(min_length=1, max_length=4)
    language: Language = Language.EN
    symptoms: list[str] = Field(default_factory=list)
    modality: Modality | None = None
    day_or_week: int | None = Field(default=None, ge=1, le=42)
    telemetry: TelemetryFrame | None = None
    exercises_per_group: int | None = Field(default=None, ge=1, le=8)
    exercises_count: int | None = Field(default=None, ge=1, le=12)
    time_budget_minutes: int | None = Field(default=None, ge=10, le=180)
    energy_level: EnergyLevel | None = None
    objective: UserObjective | None = None
    include_warmup: bool = True


class RoutineResponse(BaseContractModel):
    """Adapted routine for the selected muscle groups."""

    schema_version: str = SCHEMA_VERSION
    session_id: str | None = None
    language: Language = Language.EN
    muscle_groups: list[MuscleGroup] = Field(min_length=1)
    phase_inferred: InferredPhase | None = None
    fatigue_level: FatigueLevel | None = None
    k_load_multiplier: float | None = Field(default=None, ge=0.70, le=1.05)
    alerts: list[str] = Field(default_factory=list)
    total_estimated_minutes: float | None = Field(default=None, ge=0)
    warmup: list[ExerciseAdaptation] = Field(default_factory=list)
    routine: list[ExerciseAdaptation] = Field(default_factory=list)


__all__ = ["AdaptedRoutine", "RoutineRequest", "RoutineResponse"]


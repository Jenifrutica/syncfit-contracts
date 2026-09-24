"""User profile, baseline loads and energy check-ins."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .common import (
    BaseContractModel,
    EnergyLevel,
    ExerciseLoad,
    GoalPhase,
    Language,
    MacroNutrients,
    Modality,
    UserObjective,
)
from .version import SCHEMA_VERSION


class SupplementMacro(BaseContractModel):
    """User-entered nutrition facts for a current supplement."""

    supplement_id: str
    macros: MacroNutrients


class UserProfile(BaseContractModel):
    """Athlete profile: guests use ephemeral profiles, users keep history."""

    schema_version: str = SCHEMA_VERSION
    profile_id: str
    display_name: str = Field(min_length=1)
    language: Language = Language.EN
    is_guest: bool = False
    height_cm: float | None = Field(default=None, ge=80, le=250)
    weight_kg: float | None = Field(default=None, ge=20, le=300)
    body_fat_pct: float | None = Field(default=None, ge=3, le=60)
    daily_calories: int | None = Field(default=None, ge=800, le=6000)
    age: int | None = Field(default=None, ge=10, le=100)
    objective: UserObjective | None = None
    goal_phase: GoalPhase | None = None
    modality: Modality | None = None
    available_machines: list[str] = Field(default_factory=list)
    current_supplements: list[str] = Field(default_factory=list)
    supplement_macros: list[SupplementMacro] = Field(default_factory=list)
    weight_unit: str | None = None
    photo_url: str | None = None
    weekly_training_goal: int | None = Field(default=None, ge=1, le=7)
    rest_days_allowance: int | None = Field(default=None, ge=0, le=7)
    loads: list[ExerciseLoad] = Field(default_factory=list)


class EnergyCheckIn(BaseContractModel):
    """Subjective energy reported before training."""

    schema_version: str = SCHEMA_VERSION
    profile_id: str | None = None
    session_id: str | None = None
    timestamp: datetime
    energy_level: EnergyLevel
    modality: Modality
    day_or_week: int | None = Field(default=None, ge=1, le=42)
    notes: str | None = None


__all__ = ["UserProfile", "EnergyCheckIn", "SupplementMacro"]

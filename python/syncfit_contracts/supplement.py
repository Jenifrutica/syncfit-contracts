"""Supplement catalog models and advice."""

from __future__ import annotations

from pydantic import Field

from .common import (
    BaseContractModel,
    GoalPhase,
    Language,
    LocalizedText,
    MacroNutrients,
    Modality,
    SupplementCategory,
    SupplementFrequency,
    SupplementSafety,
    UserObjective,
)
from .version import SCHEMA_VERSION


class Supplement(BaseContractModel):
    """Catalog entry for a supplement with context-dependent safety."""

    id: str
    name: LocalizedText
    category: SupplementCategory
    dosage: LocalizedText
    macros: MacroNutrients
    objectives: list[UserObjective] = Field(default_factory=list)
    safety_general: SupplementSafety
    safety_pregnancy: SupplementSafety
    notes: LocalizedText
    frequency: SupplementFrequency | None = None
    is_daily: bool = False
    brand_examples: list[str] = Field(default_factory=list)
    image_url: str | None = None


class SupplementIntake(BaseContractModel):
    """Whether a supplement was taken on a given day."""

    schema_version: str = SCHEMA_VERSION
    profile_id: str
    supplement_id: str
    date: str
    taken: bool


class SupplementRequest(BaseContractModel):
    """Request supplement advice for a context."""

    schema_version: str = SCHEMA_VERSION
    language: Language = Language.EN
    modality: Modality
    objective: UserObjective | None = None
    goal_phase: GoalPhase | None = None
    week: int | None = Field(default=None, ge=1, le=42)
    weight_kg: float | None = Field(default=None, ge=20, le=300)
    height_cm: float | None = Field(default=None, ge=80, le=250)
    body_fat_pct: float | None = Field(default=None, ge=3, le=60)
    age: int | None = Field(default=None, ge=10, le=100)
    daily_calories: int | None = Field(default=None, ge=800, le=6000)


class SupplementAdviceItem(BaseContractModel):
    supplement_id: str
    name: LocalizedText
    category: SupplementCategory
    safety: SupplementSafety
    dosage: LocalizedText
    macros: MacroNutrients
    reason: LocalizedText
    image_url: str | None = None


class SupplementAdvice(BaseContractModel):
    """Supplement recommendations for a context."""

    schema_version: str = SCHEMA_VERSION
    language: Language = Language.EN
    modality: Modality | None = None
    objective: UserObjective | None = None
    goal_phase: GoalPhase | None = None
    daily_macros: MacroNutrients | None = None
    items: list[SupplementAdviceItem] = Field(default_factory=list)


__all__ = [
    "Supplement",
    "SupplementIntake",
    "SupplementRequest",
    "SupplementAdvice",
    "SupplementAdviceItem",
]

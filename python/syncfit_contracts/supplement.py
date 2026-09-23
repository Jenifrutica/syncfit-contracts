"""Supplement catalog models and advice."""

from __future__ import annotations

from pydantic import Field

from .common import (
    BaseContractModel,
    Language,
    LocalizedText,
    MacroNutrients,
    Modality,
    SupplementCategory,
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
    image_url: str | None = None


class SupplementRequest(BaseContractModel):
    """Request supplement advice for a context."""

    schema_version: str = SCHEMA_VERSION
    language: Language = Language.EN
    modality: Modality
    objective: UserObjective | None = None
    week: int | None = Field(default=None, ge=1, le=42)


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
    items: list[SupplementAdviceItem] = Field(default_factory=list)


__all__ = [
    "Supplement",
    "SupplementRequest",
    "SupplementAdvice",
    "SupplementAdviceItem",
]

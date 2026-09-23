"""Shared definitions reused by every SyncFit Edge contract model."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .version import SCHEMA_VERSION


class Modality(str, Enum):
    """Physiological modality selected by the athlete."""

    MENSTRUAL_CYCLE = "MENSTRUAL_CYCLE"
    GESTATIONAL = "GESTATIONAL"


class CyclePhase(str, Enum):
    MENSTRUAL = "MENSTRUAL"
    FOLLICULAR = "FOLLICULAR"
    OVULATORY = "OVULATORY"
    LUTEAL = "LUTEAL"


class Trimester(str, Enum):
    TRIMESTER_1 = "TRIMESTER_1"
    TRIMESTER_2 = "TRIMESTER_2"
    TRIMESTER_3 = "TRIMESTER_3"


class InferredPhase(str, Enum):
    """Phase of the cycle or gestational trimester inferred by the system."""

    MENSTRUAL = "MENSTRUAL"
    FOLLICULAR = "FOLLICULAR"
    OVULATORY = "OVULATORY"
    LUTEAL = "LUTEAL"
    TRIMESTER_1 = "TRIMESTER_1"
    TRIMESTER_2 = "TRIMESTER_2"
    TRIMESTER_3 = "TRIMESTER_3"


class FatigueLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class Language(str, Enum):
    """Output/UI language. English is the default; more may be added."""

    EN = "EN"
    ES = "ES"
    ZH = "ZH"


class ExerciseImpact(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class MuscleGroup(str, Enum):
    """Target muscle groups: isolated, region, or movement pattern."""

    GLUTES = "GLUTES"
    QUADRICEPS = "QUADRICEPS"
    HAMSTRINGS = "HAMSTRINGS"
    CALVES = "CALVES"
    ADDUCTORS = "ADDUCTORS"
    ABDUCTORS = "ABDUCTORS"
    ABS = "ABS"
    OBLIQUES = "OBLIQUES"
    LOWER_BACK = "LOWER_BACK"
    UPPER_BACK = "UPPER_BACK"
    BACK = "BACK"
    LATS = "LATS"
    CHEST = "CHEST"
    SHOULDERS = "SHOULDERS"
    BICEPS = "BICEPS"
    TRICEPS = "TRICEPS"
    FOREARMS = "FOREARMS"
    ARMS = "ARMS"
    FULL_LEG = "FULL_LEG"
    CORE = "CORE"
    UPPER_BODY = "UPPER_BODY"
    LOWER_BODY = "LOWER_BODY"
    FULL_BODY = "FULL_BODY"
    PUSH = "PUSH"
    PULL = "PULL"


class LocalizedText(BaseModel):
    """Text localized by language code; English is required, others optional."""

    model_config = ConfigDict(extra="allow")

    en: str


class BaseContractModel(BaseModel):
    """Base model: rejects unknown fields to keep the contract strict."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class Biomarkers(BaseContractModel):
    """Basal and neuromuscular biomarkers sampled at the edge."""

    delta_temperature_c: float = Field(ge=-2.0, le=2.0)
    rmssd_hrv_ms: float = Field(ge=0, le=300)
    isometric_force_loss_pct: float = Field(ge=0, le=100)


class ExerciseAdaptation(BaseContractModel):
    """Adaptation applied to a single programmed exercise."""

    exercise_original: str
    blocked: bool
    block_reason: str = ""
    exercise_substitute: str = ""
    series_adapted: int = Field(ge=0, le=20)
    reps_adapted: int = Field(ge=0, le=100)
    weight_suggested_kg: float = Field(ge=0)
    exercise_id: str | None = None
    muscle_groups: list[MuscleGroup] = Field(default_factory=list)
    impact: ExerciseImpact | None = None
    description: LocalizedText | None = None
    image_url: str | None = None
    media_url: str | None = None


class Exercise(BaseContractModel):
    """Catalog entry: an exercise with localized text and free-use media."""

    id: str
    name: LocalizedText
    muscle_groups: list[MuscleGroup] = Field(min_length=1)
    equipment: str
    impact: ExerciseImpact
    description: LocalizedText
    image_url: str
    media_url: str | None = None


class PhysiologicalState(BaseContractModel):
    """Node of the Directed State Graph."""

    id: str
    state: InferredPhase
    kind: str = Field(pattern="^(CYCLE_PHASE|TRIMESTER)$")
    label: str


class StateTransition(BaseContractModel):
    """Weighted, directed edge of the Directed State Graph."""

    from_: str = Field(alias="from")
    to: str
    weight: float = Field(ge=0, le=1)
    condition: str | None = None

    model_config = ConfigDict(extra="forbid", populate_by_name=True, use_enum_values=True)


__all__ = [
    "SCHEMA_VERSION",
    "Modality",
    "CyclePhase",
    "Trimester",
    "InferredPhase",
    "FatigueLevel",
    "AlertSeverity",
    "Language",
    "ExerciseImpact",
    "MuscleGroup",
    "LocalizedText",
    "BaseContractModel",
    "Biomarkers",
    "ExerciseAdaptation",
    "Exercise",
    "PhysiologicalState",
    "StateTransition",
]


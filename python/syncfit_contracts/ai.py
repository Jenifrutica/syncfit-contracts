"""Strict output contract for the DeepSeek JSON Mode reasoning kernel."""

from __future__ import annotations

from pydantic import Field

from .common import BaseContractModel, ExerciseAdaptation, FatigueLevel, InferredPhase
from .version import SCHEMA_VERSION


class AIReasoningResponse(BaseContractModel):
    """The model must return exactly this object, with no prose or wrapper."""

    schema_version: str = SCHEMA_VERSION
    session_id: str | None = None
    phase_inferred: InferredPhase
    fatigue_level: FatigueLevel
    articular_risk_pct: float = Field(ge=0, le=100)
    k_load_multiplier: float = Field(ge=0.70, le=1.05)
    alerts: list[str] = Field(default_factory=list)
    adapted_routine: list[ExerciseAdaptation] = Field(default_factory=list)


__all__ = ["AIReasoningResponse"]

"""Physiological assessment: the bridge between the local model and the reasoning layer.

`syncfit-core` produces this structured state (deterministically) and the cloud
reasoning layer consumes it to design the routine. The reasoning layer must never
recompute `k_load_multiplier`.
"""

from __future__ import annotations

from pydantic import Field

from .common import BaseContractModel, FatigueLevel, InferredPhase
from .version import SCHEMA_VERSION


class PhysiologicalAssessment(BaseContractModel):
    schema_version: str = SCHEMA_VERSION
    session_id: str | None = None
    phase_inferred: InferredPhase
    fatigue_level: FatigueLevel
    k_load_multiplier: float = Field(ge=0.70, le=1.05)
    autonomic_status: str = "BALANCED"
    articular_risk_pct: float = Field(default=0.0, ge=0, le=100)
    contraindicated_patterns: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    source: str = "core"


__all__ = ["PhysiologicalAssessment"]

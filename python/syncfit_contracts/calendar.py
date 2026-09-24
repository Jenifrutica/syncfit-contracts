"""Cycle/gestation calendar models."""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from .common import BaseContractModel, InferredPhase, LocalizedText, Modality
from .version import SCHEMA_VERSION


class CalendarKind(str, Enum):
    CYCLE = "CYCLE"
    OVULATION = "OVULATION"
    STRENGTH = "STRENGTH"
    LOW_IMPACT = "LOW_IMPACT"
    REST = "REST"


class CalendarDay(BaseContractModel):
    date: str
    kind: CalendarKind
    cycle_day: int | None = None
    phase: InferredPhase | None = None
    label: LocalizedText | None = None
    note: LocalizedText | None = None


class CycleCalendar(BaseContractModel):
    """Monthly calendar of cycle days, strength days and low-impact guidance."""

    schema_version: str = SCHEMA_VERSION
    month: str
    modality: Modality | None = None
    days: list[CalendarDay] = Field(default_factory=list)


__all__ = ["CalendarKind", "CalendarDay", "CycleCalendar"]

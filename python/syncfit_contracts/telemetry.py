"""Telemetry frame emitted by the ESP32 device and carried by the Ring Buffer."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from .common import BaseContractModel, Biomarkers, Modality
from .version import SCHEMA_VERSION


class PpgWindow(BaseContractModel):
    """Ring-buffer window of optical PPG samples."""

    sample_rate_hz: Literal[100] = 100
    window_size: int | None = Field(default=None, ge=1)
    samples: list[float] = Field(min_length=1)


class TelemetryFrame(BaseContractModel):
    """A fixed-window telemetry frame emitted at 100 Hz."""

    schema_version: str = SCHEMA_VERSION
    device_id: str = Field(min_length=1)
    session_id: str
    timestamp: datetime
    modality: Modality
    day_or_week: int = Field(ge=1, le=42)
    biomarkers: Biomarkers
    ppg_window: PpgWindow


__all__ = ["PpgWindow", "TelemetryFrame"]

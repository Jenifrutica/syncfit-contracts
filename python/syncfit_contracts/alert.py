"""Critical physiological alert dispatched through the Max-Heap in O(1)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from .common import AlertSeverity, BaseContractModel
from .version import SCHEMA_VERSION


class AlertCode(str, Enum):
    RMSSD_DROP = "RMSSD_DROP"
    CORE_TEMP_RISE = "CORE_TEMP_RISE"
    CNS_FATIGUE = "CNS_FATIGUE"
    ARTICULAR_RISK = "ARTICULAR_RISK"
    SENSOR_FAULT = "SENSOR_FAULT"


class PhysiologicalAlert(BaseContractModel):
    schema_version: str = SCHEMA_VERSION
    alert_id: str
    session_id: str
    timestamp: datetime
    severity: AlertSeverity
    code: AlertCode
    message: str
    metric: str | None = None
    value: float | None = None
    threshold: float | None = None


__all__ = ["AlertCode", "PhysiologicalAlert"]

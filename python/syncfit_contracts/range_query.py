"""Request and response models for the Time-Series Segment Tree range queries."""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from .common import BaseContractModel
from .version import SCHEMA_VERSION


class Metric(str, Enum):
    TEMPERATURE = "temperature"
    RMSSD = "rmssd"
    ISOMETRIC_FORCE_LOSS = "isometric_force_loss"


class Aggregation(str, Enum):
    MIN = "min"
    MAX = "max"
    MEAN = "mean"


class RangeQueryRequest(BaseContractModel):
    schema_version: str = SCHEMA_VERSION
    session_id: str
    metric: Metric
    start_index: int = Field(ge=0)
    end_index: int = Field(ge=0)
    aggregation: Aggregation


class RangeQueryResponse(BaseContractModel):
    schema_version: str = SCHEMA_VERSION
    session_id: str
    metric: Metric
    start_index: int = Field(ge=0)
    end_index: int = Field(ge=0)
    aggregation: Aggregation
    value: float
    count: int = Field(ge=0)


__all__ = ["Metric", "Aggregation", "RangeQueryRequest", "RangeQueryResponse"]

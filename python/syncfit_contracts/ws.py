"""WebSocket envelope for every message exchanged in either direction."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from .common import BaseContractModel
from .version import SCHEMA_VERSION


class WsMessageType(str, Enum):
    TELEMETRY = "telemetry"
    ALERT = "alert"
    PRESCRIPTION = "prescription"
    ACK = "ack"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


class WsEnvelope(BaseContractModel):
    """Envelope wrapping a typed payload."""

    schema_version: str = SCHEMA_VERSION
    type: WsMessageType
    timestamp: datetime
    session_id: str | None = None
    correlation_id: str | None = None
    payload: dict[str, Any]


__all__ = ["WsMessageType", "WsEnvelope"]

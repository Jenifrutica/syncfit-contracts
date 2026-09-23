"""SyncFit Edge cross-repository contracts.

This package is the single source of truth for every payload exchanged between
the firmware, backend, core, reasoning layer, simulator and frontend.
"""

from .ai import AIReasoningResponse
from .alert import AlertCode, PhysiologicalAlert
from .catalog import (
    exercises_for_groups,
    get_exercise,
    load_exercises,
    localize,
)
from .common import (
    AlertSeverity,
    Biomarkers,
    CyclePhase,
    Exercise,
    ExerciseAdaptation,
    ExerciseImpact,
    FatigueLevel,
    InferredPhase,
    Language,
    LocalizedText,
    Modality,
    MuscleGroup,
    PhysiologicalState,
    StateTransition,
    Trimester,
)
from .range_query import (
    Aggregation,
    Metric,
    RangeQueryRequest,
    RangeQueryResponse,
)
from .routine import AdaptedRoutine, RoutineRequest, RoutineResponse
from .state_graph import PhysiologicalStateGraph
from .telemetry import PpgWindow, TelemetryFrame
from .version import SCHEMA_VERSION
from .ws import WsEnvelope, WsMessageType

__version__ = SCHEMA_VERSION

__all__ = [
    "SCHEMA_VERSION",
    "__version__",
    "AIReasoningResponse",
    "AdaptedRoutine",
    "Aggregation",
    "AlertCode",
    "AlertSeverity",
    "Biomarkers",
    "CyclePhase",
    "Exercise",
    "ExerciseAdaptation",
    "ExerciseImpact",
    "FatigueLevel",
    "InferredPhase",
    "Language",
    "LocalizedText",
    "Metric",
    "Modality",
    "MuscleGroup",
    "PhysiologicalAlert",
    "PhysiologicalState",
    "PhysiologicalStateGraph",
    "PpgWindow",
    "RangeQueryRequest",
    "RangeQueryResponse",
    "RoutineRequest",
    "RoutineResponse",
    "StateTransition",
    "TelemetryFrame",
    "Trimester",
    "WsEnvelope",
    "WsMessageType",
    "load_exercises",
    "get_exercise",
    "exercises_for_groups",
    "localize",
]

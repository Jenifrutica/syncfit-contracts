"""SyncFit Edge cross-repository contracts.

This package is the single source of truth for every payload exchanged between
the firmware, backend, core, reasoning layer, simulator and frontend.
"""

from .ai import AIReasoningResponse
from .alert import AlertCode, PhysiologicalAlert
from .catalog import (
    exercises_for_groups,
    get_exercise,
    get_machine,
    get_supplement,
    load_exercises,
    load_machines,
    load_supplements,
    localize,
    machines_for_exercise,
    supplements_for,
)
from .calendar import CalendarDay, CalendarKind, CycleCalendar
from .common import (
    AlertSeverity,
    Biomarkers,
    CyclePhase,
    EnergyLevel,
    EquipmentType,
    Exercise,
    ExerciseAdaptation,
    ExerciseImpact,
    ExerciseLoad,
    ExerciseRole,
    FatigueLevel,
    GoalPhase,
    InferredPhase,
    Language,
    LocalizedText,
    MacroNutrients,
    Modality,
    MuscleGroup,
    PhysiologicalState,
    SetPrescription,
    SetType,
    StateTransition,
    SupplementCategory,
    SupplementFrequency,
    SupplementSafety,
    Trimester,
    UserObjective,
)
from .machine import GymMachine
from .range_query import (
    Aggregation,
    Metric,
    RangeQueryRequest,
    RangeQueryResponse,
)
from .routine import AdaptedRoutine, RoutineRequest, RoutineResponse
from .state_graph import PhysiologicalStateGraph
from .supplement import (
    Supplement,
    SupplementAdvice,
    SupplementAdviceItem,
    SupplementIntake,
    SupplementRequest,
)
from .telemetry import PpgWindow, TelemetryFrame
from .user import EnergyCheckIn, UserProfile
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
    "ExerciseLoad",
    "ExerciseRole",
    "EquipmentType",
    "EnergyLevel",
    "EnergyCheckIn",
    "GoalPhase",
    "GymMachine",
    "CalendarDay",
    "CalendarKind",
    "CycleCalendar",
    "FatigueLevel",
    "InferredPhase",
    "Language",
    "LocalizedText",
    "MacroNutrients",
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
    "SetPrescription",
    "SetType",
    "StateTransition",
    "Supplement",
    "SupplementIntake",
    "SupplementFrequency",
    "SupplementAdvice",
    "SupplementAdviceItem",
    "SupplementCategory",
    "SupplementRequest",
    "SupplementSafety",
    "TelemetryFrame",
    "Trimester",
    "UserObjective",
    "UserProfile",
    "WsEnvelope",
    "WsMessageType",
    "load_exercises",
    "load_supplements",
    "load_machines",
    "get_exercise",
    "get_supplement",
    "get_machine",
    "exercises_for_groups",
    "supplements_for",
    "machines_for_exercise",
    "localize",
]

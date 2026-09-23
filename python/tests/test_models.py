import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from syncfit_contracts import (  # noqa: E402
    AdaptedRoutine,
    AIReasoningResponse,
    Exercise,
    MuscleGroup,
    PhysiologicalAlert,
    PhysiologicalStateGraph,
    RangeQueryRequest,
    RangeQueryResponse,
    RoutineRequest,
    RoutineResponse,
    TelemetryFrame,
    WsEnvelope,
    exercises_for_groups,
    get_exercise,
    load_exercises,
    localize,
)

EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"


def load(name: str) -> dict:
    return json.loads((EXAMPLES_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "name,model",
    [
        ("telemetry-menstrual-ovulatory.json", TelemetryFrame),
        ("telemetry-gestational.json", TelemetryFrame),
        ("ws-envelope-telemetry.json", WsEnvelope),
        ("ai-response-ovulatory-block.json", AIReasoningResponse),
        ("ai-response-gestational.json", AIReasoningResponse),
        ("adapted-routine.json", AdaptedRoutine),
        ("alert-critical.json", PhysiologicalAlert),
        ("range-query-request.json", RangeQueryRequest),
        ("range-query-response.json", RangeQueryResponse),
        ("state-graph.json", PhysiologicalStateGraph),
    ],
)
def test_examples_parse_with_pydantic(name, model):
    instance = model.model_validate(load(name))
    assert instance.schema_version == "1.0.0"


def test_routine_request_and_response_parse():
    request = RoutineRequest.model_validate(load("routine-request.json"))
    assert request.language == "ES"
    assert request.muscle_groups == ["GLUTES", "QUADRICEPS"]

    response = RoutineResponse.model_validate(load("routine-response.json"))
    assert response.routine[0].exercise_id == "goblet-squat"
    assert response.routine[0].blocked is True


def test_exercise_parses_and_requires_english():
    exercise = Exercise.model_validate(load("exercise.json"))
    assert exercise.id == "goblet-squat"
    assert "GLUTES" in exercise.muscle_groups


def test_catalog_loader_and_helpers():
    exercises = load_exercises()
    assert len(exercises) >= 20
    assert get_exercise("goblet-squat") is not None
    assert get_exercise("does-not-exist") is None

    glutes = exercises_for_groups([MuscleGroup.GLUTES])
    assert len(glutes) >= 3
    assert all("GLUTES" in [str(g) for g in e.muscle_groups] for e in glutes)

    low_impact = exercises_for_groups(["QUADRICEPS"], impact="LOW")
    assert all(str(e.impact) == "LOW" for e in low_impact)


def test_localize_falls_back_to_english():
    exercise = get_exercise("goblet-squat")
    assert exercise is not None
    assert localize(exercise.name, "ES") == "Sentadilla goblet"
    assert localize(exercise.name, "ZH") == "高脚杯深蹲"
    assert localize(exercise.name, "FR") == "Goblet squat"  # unknown -> English


def test_k_load_range_is_enforced():
    from pydantic import ValidationError

    payload = load("adapted-routine.json")
    payload["k_load_multiplier"] = 1.5
    with pytest.raises(ValidationError):
        AdaptedRoutine.model_validate(payload)


def test_unknown_fields_are_rejected():
    from pydantic import ValidationError

    payload = load("alert-critical.json")
    payload["unexpected"] = True
    with pytest.raises(ValidationError):
        PhysiologicalAlert.model_validate(payload)


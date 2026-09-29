import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from syncfit_contracts import (  # noqa: E402
    AdaptedRoutine,
    AIReasoningResponse,
    EnergyCheckIn,
    Exercise,
    MuscleGroup,
    PhysiologicalAlert,
    PhysiologicalStateGraph,
    RangeQueryRequest,
    RangeQueryResponse,
    RoutineRequest,
    RoutineResponse,
    SetPrescription,
    Supplement,
    SupplementAdvice,
    SupplementRequest,
    TelemetryFrame,
    UserProfile,
    WsEnvelope,
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


def test_user_profile_and_energy_checkin():
    profile = UserProfile.model_validate(load("user-profile.json"))
    assert profile.height_cm == 165
    assert profile.loads[0].exercise_id == "goblet-squat"

    checkin = EnergyCheckIn.model_validate(load("energy-checkin.json"))
    assert checkin.energy_level == "MODERATE"
    assert checkin.day_or_week == 14


def test_supplement_models_and_catalog():
    supplement = Supplement.model_validate(load("supplement.json"))
    assert supplement.safety_pregnancy == "SAFE"
    advice = SupplementAdvice.model_validate(load("supplement-advice.json"))
    assert advice.items[0].supplement_id == "folate"
    assert SupplementRequest.model_validate(load("supplement-request.json")).modality == "GESTATIONAL"


def test_supplement_catalog_helpers():
    supplements = load_supplements()
    assert len(supplements) >= 8
    assert get_supplement("folate") is not None

    gestational = supplements_for(modality="GESTATIONAL")
    ids = {s.id for s in gestational}
    assert "creatine" not in ids  # excluded as AVOID in pregnancy
    assert "folate" in ids

    hydrate = supplements_for(objective="HYPERTROPHY")
    assert any(s.id == "whey-protein" for s in hydrate)


def test_set_prescription_model():
    prescription = SetPrescription(
        type="APPROXIMATION", reps=8, weight_kg=40, rest_seconds=60, estimated_seconds=75
    )
    assert prescription.type == "APPROXIMATION"


def test_activation_exercises_in_catalog():
    activation = [e for e in load_exercises() if str(e.role) == "ACTIVATION"]
    assert activation, "expected activation exercises in the catalog"


def test_machine_catalog_and_helpers():
    machines = load_machines()
    assert len(machines) >= 24
    leg_press = get_machine("leg-press")
    assert leg_press is not None and leg_press.weight_factor > 1
    assisted = get_machine("assisted-pullup-machine")
    assert assisted is not None and assisted.unit == "BODYWEIGHT"
    supported = machines_for_exercise("leg-press")
    assert any(m.id == "leg-press" for m in supported)


def test_more_exercises_including_assisted_and_machines():
    ids = {e.id for e in load_exercises()}
    for expected in ("assisted-pull-up", "assisted-dip", "hack-squat", "leg-press", "pull-up", "dip", "belt-squat", "pendulum-squat", "hip-abduction", "seated-cable-row"):
        assert expected in ids
    belt = get_exercise("belt-squat")
    assert belt is not None and belt.how_to is not None and belt.tips
    leg_press = get_exercise("leg-press")
    assert leg_press is not None and str(leg_press.equipment_type) == "MACHINE"


def test_symptom_catalog():
    from syncfit_contracts import load_symptoms, get_symptom

    assert len(load_symptoms()) >= 5
    assert get_symptom("knee_pain")["impact_cap"] == "LOW"


def test_cycle_calendar_parses():
    from syncfit_contracts import CycleCalendar

    calendar = CycleCalendar.model_validate(load("cycle-calendar.json"))
    assert calendar.month == "2026-09"
    assert any(day.kind == "OVULATION" for day in calendar.days)


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


def test_joined_gym_parses():
    from syncfit_contracts import JoinedGym

    gym = JoinedGym.model_validate(load("joined-gym.json"))
    assert gym.name == "Asgard"
    assert gym.active is True
    assert len(gym.machines) == 1
    assert gym.machines[0].gym_id == gym.gym_id
    assert gym.machines[0].name.en == "Hip thrust machine"
    assert "hip-thrust" in gym.machines[0].exercise_ids


def test_unknown_fields_are_rejected():
    from pydantic import ValidationError

    payload = load("alert-critical.json")
    payload["unexpected"] = True
    with pytest.raises(ValidationError):
        PhysiologicalAlert.model_validate(payload)



def test_exercise_variants_share_a_family():
    from syncfit_contracts import variants_of, exercise_family

    assert exercise_family("hip-thrust-machine") == "hip_thrust"
    ids = {e.id for e in variants_of("hip-thrust-machine")}
    assert {"hip-thrust", "smith-hip-thrust", "hip-thrust-machine"} <= ids
    assert variants_of("goblet-squat")  # squat family has several variants


def test_required_patterns_for_glutes():
    from syncfit_contracts import required_patterns

    patterns = required_patterns("GLUTES")
    assert patterns[:5] == ("hinge", "lunge", "hip_thrust", "glute_kickback", "hip_abduction")


def test_physiological_assessment_parses():
    from syncfit_contracts import PhysiologicalAssessment

    data = load("physiological-assessment.json")
    assessment = PhysiologicalAssessment.model_validate(data)
    assert assessment.phase_inferred == "OVULATORY"
    assert assessment.k_load_multiplier == 0.88


def test_exercise_required_equipment_and_filter():
    from syncfit_contracts import get_exercise, exercises_for_equipment

    assert "bench" in get_exercise("db-bulgarian-split-squat").required_equipment
    with_bench = {e.id for e in exercises_for_equipment(["dumbbell", "bench"])}
    assert "db-bulgarian-split-squat" in with_bench
    assert "step-ups" in with_bench
    without = {e.id for e in exercises_for_equipment(["machine"])}
    assert "db-bulgarian-split-squat" not in without
    assert "hip-thrust-machine" in without
    # bodyweight is always available
    bodyweight = {e.id for e in exercises_for_equipment([])}
    assert "plank" in bodyweight

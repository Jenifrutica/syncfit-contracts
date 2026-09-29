"""Exercise catalog: shared, localized, free-use exercise data."""

from __future__ import annotations

import json
from collections.abc import Iterable
from functools import lru_cache
from importlib.resources import files

from ..common import Exercise, ExerciseImpact, LocalizedText, SupplementSafety
from ..machine import GymMachine
from ..supplement import Supplement

CATALOG_FILE = "exercises.json"
SUPPLEMENT_FILE = "supplements.json"
MACHINE_FILE = "machines.json"
SYMPTOM_FILE = "symptoms.json"


@lru_cache(maxsize=1)
def load_machines() -> tuple[GymMachine, ...]:
    """Load and validate the gym machine catalog (cached)."""
    raw = (files(__package__) / MACHINE_FILE).read_text(encoding="utf-8")
    data = json.loads(raw)
    return tuple(GymMachine.model_validate(item) for item in data)


@lru_cache(maxsize=1)
def load_symptoms() -> tuple[dict, ...]:
    """Load the symptom catalog (plain data)."""
    raw = (files(__package__) / SYMPTOM_FILE).read_text(encoding="utf-8")
    return tuple(json.loads(raw))


def get_symptom(symptom_id: str) -> dict | None:
    for symptom in load_symptoms():
        if symptom["id"] == symptom_id:
            return symptom
    return None


def get_machine(machine_id: str) -> GymMachine | None:
    for machine in load_machines():
        if machine.id == machine_id:
            return machine
    return None


def machines_for_exercise(exercise_id: str) -> list[GymMachine]:
    return [m for m in load_machines() if exercise_id in m.exercises]


@lru_cache(maxsize=1)
def load_exercises() -> tuple[Exercise, ...]:
    """Load and validate the exercise catalog (cached)."""
    raw = (files(__package__) / CATALOG_FILE).read_text(encoding="utf-8")
    data = json.loads(raw)
    return tuple(Exercise.model_validate(item) for item in data)


@lru_cache(maxsize=1)
def load_supplements() -> tuple[Supplement, ...]:
    """Load and validate the supplement catalog (cached)."""
    raw = (files(__package__) / SUPPLEMENT_FILE).read_text(encoding="utf-8")
    data = json.loads(raw)
    return tuple(Supplement.model_validate(item) for item in data)


def get_supplement(supplement_id: str) -> Supplement | None:
    for supplement in load_supplements():
        if supplement.id == supplement_id:
            return supplement
    return None


def supplements_for(
    objective: object | None = None,
    modality: object | None = None,
) -> list[Supplement]:
    """Filter supplements by objective; exclude AVOID ones for pregnancy."""
    result = list(load_supplements())
    if objective is not None:
        wanted = _value(objective)
        result = [
            s for s in result if wanted in {_value(o) for o in s.objectives}
        ]
    if modality is not None and _value(modality) == "GESTATIONAL":
        result = [s for s in result if _value(s.safety_pregnancy) != "AVOID"]
    return result



def get_exercise(exercise_id: str) -> Exercise | None:
    for exercise in load_exercises():
        if exercise.id == exercise_id:
            return exercise
    return None


def _value(item: object) -> str:
    return item.value if hasattr(item, "value") else str(item)


def exercises_for_groups(
    groups: list[str],
    impact: ExerciseImpact | str | None = None,
) -> list[Exercise]:
    """Return exercises targeting any of the given muscle groups."""
    wanted = {_value(g) for g in groups}
    result = [
        exercise
        for exercise in load_exercises()
        if wanted & {_value(group) for group in exercise.muscle_groups}
    ]
    if impact is not None:
        result = [exercise for exercise in result if _value(exercise.impact) == _value(impact)]
    return result


def exercise_family(exercise_id: str) -> str | None:
    """Return the movement family (`variant_of`) of an exercise, if any."""
    exercise = get_exercise(exercise_id)
    if exercise is None:
        return None
    return getattr(exercise, "variant_of", None)


def variants_of(exercise_id: str) -> tuple[Exercise, ...]:
    """Interchangeable variations of the same movement (same `variant_of`).

    Uses a single pass over the catalog; the family acts as a hash key so callers
    can group the whole catalog in O(n).
    """
    family = exercise_family(exercise_id)
    if not family:
        return ()
    return tuple(
        exercise
        for exercise in load_exercises()
        if getattr(exercise, "variant_of", None) == family
    )


#: Movement patterns that a routine should cover for each muscle group, in priority order.
REQUIRED_PATTERNS: dict[str, tuple[str, ...]] = {
    "GLUTES": ("hinge", "lunge", "hip_thrust", "glute_kickback", "hip_abduction"),
    "QUADRICEPS": ("squat", "lunge", "leg_extension"),
    "HAMSTRINGS": ("hinge", "glute_ham", "leg_curl"),
    "CALVES": ("calf_raise",),
    "ADDUCTORS": ("hip_adduction",),
    "ABDUCTORS": ("hip_abduction", "glute_kickback"),
    "LOWER_BACK": ("hinge", "row"),
    "BACK": ("pull_vertical", "row"),
    "LATS": ("pull_vertical", "row"),
    "UPPER_BACK": ("row", "pull_vertical"),
    "CHEST": ("bench_press", "chest_fly"),
    "SHOULDERS": ("overhead_press", "lateral_raise"),
    "BICEPS": ("biceps",),
    "TRICEPS": ("triceps",),
    "ARMS": ("biceps", "triceps"),
    "FOREARMS": ("biceps",),
    "ABS": ("core_plank", "core_deadbug", "core_hanging"),
    "OBLIQUES": ("core_plank", "core_deadbug"),
    "CORE": ("core_plank", "core_deadbug", "core_hanging"),
    "FULL_LEG": ("squat", "hinge", "lunge"),
    "LOWER_BODY": ("squat", "hinge", "lunge", "hip_thrust"),
    "UPPER_BODY": ("bench_press", "pull_vertical", "row", "overhead_press"),
    "FULL_BODY": ("squat", "hinge", "bench_press", "row"),
    "PUSH": ("bench_press", "overhead_press"),
    "PULL": ("pull_vertical", "row"),
}


#: Canonical equipment keys used by `Exercise.required_equipment` and gym inventory.
EQUIPMENT_KEYS = (
    "machine", "smith", "barbell", "dumbbell", "bench", "cable",
    "pullup-bar", "dip-bar", "ghd", "box", "band", "none",
)


def exercise_required_equipment(exercise: "Exercise") -> set[str]:
    required = {str(k) for k in (getattr(exercise, "required_equipment", None) or [])}
    return required or {"none"}


def exercises_for_equipment(
    equipment_keys: Iterable[str] | None = None,
    muscle_groups: Iterable[str] | None = None,
) -> list["Exercise"]:
    """Exercises doable with the given equipment (``none``/bodyweight always allowed)."""
    available = {_value(k) for k in equipment_keys} if equipment_keys else None
    wanted = {_value(g) for g in muscle_groups} if muscle_groups else None
    result: list["Exercise"] = []
    for exercise in load_exercises():
        required = exercise_required_equipment(exercise)
        if available is not None and not (required <= available or required <= {"none"}):
            continue
        if wanted is not None and not (wanted & {_value(g) for g in exercise.muscle_groups}):
            continue
        result.append(exercise)
    return result


def patterns_of(exercise: "Exercise") -> str | None:
    return getattr(exercise, "movement_pattern", None) or getattr(exercise, "variant_of", None)


def required_patterns(muscle_groups: Iterable[str] | str) -> tuple[str, ...]:
    """Return the required movement patterns for the given group(s), deduplicated.

    Order follows ``REQUIRED_PATTERNS``; duplicates across groups are removed
    while preserving the first occurrence (so priority is stable).
    """
    groups = [muscle_groups] if isinstance(muscle_groups, str) else list(muscle_groups)
    ordered: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for pattern in REQUIRED_PATTERNS.get(_value(group), ()):  # type: ignore[arg-type]
            if pattern not in seen:
                seen.add(pattern)
                ordered.append(pattern)
    return tuple(ordered)


def exercises_for_pattern(pattern: str, muscle_groups: Iterable[str] | None = None) -> list["Exercise"]:
    """Catalog exercises with a given movement pattern, optionally restricted to groups."""
    wanted = {_value(g) for g in muscle_groups} if muscle_groups else None
    result = []
    for exercise in load_exercises():
        if patterns_of(exercise) != pattern:
            continue
        if wanted is not None and not (wanted & {_value(g) for g in exercise.muscle_groups}):
            continue
        result.append(exercise)
    return result


def localize(text: LocalizedText | dict[str, str] | None, language: str) -> str:
    """Return the text in the requested language, falling back to English."""
    if text is None:
        return ""
    if isinstance(text, dict):
        code = language.lower()
        return text.get(code) or text.get("en", "")
    code = language.lower()
    if code == "en":
        return text.en
    extra = text.model_extra or {}
    return extra.get(code) or text.en


__all__ = [
    "CATALOG_FILE",
    "SUPPLEMENT_FILE",
    "MACHINE_FILE",
    "load_exercises",
    "load_supplements",
    "load_machines",
    "get_exercise",
    "get_supplement",
    "get_machine",
    "exercises_for_groups",
    "exercise_family",
    "variants_of",
    "REQUIRED_PATTERNS",
    "EQUIPMENT_KEYS",
    "patterns_of",
    "required_patterns",
    "exercises_for_pattern",
    "exercise_required_equipment",
    "exercises_for_equipment",
    "supplements_for",
    "machines_for_exercise",
    "load_symptoms",
    "get_symptom",
    "localize",
]

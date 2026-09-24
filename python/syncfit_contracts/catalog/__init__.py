"""Exercise catalog: shared, localized, free-use exercise data."""

from __future__ import annotations

import json
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
    "supplements_for",
    "machines_for_exercise",
    "load_symptoms",
    "get_symptom",
    "localize",
]

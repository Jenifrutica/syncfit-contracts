"""Exercise catalog: shared, localized, free-use exercise data."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files

from ..common import Exercise, ExerciseImpact, LocalizedText

CATALOG_FILE = "exercises.json"


@lru_cache(maxsize=1)
def load_exercises() -> tuple[Exercise, ...]:
    """Load and validate the exercise catalog (cached)."""
    raw = (files(__package__) / CATALOG_FILE).read_text(encoding="utf-8")
    data = json.loads(raw)
    return tuple(Exercise.model_validate(item) for item in data)


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
    "load_exercises",
    "get_exercise",
    "exercises_for_groups",
    "localize",
]

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = REPO_ROOT / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def registry():
    referencing = pytest.importorskip("referencing")
    resources = []
    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        schema = load_json(schema_path)
        resources.append((schema["$id"], referencing.Resource.from_contents(schema)))
    return referencing.Registry().with_resources(resources)


EXAMPLE_TO_SCHEMA = {
    "telemetry-menstrual-ovulatory.json": "telemetry-frame.schema.json",
    "telemetry-gestational.json": "telemetry-frame.schema.json",
    "ws-envelope-telemetry.json": "ws-envelope.schema.json",
    "ai-response-ovulatory-block.json": "ai-response.schema.json",
    "ai-response-gestational.json": "ai-response.schema.json",
    "adapted-routine.json": "adapted-routine.schema.json",
    "alert-critical.json": "alert.schema.json",
    "range-query-request.json": "range-query-request.schema.json",
    "range-query-response.json": "range-query-response.schema.json",
    "state-graph.json": "state-graph.schema.json",
    "exercise.json": "exercise.schema.json",
    "routine-request.json": "routine-request.schema.json",
    "routine-response.json": "routine-response.schema.json",
}


@pytest.mark.parametrize("example_name,schema_name", sorted(EXAMPLE_TO_SCHEMA.items()))
def test_examples_validate_against_schemas(registry, example_name, schema_name):
    jsonschema = pytest.importorskip("jsonschema")
    from jsonschema import Draft202012Validator

    schema = load_json(SCHEMAS_DIR / schema_name)
    instance = load_json(EXAMPLES_DIR / example_name)
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    assert not errors, "\n".join(e.message for e in errors)


def test_catalog_validates_against_schema(registry):
    from jsonschema import Draft202012Validator

    catalog_path = REPO_ROOT / "python" / "syncfit_contracts" / "catalog" / "exercises.json"
    schema = load_json(SCHEMAS_DIR / "exercise-catalog.schema.json")
    instance = load_json(catalog_path)
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    assert not errors, "\n".join(e.message for e in errors)


def test_all_schemas_are_valid_json_schema(registry):
    from jsonschema import Draft202012Validator

    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        Draft202012Validator.check_schema(load_json(schema_path))


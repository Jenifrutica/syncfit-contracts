import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from syncfit_contracts import (  # noqa: E402
    AdaptedRoutine,
    AIReasoningResponse,
    PhysiologicalAlert,
    PhysiologicalStateGraph,
    RangeQueryRequest,
    RangeQueryResponse,
    TelemetryFrame,
    WsEnvelope,
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

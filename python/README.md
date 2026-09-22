# syncfit-contracts (Python)

Pydantic v2 models for the SyncFit Edge cross-repository contract.

```bash
pip install .
```

```python
from syncfit_contracts import TelemetryFrame, AdaptedRoutine

frame = TelemetryFrame.model_validate(payload)
routine = AdaptedRoutine.model_validate(ai_payload)
```

The full contract (JSON Schemas, OpenAPI, TypeScript types, fixtures) lives at
the repository root. See the top-level `README.md`.

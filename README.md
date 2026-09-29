# SyncFit Contracts

Single source of truth for every interface between SyncFit Edge repositories. No layer may define its own payload: every telemetry frame, WebSocket message, REST response and AI output must validate against a schema published here.

## Purpose

`syncfit-contracts` guarantees that firmware, backend, frontend and the AI pipeline never drift apart. It contains schemas, generated type definitions and example fixtures, and it is versioned so that consumers can pin a known-good contract.

## What belongs here

- **JSON Schemas** for every cross-repo payload:
  - Telemetry frame emitted by the device (PPG at 100 Hz, thermal delta, isometric load).
  - WebSocket message envelope (client to server and server to client).
  - Adapted routine object returned by the reasoning layer.
  - Strict output schema for the DeepSeek JSON Mode response.
- **OpenAPI specification** for the backend REST endpoints.
- **Shared types**:
  - Python definitions (Pydantic models).
  - TypeScript definitions and validators (generated types / Zod).
- **Example fixtures** used as test data across all repositories.

## What does NOT belong here

- Business logic, orchestration or any runtime service.
- DSP, ML models or prompt engineering.
- Hardware drivers or UI components.

## Data Structures

Although this repository contains no algorithms, its schemas formally describe the structures used elsewhere:

| Structure | How it is represented here |
|-----------|----------------------------|
| Ring Buffer | Frame schema for the fixed-window 100 Hz sample stream. |
| Priority Queue / Max-Heap | Alert entry schema (severity, timestamp, payload). |
| Directed State Graph | Node and weighted-edge schema for physiological states. |
| Time-Series Segment Tree | Range-query request/response schema (min, max, mean). |

### Routine patterns and assessment (v1.12.0)

- `Exercise.movement_pattern` / `compound` drive pattern coverage, duplicate
  avoidance and compound-first ordering; `required_patterns()` / `patterns_of()` /
  `exercises_for_pattern()` expose them.
- `Exercise.required_equipment` + `EQUIPMENT_KEYS` / `exercises_for_equipment()` filter
  routines by the gym's real equipment.
- `PhysiologicalAssessment` is the local-model state consumed by DeepSeek.
- `ExerciseAdaptation` carries `movement_pattern`, `compound` and `rationale`.

### Gym membership schemas (v1.9.0)

- `GymMembership` formalizes the join relation as a **unique pair**
  `(profile_id, gym_id)` — set semantics, so joining the same gym twice is a no-op.
- `JoinedGym` is a **hash-map-shaped view**: gyms are keyed by `gym_id` and each
  carries a live list of `GymStation` machines plus an `active` flag.
- `GymStation` describes a machine added by a gym admin, distinct from the shared
  catalog `GymMachine`. Its `name`/`purpose` are `LocalizedText` (AI-translated on
  write) and `exercise_ids` lists the catalog exercises it covers.
- `ExerciseAdaptation.machine_id`/`machine_name` point a routine entry to the gym
  machine that handles it (photo + weight factor).
- `Exercise.variant_of` groups interchangeable movements (movement family);
  `variants_of(id)` / `exercise_family(id)` expose them. `UserProfile.document_id`
  is the national id (cedula).

## Repository layout

```
syncfit-contracts/
├── schemas/                              # JSON Schema (Draft 2020-12)
│   ├── common.schema.json                # shared definitions ($defs)
│   ├── telemetry-frame.schema.json       # 100 Hz telemetry frame (Ring Buffer)
│   ├── ws-envelope.schema.json           # WebSocket envelope
│   ├── alert.schema.json                 # alert entry (Max-Heap)
│   ├── adapted-routine.schema.json       # adapted prescription
│   ├── ai-response.schema.json           # strict DeepSeek JSON Mode output
│   ├── range-query-request.schema.json   # Segment Tree query (request)
│   ├── range-query-response.schema.json  # Segment Tree query (response)
│   └── state-graph.schema.json           # Directed State Graph
├── openapi/openapi.yaml                  # backend REST contract
├── python/
│   ├── syncfit_contracts/                # Pydantic v2 models
│   ├── tests/                            # schema + model validation tests
│   └── pyproject.toml
├── typescript/
│   ├── src/                              # Zod validators + inferred types
│   ├── test/                             # validation tests (vitest)
│   ├── package.json
│   └── tsconfig.json
├── examples/                             # fixtures used across all repos
├── CHANGELOG.md
├── VERSION
└── README.md
```

## Usage

### Python

```bash
cd python
pip install -e ".[dev]"
pytest -q
```

```python
from syncfit_contracts import TelemetryFrame, AdaptedRoutine

frame = TelemetryFrame.model_validate(payload)
routine = AdaptedRoutine.model_validate(ai_payload)
```

### TypeScript

```bash
cd typescript
npm install
npm run typecheck
npm test
```

```ts
import { TelemetryFrame, AdaptedRoutine } from "@syncfit/contracts";

const frame = TelemetryFrame.parse(payload);
const routine = AdaptedRoutine.parse(aiPayload);
```

## Versioning

The contract follows Semantic Versioning. The current version lives in `VERSION`
and `python/syncfit_contracts/version.py` (`SCHEMA_VERSION`); every change is
recorded in `CHANGELOG.md`. Consumers should pin a known-good version.

## Stack

Python 3.11+ (Pydantic v2, jsonschema) and TypeScript (Zod, vitest).

## Tasks

### Requirements

- [x] Define the JSON Schema for the telemetry frame (PPG at 100 Hz, thermal delta, isometric load).
- [x] Define the WebSocket message envelope (client → server and server → client).
- [x] Define the adapted-routine schema returned by the reasoning layer.
- [x] Define the strict DeepSeek JSON Mode output schema.
- [x] Publish the OpenAPI specification for all backend REST endpoints.
- [x] Generate Python models (Pydantic).
- [x] Generate TypeScript types and Zod validators.
- [x] Add a versioning strategy and changelog.
- [x] Add example fixtures used as test data across all repositories.
- [x] Add schema validation tests.

## Related repositories

- [`syncfit-hardware`](../syncfit-hardware) — produces telemetry frames.
- [`syncfit-backend`](../syncfit-backend) — consumes and validates schemas.
- [`syncfit-core`](../syncfit-core) — feature and model I/O.
- [`syncfit-ai-reasoning`](../syncfit-ai-reasoning) — validates strict AI output.
- [`syncfit-simulator`](../syncfit-simulator) — generates schema-valid test data.
- [`syncfit-frontend`](../syncfit-frontend) — consumes generated TypeScript types.

All code, comments, documentation and commits in this repository are written in English.

## Context for a new session

**What it is.** Single source of truth for every interface between SyncFit Edge
repos. Version **1.7.0** (see `VERSION`). 9+ JSON Schemas, OpenAPI, Pydantic and
Zod models, shared catalogs and fixtures.

**Stack.** Python 3.11+ (Pydantic v2, jsonschema) + TypeScript (Zod, vitest).

**Layout.** `schemas/` (JSON Schema), `openapi/openapi.yaml`, `python/syncfit_contracts/`
(models + `catalog/` data), `typescript/src/`, `examples/` (fixtures),
`CHANGELOG.md`, `VERSION`.

**Catalogs (data).** `python/syncfit_contracts/catalog/`: `exercises.json`
(~52 exercises, with `how_to`/`tips`), `machines.json` (~51 gym machines with
`weight_factor`), `supplements.json` (~22, with brands/frequency/pregnancy
safety), `symptoms.json` (cramps, low_back_pain, knee_pain, contractions,
dilation).

**Key contracts.** `TelemetryFrame`, `RoutineRequest`/`RoutineResponse`
(exercises_count, time_budget_minutes, energy_level, symptoms, include_warmup;
sets with rest/estimated_seconds), `UserProfile` (body comp, goal_phase,
available_machines, current_supplements, supplement_macros, symptoms,
weekly_training_goal, rest_days_allowance, weight_unit, photo_url),
`SupplementIntake`, `ShareLink`/`SharedProfile`, `CycleCalendar`.

**Run tests.** `pytest python/tests` and, in `typescript/`, `npm i && npm test`.

**Rule.** Additive changes only; bump `VERSION` + `CHANGELOG`; add/extend
`examples/` fixtures; keep schemas valid (tests enforce). Everything in English.

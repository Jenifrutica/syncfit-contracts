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

## Suggested structure

```
syncfit-contracts/
├── schemas/            # JSON Schema files
│   ├── telemetry-frame.schema.json
│   ├── ws-envelope.schema.json
│   ├── adapted-routine.schema.json
│   └── ai-response.schema.json
├── openapi/            # OpenAPI specification
├── python/             # Pydantic models (syncfit_contracts)
├── typescript/         # Generated types and Zod validators
├── examples/           # Fixtures and sample payloads
└── README.md
```

## Stack

Python 3.11+ (Pydantic) and TypeScript (Zod / JSON Schema tooling).

## Tasks

### Requirements

- [ ] Define the JSON Schema for the telemetry frame (PPG at 100 Hz, thermal delta, isometric load).
- [ ] Define the WebSocket message envelope (client → server and server → client).
- [ ] Define the adapted-routine schema returned by the reasoning layer.
- [ ] Define the strict DeepSeek JSON Mode output schema.
- [ ] Publish the OpenAPI specification for all backend REST endpoints.
- [ ] Generate Python models (Pydantic).
- [ ] Generate TypeScript types and Zod validators.
- [ ] Add a versioning strategy and changelog.
- [ ] Add example fixtures used as test data across all repositories.
- [ ] Add schema validation tests.

## Related repositories

- [`syncfit-hardware`](../syncfit-hardware) — produces telemetry frames.
- [`syncfit-backend`](../syncfit-backend) — consumes and validates schemas.
- [`syncfit-core`](../syncfit-core) — feature and model I/O.
- [`syncfit-ai-reasoning`](../syncfit-ai-reasoning) — validates strict AI output.
- [`syncfit-simulator`](../syncfit-simulator) — generates schema-valid test data.
- [`syncfit-frontend`](../syncfit-frontend) — consumes generated TypeScript types.

All code, comments, documentation and commits in this repository are written in English.

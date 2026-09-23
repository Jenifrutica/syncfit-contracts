# Changelog

All notable changes to the SyncFit Edge cross-repository contract are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-09-23

### Added

- `MuscleGroup` and `Language` enums (`EN`, `ES`, `ZH`), `ExerciseImpact` and `LocalizedText`.
- `exercise.schema.json` and `exercise-catalog.schema.json` plus the shared catalog at `python/syncfit_contracts/catalog/exercises.json` (localized names/descriptions, free-use placeholder images, `media_url` reserved for videos).
- `routine-request.schema.json` and `routine-response.schema.json` for muscle-group-based routine generation.
- Optional media/description/muscle-group fields on `ExerciseAdaptation` (`exercise_id`, `muscle_groups`, `impact`, `description`, `image_url`, `media_url`).
- Catalog helpers in Python (`load_exercises`, `get_exercise`, `exercises_for_groups`, `localize`).

## [1.0.0] - 2026-09-22

### Added

- `common.schema.json`: shared definitions (modality, phases, trimesters, biomarkers, exercise adaptation, state graph node and edge).
- `telemetry-frame.schema.json`: fixed-window 100 Hz telemetry frame carried by the Ring Buffer.
- `ws-envelope.schema.json`: WebSocket message envelope for both directions.
- `alert.schema.json`: physiological alert dispatched through the Max-Heap.
- `adapted-routine.schema.json`: adapted prescription delivered to the frontend.
- `ai-response.schema.json`: strict DeepSeek JSON Mode output.
- `range-query-request.schema.json` / `range-query-response.schema.json`: Segment Tree range queries.
- `state-graph.schema.json`: Directed State Graph of cycle phases and trimesters.
- `openapi/openapi.yaml`: REST contract for the backend.
- Python models (Pydantic v2) under `python/syncfit_contracts`.
- TypeScript types and Zod validators under `typescript/src`.
- Example fixtures under `examples/`.
- Validation tests for Python and TypeScript.

[1.0.0]: https://github.com/Jenifrutica/syncfit-contracts/releases/tag/v1.0.0

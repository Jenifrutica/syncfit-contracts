# Changelog

All notable changes to the SyncFit Edge cross-repository contract are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.13.0] - 2026-09-24

### Added

- `Exercise.required_equipment` (equipment keys such as barbell+bench, dumbbell,
  machine, smith), `EQUIPMENT_KEYS`, `exercises_for_equipment()` and
  `exercise_required_equipment()` so routines are filtered by the gym's real
  equipment (machines first, then free weights, then bodyweight).
- `GymStation.equipment_key` / `equipment_type` for gym inventory items beyond machines.

## [1.12.0] - 2026-09-24

### Added

- `Exercise.movement_pattern` and `Exercise.compound`: pattern coverage, duplicate
  avoidance and compound-first ordering. Catalog populated for all exercises.
- `required_patterns()` / `patterns_of()` / `exercises_for_pattern()` and
  `REQUIRED_PATTERNS` (e.g. GLUTES → hinge, lunge, hip_thrust, glute_kickback, hip_abduction).
- `PhysiologicalAssessment` (local-model state consumed by the reasoning layer).
- `symptoms.json` gains `avoid_patterns` (e.g. knee_pain blocks lunge/squat).

## [1.11.0] - 2026-09-24

### Added

- `Exercise.variant_of`: movement family so the UI can offer interchangeable
  variations (e.g. `hip_thrust`: barbell, Smith, machine). Catalog populated for
  all exercises; `variants_of()` / `exercise_family()` helpers.
- `UserProfile.document_id`: national id (cedula), digits only.

## [1.10.0] - 2026-09-24

### Added

- `GymStation.name`/`purpose` are now `LocalizedText` (the admin types in any
  language; the backend fills the other locales) and gained `exercise_ids`.
- `ExerciseAdaptation.machine_id` / `machine_name`: the routine can point to the
  gym machine that handles an exercise (photo, weight factor).

## [1.9.0] - 2026-09-24

### Added

- `GymMembership`, `GymStation` and `JoinedGym` schemas/models/types for the athlete side of gyms.
  - `GymMembership`: one row per (profile, gym) link.
  - `GymStation`: a machine added by a gym admin (distinct from the catalog `GymMachine`).
  - `JoinedGym`: a joined gym with its machines resolved live and an `active` flag.
- `examples/gym-station.json` and `examples/joined-gym.json` fixtures; Python/TS tests.

### Fixed

- TypeScript `SCHEMA_VERSION` was stuck at `1.0.0`; now aligned with the Python/schema version.

## [1.8.0] - 2026-09-24

### Added

- `pain_levels` map (per symptom 1-10 plus `OVERALL`) and `symptom_notes` on `UserProfile`.

## [1.7.0] - 2026-09-24

### Added

- `symptoms.json` catalog with `avoid_keywords`, `impact_cap`, localized `advice` and an
  `block_training` absolute-contraindication flag.

## [1.6.0] - 2026-09-24

### Added

- `how_to` and `tips` on exercises and adaptations (movement detail).
- `supplement_macros` on `UserProfile` (user-entered nutrition facts).
- 14 more machines (belt squat, pendulum, V-squat, glute drive, hip abduction/adduction, seated row, shoulder press, pec deck, preacher, GHD, functional trainer, cable crossover) and 8 more exercises.

## [1.5.0] - 2026-09-24

### Added

- `ShareRole`, `SharePermission`, `WeightUnit`; `ShareLink` and `SharedProfile` schemas for guest sharing.
- `current_supplements`, `weight_unit` and `photo_url` on `UserProfile`.

## [1.4.0] - 2026-09-24

### Added

- `SupplementFrequency` and supplement `is_daily`/`brand_examples` (illustrative, not endorsements).
- `SupplementIntake` schema for daily intake tracking.
- `weekly_training_goal` and `rest_days_allowance` on `UserProfile` (streak wildcards).
- +10 supplements (mass gainer, fat burner, L-carnitine, BCAA, beta-alanine, citrulline, zinc, vitamin C, ashwagandha, glutamine).

## [1.3.0] - 2026-09-24

### Added

- `EquipmentType` and `GoalPhase` enums; `Exercise.equipment_type`; `ExerciseLoad` machine/unit.
- Gym machine catalog (`machines.json`) with per-machine `weight_factor` and the `gym-machine` schema.
- `CycleCalendar` schema (cycle days, strength days, ovulation, low impact).
- Body composition and goal fields on `UserProfile` (`body_fat_pct`, `daily_calories`, `goal_phase`, `available_machines`).
- `daily_macros` on supplement advice plus goal/body fields on the request.
- +13 exercises (assisted pull-up/chin-up/dip, smith/machine squat and hip thrust, hack squat, leg press, chest/cable fly, pull-up, dip).

## [1.2.0] - 2026-09-23

### Added

- Timing and set structure: `SetType`, `SetPrescription`, `ExerciseRole`; `ExerciseAdaptation` now carries `sets` (warm-up/activation/approximation/effective), `rest_seconds`, `estimated_seconds` and `role`.
- Routine timing: `exercises_count`, `time_budget_minutes`, `energy_level`, `objective`, `include_warmup` on the request; `total_estimated_minutes` and `warmup` on the response.
- `EnergyLevel`, `UserObjective`, `ExerciseLoad`, `UserProfile` and `EnergyCheckIn` (guest or registered accounts with baseline loads).
- Supplements: `Supplement`, `SupplementRequest`, `SupplementAdvice` plus the localized supplement catalog with pregnancy safety, dosage and macros (`supplements.json`).
- 6 warm-up/activation exercises (e.g. band glute activation, cat-cow, bird dog).
- Schemas, fixtures and tests (Python + TypeScript).

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

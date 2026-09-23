import { z } from "zod";
import {
  ExerciseAdaptation,
  EnergyLevel,
  FatigueLevel,
  InferredPhase,
  Language,
  Modality,
  MuscleGroup,
  SCHEMA_VERSION,
  SchemaVersion,
  UserObjective,
  Uuid,
} from "./common.js";
import { TelemetryFrame } from "./telemetry.js";

export const AdaptedRoutine = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: Uuid,
    phase_inferred: InferredPhase,
    fatigue_level: FatigueLevel,
    k_load_multiplier: z.number().min(0.7).max(1.05),
    alerts: z.array(z.string()),
    adapted_routine: z.array(ExerciseAdaptation),
  })
  .strict();
export type AdaptedRoutine = z.infer<typeof AdaptedRoutine>;

export const RoutineRequest = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: Uuid.optional(),
    muscle_groups: z.array(MuscleGroup).min(1).max(4),
    language: Language.default("EN"),
    modality: Modality.optional(),
    day_or_week: z.number().int().min(1).max(42).optional(),
    telemetry: TelemetryFrame.optional(),
    exercises_per_group: z.number().int().min(1).max(8).optional(),
    exercises_count: z.number().int().min(1).max(12).optional(),
    time_budget_minutes: z.number().int().min(10).max(180).optional(),
    energy_level: EnergyLevel.optional(),
    objective: UserObjective.optional(),
    include_warmup: z.boolean().optional(),
  })
  .strict();
export type RoutineRequest = z.infer<typeof RoutineRequest>;

export const RoutineResponse = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: Uuid.optional(),
    language: Language.default("EN"),
    muscle_groups: z.array(MuscleGroup).min(1),
    phase_inferred: InferredPhase.optional(),
    fatigue_level: FatigueLevel.optional(),
    k_load_multiplier: z.number().min(0.7).max(1.05).optional(),
    alerts: z.array(z.string()),
    total_estimated_minutes: z.number().min(0).optional(),
    warmup: z.array(ExerciseAdaptation).optional(),
    routine: z.array(ExerciseAdaptation),
  })
  .strict();
export type RoutineResponse = z.infer<typeof RoutineResponse>;

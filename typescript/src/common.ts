import { z } from "zod";

export const SCHEMA_VERSION = "1.0.0" as const;

export const SchemaVersion = z
  .string()
  .regex(/^[0-9]+\.[0-9]+\.[0-9]+$/, "must be a semantic version");

export const Timestamp = z.string().datetime({ offset: true });

export const Uuid = z.string().uuid();

export const Modality = z.enum(["MENSTRUAL_CYCLE", "GESTATIONAL"]);
export type Modality = z.infer<typeof Modality>;

export const CyclePhase = z.enum([
  "MENSTRUAL",
  "FOLLICULAR",
  "OVULATORY",
  "LUTEAL",
]);
export type CyclePhase = z.infer<typeof CyclePhase>;

export const Trimester = z.enum(["TRIMESTER_1", "TRIMESTER_2", "TRIMESTER_3"]);
export type Trimester = z.infer<typeof Trimester>;

export const InferredPhase = z.enum([
  "MENSTRUAL",
  "FOLLICULAR",
  "OVULATORY",
  "LUTEAL",
  "TRIMESTER_1",
  "TRIMESTER_2",
  "TRIMESTER_3",
]);
export type InferredPhase = z.infer<typeof InferredPhase>;

export const FatigueLevel = z.enum(["LOW", "MEDIUM", "HIGH"]);
export type FatigueLevel = z.infer<typeof FatigueLevel>;

export const AlertSeverity = z.enum(["INFO", "WARNING", "CRITICAL"]);
export type AlertSeverity = z.infer<typeof AlertSeverity>;

export const Biomarkers = z
  .object({
    delta_temperature_c: z.number().min(-2).max(2),
    rmssd_hrv_ms: z.number().min(0).max(300),
    isometric_force_loss_pct: z.number().min(0).max(100),
  })
  .strict();
export type Biomarkers = z.infer<typeof Biomarkers>;

export const ExerciseAdaptation = z
  .object({
    exercise_original: z.string(),
    blocked: z.boolean(),
    block_reason: z.string(),
    exercise_substitute: z.string(),
    series_adapted: z.number().int().min(0).max(20),
    reps_adapted: z.number().int().min(0).max(100),
    weight_suggested_kg: z.number().min(0),
  })
  .strict();
export type ExerciseAdaptation = z.infer<typeof ExerciseAdaptation>;

export const PhysiologicalState = z
  .object({
    id: z.string(),
    state: InferredPhase,
    kind: z.enum(["CYCLE_PHASE", "TRIMESTER"]),
    label: z.string(),
  })
  .strict();
export type PhysiologicalState = z.infer<typeof PhysiologicalState>;

export const StateTransition = z
  .object({
    from: z.string(),
    to: z.string(),
    weight: z.number().min(0).max(1),
    condition: z.string().optional(),
  })
  .strict();
export type StateTransition = z.infer<typeof StateTransition>;

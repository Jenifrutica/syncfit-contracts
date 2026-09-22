import { z } from "zod";
import {
  ExerciseAdaptation,
  FatigueLevel,
  InferredPhase,
  SCHEMA_VERSION,
  SchemaVersion,
  Uuid,
} from "./common.js";

export const AIReasoningResponse = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: Uuid.optional(),
    phase_inferred: InferredPhase,
    fatigue_level: FatigueLevel,
    articular_risk_pct: z.number().min(0).max(100),
    k_load_multiplier: z.number().min(0.7).max(1.05),
    alerts: z.array(z.string()),
    adapted_routine: z.array(ExerciseAdaptation),
  })
  .strict();
export type AIReasoningResponse = z.infer<typeof AIReasoningResponse>;

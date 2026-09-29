import { z } from "zod";
import { FatigueLevel, InferredPhase, SchemaVersion, SCHEMA_VERSION } from "./common.js";

export const PhysiologicalAssessment = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: z.string().optional(),
    phase_inferred: InferredPhase,
    fatigue_level: FatigueLevel,
    k_load_multiplier: z.number().min(0.7).max(1.05),
    autonomic_status: z.string().default("BALANCED"),
    articular_risk_pct: z.number().min(0).max(100).optional(),
    contraindicated_patterns: z.array(z.string()).optional(),
    notes: z.array(z.string()).optional(),
    source: z.enum(["core", "deepseek"]).default("core"),
  })
  .strict();
export type PhysiologicalAssessment = z.infer<typeof PhysiologicalAssessment>;

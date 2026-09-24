import { z } from "zod";
import {
  GoalPhase,
  Language,
  LocalizedText,
  MacroNutrients,
  Modality,
  SCHEMA_VERSION,
  SchemaVersion,
  SupplementCategory,
  SupplementFrequency,
  SupplementSafety,
  UserObjective,
  Uuid,
} from "./common.js";

export const Supplement = z
  .object({
    id: z.string(),
    name: LocalizedText,
    category: SupplementCategory,
    dosage: LocalizedText,
    macros: MacroNutrients,
    objectives: z.array(UserObjective),
    safety_general: SupplementSafety,
    safety_pregnancy: SupplementSafety,
    notes: LocalizedText,
    frequency: SupplementFrequency.optional(),
    is_daily: z.boolean().optional(),
    brand_examples: z.array(z.string()).optional(),
    image_url: z.string().optional(),
  })
  .strict();
export type Supplement = z.infer<typeof Supplement>;

export const SupplementIntake = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    profile_id: Uuid,
    supplement_id: z.string(),
    date: z.string(),
    taken: z.boolean(),
  })
  .strict();
export type SupplementIntake = z.infer<typeof SupplementIntake>;

export const SupplementRequest = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    language: Language.default("EN"),
    modality: Modality,
    objective: UserObjective.optional(),
    goal_phase: GoalPhase.optional(),
    week: z.number().int().min(1).max(42).optional(),
    weight_kg: z.number().min(20).max(300).optional(),
    height_cm: z.number().min(80).max(250).optional(),
    body_fat_pct: z.number().min(3).max(60).optional(),
    age: z.number().int().min(10).max(100).optional(),
    daily_calories: z.number().int().min(800).max(6000).optional(),
  })
  .strict();
export type SupplementRequest = z.infer<typeof SupplementRequest>;

export const SupplementAdviceItem = z
  .object({
    supplement_id: z.string(),
    name: LocalizedText,
    category: SupplementCategory,
    safety: SupplementSafety,
    dosage: LocalizedText,
    macros: MacroNutrients,
    reason: LocalizedText,
    image_url: z.string().optional(),
  })
  .strict();
export type SupplementAdviceItem = z.infer<typeof SupplementAdviceItem>;

export const SupplementAdvice = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    language: Language.default("EN"),
    modality: Modality.optional(),
    objective: UserObjective.optional(),
    goal_phase: GoalPhase.optional(),
    daily_macros: MacroNutrients.optional(),
    items: z.array(SupplementAdviceItem),
  })
  .strict();
export type SupplementAdvice = z.infer<typeof SupplementAdvice>;

import { z } from "zod";
import {
  EnergyLevel,
  ExerciseLoad,
  GoalPhase,
  Language,
  MacroNutrients,
  Modality,
  SCHEMA_VERSION,
  SchemaVersion,
  Timestamp,
  UserObjective,
  Uuid,
} from "./common.js";

export const UserProfile = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    profile_id: Uuid,
    display_name: z.string().min(1),
    language: Language.default("EN"),
    is_guest: z.boolean().optional(),
    height_cm: z.number().min(80).max(250).optional(),
    weight_kg: z.number().min(20).max(300).optional(),
    body_fat_pct: z.number().min(3).max(60).optional(),
    daily_calories: z.number().int().min(800).max(6000).optional(),
    age: z.number().int().min(10).max(100).optional(),
    objective: UserObjective.optional(),
    goal_phase: GoalPhase.optional(),
    modality: Modality.optional(),
    available_machines: z.array(z.string()).optional(),
    symptoms: z.array(z.string()).optional(),
    current_supplements: z.array(z.string()).optional(),
    supplement_macros: z
      .array(z.object({ supplement_id: z.string(), macros: MacroNutrients }).strict())
      .optional(),
    weight_unit: z.enum(["KG", "LB"]).optional(),
    photo_url: z.string().optional(),
    weekly_training_goal: z.number().int().min(1).max(7).optional(),
    rest_days_allowance: z.number().int().min(0).max(7).optional(),
    loads: z.array(ExerciseLoad).optional(),
  })
  .strict();
export type UserProfile = z.infer<typeof UserProfile>;

export const EnergyCheckIn = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    profile_id: Uuid.optional(),
    session_id: Uuid.optional(),
    timestamp: Timestamp,
    energy_level: EnergyLevel,
    modality: Modality,
    day_or_week: z.number().int().min(1).max(42).optional(),
    notes: z.string().optional(),
  })
  .strict();
export type EnergyCheckIn = z.infer<typeof EnergyCheckIn>;

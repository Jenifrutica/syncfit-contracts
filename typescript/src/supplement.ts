import { z } from "zod";
import {
  Language,
  LocalizedText,
  MacroNutrients,
  Modality,
  SCHEMA_VERSION,
  SchemaVersion,
  SupplementCategory,
  SupplementSafety,
  UserObjective,
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
    image_url: z.string().optional(),
  })
  .strict();
export type Supplement = z.infer<typeof Supplement>;

export const SupplementRequest = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    language: Language.default("EN"),
    modality: Modality,
    objective: UserObjective.optional(),
    week: z.number().int().min(1).max(42).optional(),
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
    items: z.array(SupplementAdviceItem),
  })
  .strict();
export type SupplementAdvice = z.infer<typeof SupplementAdvice>;

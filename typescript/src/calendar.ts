import { z } from "zod";
import {
  InferredPhase,
  LocalizedText,
  Modality,
  SCHEMA_VERSION,
  SchemaVersion,
} from "./common.js";

export const CalendarKind = z.enum(["CYCLE", "OVULATION", "STRENGTH", "LOW_IMPACT", "REST"]);
export type CalendarKind = z.infer<typeof CalendarKind>;

export const CalendarDay = z
  .object({
    date: z.string(),
    kind: CalendarKind,
    cycle_day: z.number().int().optional(),
    phase: InferredPhase.optional(),
    label: LocalizedText.optional(),
    note: LocalizedText.optional(),
  })
  .strict();
export type CalendarDay = z.infer<typeof CalendarDay>;

export const CycleCalendar = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    month: z.string(),
    modality: Modality.optional(),
    days: z.array(CalendarDay),
  })
  .strict();
export type CycleCalendar = z.infer<typeof CycleCalendar>;

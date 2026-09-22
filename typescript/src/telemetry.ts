import { z } from "zod";
import {
  Biomarkers,
  Modality,
  SCHEMA_VERSION,
  SchemaVersion,
  Timestamp,
  Uuid,
} from "./common.js";

export const PpgWindow = z
  .object({
    sample_rate_hz: z.literal(100),
    window_size: z.number().int().min(1).optional(),
    samples: z.array(z.number()).min(1),
  })
  .strict();
export type PpgWindow = z.infer<typeof PpgWindow>;

export const TelemetryFrame = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    device_id: z.string().min(1),
    session_id: Uuid,
    timestamp: Timestamp,
    modality: Modality,
    day_or_week: z.number().int().min(1).max(42),
    biomarkers: Biomarkers,
    ppg_window: PpgWindow,
  })
  .strict();
export type TelemetryFrame = z.infer<typeof TelemetryFrame>;

import { z } from "zod";
import { AlertSeverity, SCHEMA_VERSION, SchemaVersion, Timestamp, Uuid } from "./common.js";

export const AlertCode = z.enum([
  "RMSSD_DROP",
  "CORE_TEMP_RISE",
  "CNS_FATIGUE",
  "ARTICULAR_RISK",
  "SENSOR_FAULT",
]);
export type AlertCode = z.infer<typeof AlertCode>;

export const PhysiologicalAlert = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    alert_id: Uuid,
    session_id: Uuid,
    timestamp: Timestamp,
    severity: AlertSeverity,
    code: AlertCode,
    message: z.string(),
    metric: z.string().optional(),
    value: z.number().optional(),
    threshold: z.number().optional(),
  })
  .strict();
export type PhysiologicalAlert = z.infer<typeof PhysiologicalAlert>;

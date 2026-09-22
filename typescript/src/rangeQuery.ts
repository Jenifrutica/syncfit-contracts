import { z } from "zod";
import { SCHEMA_VERSION, SchemaVersion, Uuid } from "./common.js";

export const Metric = z.enum(["temperature", "rmssd", "isometric_force_loss"]);
export type Metric = z.infer<typeof Metric>;

export const Aggregation = z.enum(["min", "max", "mean"]);
export type Aggregation = z.infer<typeof Aggregation>;

export const RangeQueryRequest = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: Uuid,
    metric: Metric,
    start_index: z.number().int().min(0),
    end_index: z.number().int().min(0),
    aggregation: Aggregation,
  })
  .strict();
export type RangeQueryRequest = z.infer<typeof RangeQueryRequest>;

export const RangeQueryResponse = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    session_id: Uuid,
    metric: Metric,
    start_index: z.number().int().min(0),
    end_index: z.number().int().min(0),
    aggregation: Aggregation,
    value: z.number(),
    count: z.number().int().min(0),
  })
  .strict();
export type RangeQueryResponse = z.infer<typeof RangeQueryResponse>;

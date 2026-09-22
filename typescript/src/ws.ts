import { z } from "zod";
import { SCHEMA_VERSION, SchemaVersion, Timestamp, Uuid } from "./common.js";

export const WsMessageType = z.enum([
  "telemetry",
  "alert",
  "prescription",
  "ack",
  "error",
  "ping",
  "pong",
]);
export type WsMessageType = z.infer<typeof WsMessageType>;

export const WsEnvelope = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    type: WsMessageType,
    timestamp: Timestamp,
    session_id: Uuid.optional(),
    correlation_id: z.string().optional(),
    payload: z.record(z.unknown()),
  })
  .strict();
export type WsEnvelope = z.infer<typeof WsEnvelope>;

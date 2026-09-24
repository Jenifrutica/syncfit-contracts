import { z } from "zod";
import {
  SCHEMA_VERSION,
  SchemaVersion,
  SharePermission,
  ShareRole,
  Timestamp,
} from "./common.js";

export const ShareLink = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    token: z.string(),
    role: ShareRole,
    label: z.string().optional(),
    permissions: z.array(SharePermission),
    active: z.boolean().default(true),
    created_at: Timestamp.optional(),
    updated_at: Timestamp.optional(),
  })
  .strict();
export type ShareLink = z.infer<typeof ShareLink>;

export const SharedProfile = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    owner_display_name: z.string(),
    owner_photo_url: z.string().nullable().optional(),
    role: ShareRole,
    permissions: z.array(SharePermission),
    updated_at: Timestamp.optional(),
    profile: z.record(z.unknown()).nullable().optional(),
    timeline: z.record(z.unknown()).nullable().optional(),
    routine: z.record(z.unknown()).nullable().optional(),
    calendar: z.record(z.unknown()).nullable().optional(),
    machines: z.array(z.unknown()).nullable().optional(),
    loads: z.array(z.unknown()).nullable().optional(),
    supplements: z.array(z.unknown()).nullable().optional(),
  })
  .strict();
export type SharedProfile = z.infer<typeof SharedProfile>;

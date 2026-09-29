import { z } from "zod";
import { LocalizedText } from "./common.js";

export const GymStation = z
  .object({
    id: z.string(),
    gym_id: z.string(),
    name: LocalizedText,
    weight_factor: z.number().min(0),
    purpose: LocalizedText.nullable().optional(),
    exercise_ids: z.array(z.string()).optional(),
    equipment_key: z.string().nullable().optional(),
    equipment_type: z.string().nullable().optional(),
    image_url: z.string().nullable().optional(),
  })
  .strict();
export type GymStation = z.infer<typeof GymStation>;

export const GymMembership = z
  .object({
    profile_id: z.string(),
    gym_id: z.string(),
    created_at: z.string().optional(),
  })
  .strict();
export type GymMembership = z.infer<typeof GymMembership>;

export const JoinedGym = z
  .object({
    gym_id: z.string(),
    name: z.string(),
    code: z.string(),
    active: z.boolean(),
    joined_at: z.string().optional(),
    machines: z.array(GymStation),
  })
  .strict();
export type JoinedGym = z.infer<typeof JoinedGym>;

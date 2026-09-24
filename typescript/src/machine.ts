import { z } from "zod";
import { EquipmentType, LocalizedText } from "./common.js";

export const GymMachine = z
  .object({
    id: z.string(),
    name: LocalizedText,
    type: EquipmentType,
    exercises: z.array(z.string()),
    weight_factor: z.number().min(0),
    unit: z.string().optional(),
    notes: LocalizedText,
    image_url: z.string().optional(),
  })
  .strict();
export type GymMachine = z.infer<typeof GymMachine>;

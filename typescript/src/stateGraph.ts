import { z } from "zod";
import {
  PhysiologicalState,
  SCHEMA_VERSION,
  SchemaVersion,
  StateTransition,
} from "./common.js";

export const PhysiologicalStateGraph = z
  .object({
    schema_version: SchemaVersion.default(SCHEMA_VERSION),
    nodes: z.array(PhysiologicalState).min(1),
    edges: z.array(StateTransition),
  })
  .strict();
export type PhysiologicalStateGraph = z.infer<typeof PhysiologicalStateGraph>;

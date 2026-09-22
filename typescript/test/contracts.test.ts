import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { describe, expect, it } from "vitest";

import {
  AdaptedRoutine,
  AIReasoningResponse,
  PhysiologicalAlert,
  PhysiologicalStateGraph,
  RangeQueryRequest,
  RangeQueryResponse,
  TelemetryFrame,
  WsEnvelope,
} from "../src/index.js";

const here = dirname(fileURLToPath(import.meta.url));
const examplesDir = resolve(here, "../../examples");

function load(name: string): unknown {
  return JSON.parse(readFileSync(resolve(examplesDir, name), "utf-8"));
}

const cases: Array<[string, { parse: (v: unknown) => unknown }]> = [
  ["telemetry-menstrual-ovulatory.json", TelemetryFrame],
  ["telemetry-gestational.json", TelemetryFrame],
  ["ws-envelope-telemetry.json", WsEnvelope],
  ["ai-response-ovulatory-block.json", AIReasoningResponse],
  ["ai-response-gestational.json", AIReasoningResponse],
  ["adapted-routine.json", AdaptedRoutine],
  ["alert-critical.json", PhysiologicalAlert],
  ["range-query-request.json", RangeQueryRequest],
  ["range-query-response.json", RangeQueryResponse],
  ["state-graph.json", PhysiologicalStateGraph],
];

describe("contracts validate the shared examples", () => {
  it.each(cases)("%s", (_name, schema) => {
    expect(() => schema.parse(load(_name))).not.toThrow();
  });
});

describe("strictness", () => {
  it("rejects an out-of-range k_load_multiplier", () => {
    const payload = load("adapted-routine.json") as Record<string, unknown>;
    payload.k_load_multiplier = 1.5;
    expect(() => AdaptedRoutine.parse(payload)).toThrow();
  });

  it("rejects unknown fields", () => {
    const payload = load("alert-critical.json") as Record<string, unknown>;
    payload.unexpected = true;
    expect(() => PhysiologicalAlert.parse(payload)).toThrow();
  });
});

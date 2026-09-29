import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { describe, expect, it } from "vitest";

import {
  AdaptedRoutine,
  AIReasoningResponse,
  CycleCalendar,
  EnergyCheckIn,
  Exercise,
  GymMachine,
  GymStation,
  PhysiologicalAssessment,
  JoinedGym,
  LocalizedText,
  PhysiologicalAlert,
  PhysiologicalStateGraph,
  RangeQueryRequest,
  RangeQueryResponse,
  RoutineRequest,
  RoutineResponse,
  Supplement,
  SupplementAdvice,
  ShareLink,
  SharedProfile,
  SupplementIntake,
  SupplementRequest,
  TelemetryFrame,
  UserProfile,
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
  ["exercise.json", Exercise],
  ["routine-request.json", RoutineRequest],
  ["routine-response.json", RoutineResponse],
  ["user-profile.json", UserProfile],
  ["energy-checkin.json", EnergyCheckIn],
  ["supplement.json", Supplement],
  ["supplement-request.json", SupplementRequest],
  ["supplement-advice.json", SupplementAdvice],
  ["gym-machine.json", GymMachine],
  ["gym-station.json", GymStation],
  ["joined-gym.json", JoinedGym],
  ["physiological-assessment.json", PhysiologicalAssessment],
  ["cycle-calendar.json", CycleCalendar],
  ["supplement-intake.json", SupplementIntake],
  ["share-link.json", ShareLink],
  ["shared-profile.json", SharedProfile],
];

describe("contracts validate the shared examples", () => {
  it.each(cases)("%s", (_name, schema) => {
    expect(() => schema.parse(load(_name))).not.toThrow();
  });
});

describe("muscle groups and localization", () => {
  it("rejects an unknown muscle group", () => {
    const payload = load("routine-request.json") as Record<string, unknown>;
    payload.muscle_groups = ["NOT_A_GROUP"];
    expect(() => RoutineRequest.parse(payload)).toThrow();
  });

  it("requires English in localized text", () => {
    expect(() => LocalizedText.parse({ es: "solo español" })).toThrow();
    expect(() => LocalizedText.parse({ en: "ok", es: "bien", zh: "好" })).not.toThrow();
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


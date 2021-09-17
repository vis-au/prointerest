import type { DoiInteraction } from "$lib/provenance/doi-interaction";
import type DataItem from "$lib/types/data-item";
import type { OutliernessMeasure } from "$lib/types/outlier-measures";
import type { ProvenanceConfig } from "$lib/types/provenance-config";
import { scagnostics } from "$lib/types/scagnostics";
import { dataItemToList } from "./item-transform";
import { mapToRecord } from "./map-to-record";

const BASE_URL = "http://127.0.0.1:5000";

type RequestMethod = "GET" | "POST" | "PUT" | "DELETE";

async function sendRequestToBaseURL(
  path: string,
  method: RequestMethod = "GET",
  body?: Record<string, unknown>
) {
  if (body === undefined) {
    return fetch(`${BASE_URL}${path}`, { method }).then((d) => d.json());
  } else {
    return fetch(`${BASE_URL}${path}`, { method, body: JSON.stringify(body) }).then((d) =>
      d.json()
    );
  }
}

function configToURLParams(config: Record<string, number>) {
  let params = "";
  const keys = Object.keys(config);
  keys.forEach((key, i) => {
    const value = config[key];
    params += `${key}=${value}`;
    if (i < keys.length - 1) {
      params += "&";
    }
  });
  return params;
}

// DATA ACCESS
export async function getTotalDatasize(): Promise<number> {
  return sendRequestToBaseURL("/size");
}

export async function getDimensionNames(): Promise<string[]> {
  return sendRequestToBaseURL("/dimensions");
}

export async function getDimensionExtent(dimension: string): Promise<{ min: number; max: number }> {
  return sendRequestToBaseURL(`/extent/${dimension}`);
}

export async function getNextChunk(
  chunkSize: number
): Promise<{ chunk: number[][]; doi: number[] }> {
  return sendRequestToBaseURL(`/next_chunk?size=${chunkSize}`);
}

export async function sendReset(): Promise<void> {
  return sendRequestToBaseURL("/reset");
}

// DOI FUNCTION
type DoiComponent = "prior" | "posterior";
export async function sendWeights(
  component: DoiComponent,
  weights: Map<string, number>
): Promise<void> {
  const record = mapToRecord(weights);
  return sendRequestToBaseURL(`/weights/${component}`, "POST", { weights: record });
}

export async function sendComponentWeights(weights: Map<string, number>): Promise<void> {
  const record = mapToRecord(weights);
  return sendRequestToBaseURL("/weights/components", "POST", { weights: record });
}

export async function sendScagnosticWeights(weights: Map<string, number>): Promise<void> {
  // make sure that every scagnostic is assigned a weight
  const copy = new Map(weights);
  scagnostics.forEach((s) => {
    if (copy.get(s) === undefined) {
      copy.set(s, 0);
    }
  });
  const record = mapToRecord(copy);
  return sendRequestToBaseURL("/weights/scagnostics", "POST", { weights: record });
}

export async function sendInterestingDimensions(dimensions: string[]): Promise<void> {
  return sendRequestToBaseURL("/dimensions", "POST", { dimensions });
}

export async function sendInterestingDimensionRange(
  dimension: string,
  range: [number, number]
): Promise<void> {
  return sendRequestToBaseURL("/dimension_range", "POST", {
    dimension,
    min: range[0],
    max: range[1]
  });
}

export async function sendAxisDimension(axis: "x" | "y", dimension: string): Promise<void> {
  return sendRequestToBaseURL(`/axis?axis=${axis}&dimension=${dimension}`);
}

export async function sendOutlierMetric(metric: OutliernessMeasure): Promise<void> {
  return sendRequestToBaseURL(`/config/outlierness?metric=${metric}`, "POST");
}

export async function sendProvenanceConfig(config: ProvenanceConfig): Promise<void> {
  return sendRequestToBaseURL(`/config/provenance?${configToURLParams(config)}`, "POST");
}

export async function sendProvenanceWeights(weights: Map<string, number>): Promise<void> {
  const record = mapToRecord(weights);
  return sendRequestToBaseURL(`/weights/provenance`, "POST", { weights: record });
}

export async function sendSelectedItems(items: DataItem[]): Promise<void> {
  const values = items.map(dataItemToList);
  return sendRequestToBaseURL("/selected_items", "POST", { items: values });
}

export function sendInteraction(interaction: DoiInteraction): Promise<void> {
  const ids = interaction.getAffectedItems().map((d) => d.id);
  const mode = interaction.mode;
  return sendRequestToBaseURL("/interaction", "POST", { mode, ids });
}

export async function getDoiValues(items: DataItem[]): Promise<[number, number][]> {
  const values = items.map(dataItemToList);
  return sendRequestToBaseURL("/doi", "POST", { items: values });
}

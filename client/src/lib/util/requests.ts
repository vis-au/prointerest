import type DataItem from "$lib/types/data-item";
import type { OutliernessMeasure } from "$lib/types/outlier-measures";
import { scagnostics } from "$lib/types/scagnostics";
import { mapToRecord } from "./map-to-record";

const BASE_URL = "http://127.0.0.1:5000";

type RequestMethod = "GET" | "POST" | "PUT" | "DELETE";


async function sendRequestToBaseURL(path: string, method: RequestMethod="GET", body?: Record<string, unknown>) {
  if (body === undefined) {
    return fetch(`${BASE_URL}${path}`, { method })
      .then(d => d.json());
  } else {
    return fetch(`${BASE_URL}${path}`, { method, body: JSON.stringify(body) })
      .then(d => d.json());
  }
}

// DATA ACCESS
export async function getTotalDatasize(): Promise<number> {
  return sendRequestToBaseURL("/size");
}

export async function getDimensionNames(): Promise<string[]> {
  return sendRequestToBaseURL("/dimensions");
}

export async function getNextChunk(chunkSize: number): Promise<number[][]> {
  return sendRequestToBaseURL(`/next_chunk?size=${chunkSize}`);
}

export async function resetProgression(): Promise<void> {
  return sendRequestToBaseURL("/reset");
}


// DOI FUNCTION
type DoiComponent = "prior"|"posterior";
export async function sendWeights(component: DoiComponent, weights: Map<string, number>): Promise<void> {
  const record = mapToRecord(weights);
  return sendRequestToBaseURL(`/weights/${component}`, "POST", { weights: record });
}

export async function sendScagnosticWeights(weights: Map<string, number>): Promise<void> {
  // make sure that every scagnostic is assigned a weight
  const copy = new Map(weights);
  scagnostics.forEach(s => {
    if (copy.get(s) === undefined) {
      copy.set(s, 0);
    }
  })
  const record = mapToRecord(copy);
  return sendRequestToBaseURL("/weights/scagnostics", "POST", { weights: record });
}

export async function sendInterestingDimensions(dimensions: string[]): Promise<void> {
  return sendRequestToBaseURL("/dimensions", "POST", { dimensions });
}

export async function sendOutlierMetric(metric: OutliernessMeasure): Promise<void> {
  return sendRequestToBaseURL(`/outlierness_metric?metric=${metric}`);
}

export async function sendSelectedItems(items: DataItem[]): Promise<void> {
  return sendRequestToBaseURL("/selected_items", "POST", { items });
}

export async function sendInterestingItems(ids: string[], doi: number[]): Promise<void> {
  return sendRequestToBaseURL("/interesting_ids", "POST", { ids, doi });
}

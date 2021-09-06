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

export async function sendInterestingItems(ids: string[], doi: number[]): Promise<void> {
  return sendRequestToBaseURL("/interesting_ids", "POST", { ids, doi });
}

const BASE_URL = "http://127.0.0.1:5000";


async function sendRequestToBaseURL(path: string) {
  return fetch(`${BASE_URL}${path}`)
    .then(d => d.json());
}

export async function getDimensionNames(): Promise<string[]> {
  return sendRequestToBaseURL("/dimensions");
}

export async function getNextChunk(): Promise<number[][]> {
  return sendRequestToBaseURL("/next_chunk");
}
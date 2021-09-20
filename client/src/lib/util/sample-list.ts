// returns true with a probability such that "sampleSize" items will be retrieved from "items".
// This is done to ensure that the histograms render in acceptable time later in the progression.
export function sample(probability: number): boolean {
  return Math.random() < probability;
}

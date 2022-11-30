// Flip a weighted coin that with the provided probability returns true.
export function sample(probability: number): boolean {
  return Math.random() < probability;
}

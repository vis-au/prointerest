import { selectedDoiInterpolationFunction } from "$lib/state/selected-doi-interpolation-function";
import { doiInterpolationFunctions } from "$lib/types/doi-interpolation-function";
import type { DoiInterpolationFunction } from "$lib/types/doi-interpolation-function";

let currentFunction: DoiInterpolationFunction = null;
selectedDoiInterpolationFunction.subscribe(
  (f) => (currentFunction = doiInterpolationFunctions.get(f))
);

export function getInterpolatedDoiValue(prior: number): number {
  return currentFunction(prior);
}

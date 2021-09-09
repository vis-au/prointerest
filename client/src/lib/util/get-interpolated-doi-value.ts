import { selectedDoiInterpolationFunction } from "$lib/state/selected-doi-interpolation-function";
import type { DoiInterpolationFunction } from "$lib/types/doi-interpolation-function";

let currentInterpolationFunction: DoiInterpolationFunction = null;
selectedDoiInterpolationFunction.subscribe(f => currentInterpolationFunction = f);

export function getInterpolatedDoiValue(prior: number): number {
  return currentInterpolationFunction(prior);
}
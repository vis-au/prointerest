import type { OutliernessMeasure } from "$lib/types/outlier-measures"
import { writable } from "svelte/store";

const currentMeasure: OutliernessMeasure = "scagnostic";

export const selectedOutlierMeasure = writable(currentMeasure);
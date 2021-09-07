import type { OutliernessMeasure } from "$lib/types/outlier-measures";
import { sendOutlierMetric } from "$lib/util/requests";
import { writable } from "svelte/store";

const currentMeasure = "scagnostic" as OutliernessMeasure;

export const selectedOutlierMeasure = writable(currentMeasure);

selectedOutlierMeasure.subscribe(sendOutlierMetric);

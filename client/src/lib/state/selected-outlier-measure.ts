import type { OutliernessMeasure } from '$lib/types/outlier-measures';
import { writable } from 'svelte/store';

const currentMeasure = 'scagnostic' as OutliernessMeasure;

export const selectedOutlierMeasure = writable(currentMeasure);

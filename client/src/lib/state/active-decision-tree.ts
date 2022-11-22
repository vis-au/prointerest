import { writable } from "svelte/store";

export const activeDecisionTree = writable({} as Record<string, unknown>);
import type { DecisionTree } from "$lib/types/decision-tree";
import { writable } from "svelte/store";

export const activeDecisionTree = writable(null as DecisionTree);
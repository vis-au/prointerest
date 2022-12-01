import type { DecisionTree } from "$lib/types/decision-tree";
import { writable } from "svelte/store";

export const activeDecisionTreePath = writable([] as DecisionTree[]);  // list of dt nodes
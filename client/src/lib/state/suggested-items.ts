import { writable } from "svelte/store";
import type { Writable } from "svelte/store";
import InteractionObserver from "$lib/provenance/interaction-observer";
import SuggestionProvider from "$lib/provenance/suggestion-provider";
import type DataItem from "$lib/types/data-item";
import type { SuggestionInput, SuggestionOutput } from "$lib/types/suggestion-mode";
import { getPointsInR } from "$lib/util/find-in-quadtree";
import { activeSuggestionInput, activeSuggestionOutput } from "./active-suggestion-modes";
import { quadtree } from "./quadtree";
import { interestingDimensions } from "./interesting-dimensions";
import { dimensions } from "./processed-data";
import { exploredItems } from "./explored-items";
import { interestingItems } from "./interesting-items";

const interactionObserver = new InteractionObserver(getPointsInR);
const suggestionProvider = new SuggestionProvider();

let currentlyInterestingItems: DataItem[] = [];
let currentlyExploredItems: DataItem[] = [];
let currentInputMode: SuggestionInput = null;
let currentOutputMode: SuggestionOutput = null;

let currenDimensions: string[] = [];

export const suggestedItems: Writable<DataItem[]> = writable([]);

function updateSuggestedItems() {
  let inputData: DataItem[] = [];
  if (currentInputMode === "explored") {
    inputData = currentlyExploredItems;
  } else if (currentInputMode === "interesting") {
    inputData = currentlyInterestingItems;
  }

  let outputData: DataItem[] = [];
  if (currentOutputMode === "similar") {
    outputData = suggestionProvider.getSimilarSuggestions(inputData);
  } else if (currentOutputMode === "dissimilar") {
    outputData = suggestionProvider.getDissimilarSuggestions(inputData);
  }

  suggestedItems.set(outputData);
}

activeSuggestionInput.subscribe((newMode) => {
  currentInputMode = newMode;
  updateSuggestedItems();
});

activeSuggestionOutput.subscribe((newMode) => {
  currentOutputMode = newMode;
  updateSuggestedItems();
});

quadtree.subscribe((newTree) => {
  const dataspace = newTree.data();
  interactionObserver.processedDataspace = dataspace;
  suggestionProvider.processedDataspace = dataspace;
});

dimensions.subscribe((dims) => (currenDimensions = dims));
interestingDimensions.subscribe((newRecord) => {
  const intersetingDimensions = Object.keys(newRecord).filter((d) => newRecord[d]);
  const indeces = intersetingDimensions.map((d) => currenDimensions.indexOf(d));

  suggestionProvider.dimensionOfInterestIndeces = indeces;
});

exploredItems.subscribe((items) => {
  currentlyExploredItems = items;
  updateSuggestedItems();
});

interestingItems.subscribe((items) => {
  currentlyInterestingItems = items;
  updateSuggestedItems();
});

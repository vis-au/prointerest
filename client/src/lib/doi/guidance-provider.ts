import { quantile } from "d3-array";
import type DataItem from "../types/data-item";

export default class GuidanceProvider {
  private distributionsOfInterest: Map<number, [number, number]> = new Map();

  public processedDataspace: DataItem[] = [];


  private computeDistributionOfInterest(itemsOfInterest: DataItem[], dimension: number) {
    // extract quantiles from the interesting data
    const values = itemsOfInterest.map(d => d.values[dimension]);
    const min = quantile(values, 0.25) || 0;
    const max = quantile(values, 0.75) || 0;

    const distribution: [number, number] = [min, max];
    return distribution;
  }

  private computeDistributionsOfInterest(itemsOfInterest: DataItem[]) {
    this.distributionsOfInterest.clear();

    if (itemsOfInterest.length === 0) {
      return;
    }

    // compute the distributions of interest for each dimension
    itemsOfInterest[0].values.forEach((_, dimension) => {
      const distribution = this.computeDistributionOfInterest(itemsOfInterest, dimension);
      this.distributionsOfInterest.set(dimension, distribution);
    });
  }

  private isItemSimilarToInterest(item: DataItem) {
    let matchesDimensions = 0;

    item.values.forEach((value, dimension) => {
      const [ min, max ] = this.distributionsOfInterest.get(dimension) || [-Infinity, Infinity];

      const isRelevant = value >= min && value <= max;
      if (isRelevant) {
        matchesDimensions += 1;
      }
    });

    // if item matches "most" distributions, it is considered similar.
    return matchesDimensions > item.values.length * 0.85;
  }

  private getSuggestions(itemsOfInterest: DataItem[], getSimilarItems: boolean) {
    if (itemsOfInterest.length === 0) {
      return [];
    }

    this.computeDistributionsOfInterest(itemsOfInterest);

    // find all other data that lies within these quantiles
    const suggestions = this.processedDataspace
      // this filter gives us a list of all items except the ones the user is already interested in
      .filter(d => itemsOfInterest.indexOf(d) === -1)
      // we can than determine if these candidates are actually interesting under the distributions
      // computed from the interesting items
      // TODO: this leaves us with a very large search space, making this step very costly
      .filter(d => getSimilarItems === this.isItemSimilarToInterest(d));

    return suggestions;
  }

  public getItemsSimilarToInterest(itemsOfInterest: DataItem[]): DataItem[] {
    return this.getSuggestions(itemsOfInterest, true);
  }

  public getItemsDissimilarToInterest(itemsOfInterest: DataItem[]): DataItem[] {
    return this.getSuggestions(itemsOfInterest, false);
  }
}
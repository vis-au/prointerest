import type DataItem from "../types/data-item";
import { interactionModes } from "./doi-interaction";
import type { DoiInteraction, InteractionMode } from "./doi-interaction";
import { getInteractionLog, InteractionLog } from "./interaction-log";

const DEFAULT_EPSILON = 100;

export default class InteractionObserver {
  private doiPerItem = new Map<DataItem, number>();
  private affectedItemIdsPerTimestamp = new Map<number, number[]>();
  private findPointsWithinRadius: (x: number, y: number, r: number) => DataItem[];

  public data: DataItem[] = [];
  public interactionLog: InteractionLog = getInteractionLog();
  public recentSteps = 10;
  public interestThreshold = 0.23;
  public doiWeights: Map<InteractionMode, number>;

  constructor(findPointsWithinRadius: (x: number, y: number, r: number) => DataItem[]) {
    this.findPointsWithinRadius = findPointsWithinRadius;
  }

  private isItemAffectedByInteraction(item: DataItem, interaction: DoiInteraction) {
    const affected = this.affectedItemIdsPerTimestamp.get(interaction.timestamp);

    if (affected === undefined) {
      return false;
    }

    return affected.indexOf(item.id) > -1;
  }

  private getInteractionCount(type: InteractionMode) {
    let count = 0;
    this.interactionLog
      .getNRecentSteps(this.recentSteps)
      .filter((interaction) => interaction.mode === type)
      .forEach(() => count++);
    return count;
  }

  private getItemBasedInteractionFrequency(item: DataItem, type: InteractionMode) {
    let interactionFrequency = 0;

    // count all recent interactions of this type that affected that item
    this.interactionLog
      .getNRecentSteps(this.recentSteps)
      .filter((interaction) => interaction.mode === type)
      .filter((interaction) => this.isItemAffectedByInteraction(item, interaction))
      .forEach(() => interactionFrequency++);

    return interactionFrequency;
  }

  private getInteractionAge(type: InteractionMode) {
    const latestInteractionOfType = this.interactionLog.getLatestInteractionOfType(type);

    if (latestInteractionOfType === null) {
      return -1;
    }

    return this.interactionLog.getLatestTimestamp() - latestInteractionOfType.timestamp;
  }

  private applyDecay(absoluteFrequency: number, type: InteractionMode) {
    const age = this.getInteractionAge(type);

    if (age === -1) {
      return 0;
    }

    return absoluteFrequency * 0.5 ** age;
  }

  private getWeightedDoiSum(subspace: DataItem[]) {
    const interestPerItem: number[] = [];
    const values = Array.from(this.doiWeights.values());
    const weightSum = Object.values(values).reduce((a, b) => a + b, 0); // should always be 1?
    let totalDoiSum = 0;
    let weightedDoiSum = 0;

    subspace.forEach((item) => {
      totalDoiSum = 0;

      interactionModes.forEach((type) => {
        const count = this.getInteractionCount(type);
        // how frequently did user interact<type> with that item?
        const absoluteFrequency = this.getItemBasedInteractionFrequency(item, type);
        // how many of the last interact<type> interactions included this item?
        const relativeFrequency = absoluteFrequency / count;
        // how recently did user interact<type> with that item?
        const adjustedFrequency = this.applyDecay(relativeFrequency, type);
        // what's the weight of that interaction?
        const weightedDoi = adjustedFrequency * this.doiWeights.get(type);

        totalDoiSum += weightedDoi;
      });

      weightedDoiSum = totalDoiSum / weightSum;
      interestPerItem.push(weightedDoiSum);
    });

    return interestPerItem;
  }

  // TODO: implement region growing
  // private getRegionGrowingNeighbors(item: DataItem): DataItem[] {
  //   return [];
  // }

  private precomputeAffectedItemsPerInteraction() {
    this.affectedItemIdsPerTimestamp = new Map();
    this.interactionLog.getNRecentSteps(this.recentSteps).forEach((interaction) => {
      const affectedItemIds = interaction.getAffectedItems().map((d) => d.id);
      this.affectedItemIdsPerTimestamp.set(interaction.timestamp, affectedItemIds);
    });
  }

  private getEpsilonExpansion(subspaceSample: DataItem[]) {
    const expansion: Set<DataItem> = new Set();

    // find all points in the neighborhood of interesting sampled data
    subspaceSample
      .filter((item) => (this.doiPerItem.get(item) || 0) > this.interestThreshold)
      .map((item) => this.findPointsWithinRadius(item.position.x, item.position.y, DEFAULT_EPSILON))
      .flat()
      .forEach((item) => expansion.add(item));

    // const regionGrowingExtension = epsilonExtension
    //   .map((item) => this.getRegionGrowingNeighbors(item))
    //   .flat();

    return Array.from(expansion);
  }

  private update() {
    this.precomputeAffectedItemsPerInteraction();

    const interestPerItem = this.getWeightedDoiSum(this.data);
    this.data.forEach((item, i) => this.doiPerItem.set(item, interestPerItem[i]));

    const expandedSample = this.getEpsilonExpansion(this.data);
    const interestPerExtenedItem = this.getWeightedDoiSum(expandedSample);
    expandedSample.forEach((item, i) => this.doiPerItem.set(item, interestPerExtenedItem[i]));
  }

  public getExploredData(): Map<DataItem, number> {
    this.update();

    const dataOfInterest: Map<DataItem, number> = new Map();

    this.doiPerItem.forEach((value, key) => {
      if (value > this.interestThreshold) {
        dataOfInterest.set(key, value);
      }
    });

    return dataOfInterest;
  }
}

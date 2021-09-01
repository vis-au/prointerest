import type DataItem from '../types/data-item';
import type { DoiInteraction, InteractionMode } from '../interaction/doi-interaction';
import { interactionModes } from '../interaction/doi-interaction';
import { InteractionLog, getInteractionLog } from '../interaction/interaction-log';
import { interactionWeights } from '$lib/state/interaction-technique-weights';

const DEFAULT_EPSILON = 100;

export default class InterestWatchDog {
	private doiPerItem = new Map<DataItem, number>();
	private affectedItemIdsPerTimestamp = new Map<number, number[]>();
	private findPointsWithinRadius: (x: number, y: number, r: number) => DataItem[];

	public processedDataspace: DataItem[] = [];
	public interactionLog: InteractionLog = getInteractionLog();
	public recentSteps = 10;
	public interestThreshold = 0.23;
	private doiWeights: Map<InteractionMode, number>;

	constructor(findPointsWithinRadius: (x: number, y: number, r: number) => DataItem[]) {
		this.findPointsWithinRadius = findPointsWithinRadius;

		interactionWeights.subscribe((newWeights) => (this.doiWeights = newWeights));
	}

	private isItemAffectedByInteraction(item: DataItem, interaction: DoiInteraction) {
		const affected = this.affectedItemIdsPerTimestamp.get(interaction.timestamp);

		if (affected === undefined) {
			return false;
		}

		return affected.indexOf(item.id) > -1;
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

		return latestInteractionOfType.timestamp - this.interactionLog.getLatestTimestamp();
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
		const weightSum = Object.values(values).reduce((a, b) => a + b, 0);
		let totalDoiSum = 0;
		let weightedDoiSum = 0;

		subspace.forEach((item) => {
			totalDoiSum = 0;

			interactionModes.forEach((type) => {
				// how frequently did user interact with that subspace?
				const absoluteFrequency = this.getItemBasedInteractionFrequency(item, type);
				// how recently did user interact with that subspace?
				const adjustedFrequency = this.applyDecay(absoluteFrequency, type);
				// how expressively did user interact with that subspace?
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

	private getRandomSample(n: number): DataItem[] {
		// adapted from https://stackoverflow.com/a/11935263
		const shuffled = this.processedDataspace.slice(0);
		let i = this.processedDataspace.length;
		let temp;
		let index;

		while (i--) {
			index = Math.floor((i + 1) * Math.random());
			temp = shuffled[index];
			shuffled[index] = shuffled[i];
			shuffled[i] = temp;
		}

		return shuffled.slice(0, n);
	}

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

		const subspaceSample = this.getRandomSample(100);
		const interestPerItem = this.getWeightedDoiSum(subspaceSample);
		subspaceSample.forEach((item, i) => this.doiPerItem.set(item, interestPerItem[i]));

		const expandedSample = this.getEpsilonExpansion(subspaceSample);
		const interestPerExtenedItem = this.getWeightedDoiSum(expandedSample);
		expandedSample.forEach((item, i) => this.doiPerItem.set(item, interestPerExtenedItem[i]));
	}

	public getDataOfInterest(): DataItem[] {
		this.update();

		const dataOfInterest: DataItem[] = [];

		this.doiPerItem.forEach((value, key) => {
			if (value > this.interestThreshold) {
				dataOfInterest.push(key);
			}
		});

		return dataOfInterest;
	}
}

import type { DoiInteraction, InteractionMode } from './doi-interaction';

const SIZE_BEFORE_FLUSH = 1000;
const FLUSH_INTERVAL = 5000;

export class InteractionLog {
	public log: DoiInteraction[] = [];

	constructor() {
		window.setInterval(this.flush.bind(this), FLUSH_INTERVAL);
	}

	private flush() {
		if (this.log.length < SIZE_BEFORE_FLUSH) {
			return;
		}
		this.log.splice(this.log.length - SIZE_BEFORE_FLUSH, this.log.length);
	}

	public add(interaction: DoiInteraction): void {
		interaction.timestamp = this.log.length;
		this.log.push(interaction);
	}

	public getNRecentSteps(n: number): DoiInteraction[] {
		const recentSteps = n > this.log.length ? this.log.length : n;
		return this.log.slice(-recentSteps);
	}

	public getLatestTimestamp(): number {
		if (this.log.length === 0) {
			return -1;
		}

		return this.log[this.log.length - 1].timestamp;
	}

	public getLatestInteractionOfType(type: InteractionMode, maxAge = 10): DoiInteraction {
		const recentInteractions = this.getNRecentSteps(maxAge);
		const lastIndexOfType = recentInteractions
			.map((interaction) => interaction.mode)
			.lastIndexOf(type);

		if (lastIndexOfType === -1) {
			return null;
		}

		return recentInteractions[lastIndexOfType];
	}
}

const instance: InteractionLog = new InteractionLog();

export function getInteractionLog(): InteractionLog {
	return instance;
}

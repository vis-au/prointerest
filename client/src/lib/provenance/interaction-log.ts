import { sendInteraction } from "$lib/util/requests";
import { readable } from "svelte/store";
import type { DoiInteraction, InteractionMode } from "./doi-interaction";

const SIZE_BEFORE_FLUSH = 1000;
const FLUSH_INTERVAL = 5000;

export class InteractionLog {
  private _log: DoiInteraction[] = [];

  public startAutomatedFlush(): void {
    if (window !== undefined) {
      window.setInterval(this.flush.bind(this), FLUSH_INTERVAL);
    }
  }

  private flush() {
    if (this._log.length < SIZE_BEFORE_FLUSH) {
      return;
    }
    this._log.splice(this._log.length - SIZE_BEFORE_FLUSH, this._log.length);
  }

  public add(interaction: DoiInteraction): void {
    interaction.timestamp = this._log.length;
    this._log.push(interaction);
    sendInteraction(interaction);
  }

  public getNRecentSteps(n: number): DoiInteraction[] {
    const recentSteps = n > this._log.length ? this._log.length : n;
    return this._log.slice(-recentSteps);
  }

  public getLatestTimestamp(): number {
    if (!this._log) {
      this._log = [];
    }
    if (this._log.length === 0) {
      return -1;
    }

    return this._log[this._log.length - 1].timestamp;
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

  public get log(): DoiInteraction[] {
    return this._log;
  }
}

const instance: InteractionLog = new InteractionLog();

export const interactionLog = readable(instance);

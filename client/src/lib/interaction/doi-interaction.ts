import type { Quadtree } from 'd3-quadtree';
import type DataItem from '../types/data-item';

export type InteractionMode = 'brush' | 'inspect' | 'zoom' | 'select';
export const interactionModes: InteractionMode[] = ['brush', 'inspect', 'zoom', 'select'];
export const dragInteractionModes: InteractionMode[] = ['brush', 'zoom'];

export const defaultDecay = (oldValue: number) => 0.99 * oldValue;
export const defaultItemInRegion = (...params: any) => ([] as DataItem[]);

export interface DoiInteraction {
  mode: InteractionMode,
  std: number,
  x: number,
  y: number,
  quadtree: Quadtree<DataItem>,
  timestamp: number,
  getAffectedItems: () => DataItem[],
}
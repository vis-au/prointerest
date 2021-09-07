import { quadtree as d3_quadtree } from 'd3-quadtree';
import type { Quadtree } from 'd3-quadtree';
import { zoomIdentity, ZoomTransform } from 'd3-zoom';
import type DataItem from '../types/data-item';
import type { DoiInteraction, InteractionMode } from './doi-interaction';

export default class ZoomAndPan implements DoiInteraction {
	public mode: InteractionMode = 'zoom';
	public std = 0; // max distance from mean is 3*std
	public x = 0;
	public y = 0;
	public width = 0;
	public height = 0;
	public quadtree: Quadtree<DataItem> = d3_quadtree<DataItem>();
	public maxDistance = 0;
	public transform: ZoomTransform = zoomIdentity;
	public timestamp = -1;
	public getItemsInRegion: (
		x0: number,
		y0: number,
		x3: number,
		y3: number
	) => DataItem[] = () => [];

	public getAffectedItems(): DataItem[] {
		const t = this.transform;
		const viewBox = [t.invert([0, 0]), t.invert([this.width, this.height])];
		const [[x0, y0], [x3, y3]] = viewBox;

		const affectedItems = this.getItemsInRegion(x0, y0, x3, y3);

		return affectedItems;
	}
}

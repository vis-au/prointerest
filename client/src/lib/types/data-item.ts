import type { ScreenCoordinate } from "./screen-coordinate";

export default interface DataItem {
  id: number; // identifier from the underlying dataset
  position: ScreenCoordinate; // location in view space (absolute in pixels)
  iteration: number; // iteration in which item was received, i.e. the "age"
  values: number[]; // original data
}

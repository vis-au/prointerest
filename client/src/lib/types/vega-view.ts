export type VegaView = {
  insert?: (name: string, tuples: Record<string, unknown>[]) => VegaView,
  remove?: (name: string, tuples: Record<string, unknown>[]) => VegaView,
  run?: () => VegaView,
  runAsync?: () => Promise<VegaView>,
}
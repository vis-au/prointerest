import type DataItem from "$lib/types/data-item";
import type { DecisionTree, InternalNode } from "$lib/types/decision-tree";
import type { DOIDimension } from "$lib/types/doi-dimension";
import type { DimensionFilter } from "$lib/types/steering-filters";

/**
 * Transforms a list of decision tree nodes into an object defining the per-dimension filters
 * corresponding to the nodes visited in that path.
 * @param dtPath list of internal and leaf nodes from a regression/fdl tree
 * @returns the record of filters
 */
export function getFiltersForDTPath(dtPath: DecisionTree[]): DimensionFilter {
  const filters: DimensionFilter = {};

  // transform consecutive nodes into interval filters
  dtPath.forEach((node) => {
    const predecessor = dtPath.find(
      (d) => d.type === "internal" && (d.left === node || d.right === node)
    ) as InternalNode;

    if (!predecessor) {
      return;
    }

    if (predecessor.left === node) {
      const interval = filters[predecessor.feature] || [null, null];
      interval[1] = predecessor.threshold;
      filters[predecessor.feature] = interval;
    }
    if (predecessor.right === node) {
      const interval = filters[predecessor.feature] || [null, null];
      interval[0] = predecessor.threshold;
      filters[predecessor.feature] = interval;
    }
  });

  // if both sides of a subtree are included, remove the filter
  for (const dimension in filters) {
    if (filters[dimension][0] === filters[dimension][1]) {
      delete filters[dimension];
    }
  }

  return filters;
}

/**
 * Applies the provided dimension filters to an item an returns, whether or not it matches them.
 * @param item a DataItem from the dataset
 * @param filter a DimensionFilter defining min-max range for a set of dimensions from the dataset.
 * @param dimensions the indeces of the dimension names in the item.values property
 * @returns whether or not the item fits all min-max ranges across all filtered dimensions.
 */
export function doesItemFitFilter(
  item: DataItem,
  filter: DimensionFilter,
  dimensions: DOIDimension[]
): boolean {
  let matchesFilters = true;

  // apply the filters defined by the brushes in the
  Object.keys(filter).forEach((dimension) => {
    const index = dimensions.indexOf(dimension);

    if (filter[dimension][0]) {
      matchesFilters = matchesFilters && item.values[index] >= filter[dimension][0];
    }
    if (filter[dimension][1]) {
      matchesFilters = matchesFilters && item.values[index] <= filter[dimension][1];
    }
  });

  return matchesFilters;
}

export function getPathToDTNode(node: DecisionTree): DecisionTree[] {
  if (!node.parent) {
    return [node];
  } else {
    return getPathToDTNode(node.parent).concat(node);
  }
}

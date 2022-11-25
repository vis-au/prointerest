<script lang="ts">
  import { hierarchy, tree as d3tree, type HierarchyPointNode } from "d3-hierarchy";
  import { scaleLinear } from "d3-scale";
  import { linkVertical } from "d3-shape";

  import type { DecisionTree, InternalNode, LeafNode } from "$lib/types/decision-tree";
  import { truncateFloat } from "$lib/util/number-transform";

  export let decisionTree: DecisionTree;
  export let height = 500;
  export let width = 500;
  export let style = "";

  // tree rendering partially adapted to svelte
  // from https://observablehq.com/@jwilber/visualize-decision-trees-from-sklearn

  // make the actual canvas a bit smaller to avoid overflow
  const CANVAS_PADDING = 25
  $: canvasWidth = width - CANVAS_PADDING;
  $: canvasHeight = height - CANVAS_PADDING;

  const INTERNAL_NODE_SIZE = 5;
  const MAX_LEAF_NODE_HEIGHT = 40;
  const LEAF_NODE_WIDTH = 6;
  const FONT_SIZE = 12;

  const MARGIN = {
    top: MAX_LEAF_NODE_HEIGHT / 2,
    right: 10,
    bottom: MAX_LEAF_NODE_HEIGHT / 2,
    left: 10
  };

  // maps interest to the size of leaf nodes
  const scaleLeafSize = scaleLinear([0, 1], [0, MAX_LEAF_NODE_HEIGHT]);

  // path generator function
  const path = linkVertical<unknown, unknown>()
    .x(d => d["x"])
    .y(d => d["y"]);

  // tree layout generator function
  $: tree = d3tree<DecisionTree>()
    .size(
      [canvasWidth - MARGIN.left - MARGIN.right, canvasHeight - MARGIN.top - MARGIN.bottom]
    );

  // turn decision tree in to d3 hierarchy format
  $: root = hierarchy(decisionTree, d => d.type === "internal" ? [d.left, d.right] : null);

  // compute the tree layout
  $: treeData = tree(root);

  // derive partitions of internal and leaf nodes
  $: internalNodes = treeData.descendants()
    .filter(d => d.data.type === "internal") as HierarchyPointNode<InternalNode>[];

  $: leafNodes = treeData.descendants()
    .filter(d => d.data.type === "leaf") as HierarchyPointNode<LeafNode>[];

</script>

<div class="decision-tree-viewer" {style}>
  {#if !decisionTree}
    <span>no dt, yet</span>
  {:else}
    <svg class="canvas"
      viewBox="0 0 {width} {height}"
      width={canvasWidth}
      height={canvasHeight}>

      <g class="decision-tree-container" transform="translate({MARGIN.left}, {MARGIN.top})">
        <g class="links">
          { #each treeData.links() as link }
            <path class="link" d={path(link)} />
          {/each}
        </g>

        <g class="nodes">
          <g class="internal-nodes">
            {#each internalNodes as node}
              <g class="internal-node" transform="translate({node.x},{node.y})">
                <circle class="node" r={INTERNAL_NODE_SIZE} />
                <text class="label"
                  font-size={FONT_SIZE}
                  alignment-baseline="middle"
                  dx={10}
                  dy={-INTERNAL_NODE_SIZE - 5}>

                  {`${node.data.feature} <= ${truncateFloat(node.data.threshold)}`}
                </text>
              </g>
            {/each}
          </g>

          <g class="leaf-nodes">
            {#each leafNodes as node}
              <g class="leaf-node" transform="translate({node.x - LEAF_NODE_WIDTH/2},{node.y})">
                <rect class="background"
                  width={LEAF_NODE_WIDTH}
                  height={scaleLeafSize.range()[1]} />
                <rect class="value"
                  width={LEAF_NODE_WIDTH}
                  height={node.data.type === "leaf" ? scaleLeafSize(node.data.value[0]) : 0} />
              </g>
            {/each}
          </g>
        </g>
      </g>
    </svg>
  {/if}
</div>

<style>
  .decision-tree-viewer .links path.link {
    fill: none;
    stroke: #aaa;
    stroke-width: 1;
  }
  .decision-tree-viewer .nodes .internal-nodes circle.node {
    fill: white;
    stroke: #555;
    stroke-width: 1;
  }
  .decision-tree-viewer text {
    font-family: Lato;
  }
  .decision-tree-viewer .nodes .internal-nodes text.label {
    text-anchor: middle;
  }
  .decision-tree-viewer .nodes .leaf-nodes rect.background {
    fill: white;
    stroke: #aaa;
    stroke-width: 1;
  }
  .decision-tree-viewer .ndoes .leaf-nodes rect.value {
    fill: black;
  }
</style>
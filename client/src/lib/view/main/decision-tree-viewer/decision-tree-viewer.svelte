<script lang="ts">
  import { hierarchy, tree as d3tree, type HierarchyPointNode } from "d3-hierarchy";
  import { scaleLinear } from "d3-scale";
  import { select, type Selection } from "d3-selection";
  import { linkVertical } from "d3-shape";
  import { afterUpdate } from "svelte";

  import type { DecisionTree, InternalNode, LeafNode } from "$lib/types/decision-tree";
  import { truncateFloat } from "$lib/util/number-transform";

  export let decisionTree: DecisionTree;
  export let height = 400;
  export let width = 800;
  export let style = "";

  // avoid overflow
  $: canvasWidth = width - 30;
  $: canvasHeight = height - 25;

  const INTERNAL_NODE_SIZE = 5;
  const MAX_LEAF_NODE_HEIGHT = 50;
  const LEAF_NODE_WIDTH = 10;
  const scaleLeafSize = scaleLinear([0, 1], [0, MAX_LEAF_NODE_HEIGHT]);
  const FONT_SIZE = 12;

  const MARGIN = ({
    top: MAX_LEAF_NODE_HEIGHT,
    right: 10,
    bottom: MAX_LEAF_NODE_HEIGHT,
    left: 10
  });

  // path generator function
  const path = linkVertical<unknown, unknown>()
    .x(d => d["x"])
    .y(d => d["y"]);

  // tree layout generator function
  $: tree = d3tree<DecisionTree>()
    // .nodeSize([INTERNAL_NODE_SIZE, INTERNAL_NODE_SIZE])
    .size(
      [canvasWidth - MARGIN.left - MARGIN.right, canvasHeight - MARGIN.top - MARGIN.bottom]
    );

  // turn decision tree in to d3 hierarchy format
  $: root = hierarchy(decisionTree, d => d.type === "internal" ? [d.left, d.right] : null);

  // compute the tree layout
  $: treeData = tree(root);
  $: internalNodes = treeData.descendants()
    .filter(d => d.data.type === "internal") as HierarchyPointNode<InternalNode>[];
  $: leafNodes = treeData.descendants()
    .filter(d => d.data.type === "leaf") as HierarchyPointNode<LeafNode>[];

</script>

<div class="decision-tree-viewer" {style}>
  {#if !decisionTree}
    <span>no dt, yet</span>
  {:else}
    <div class="nodes" style="max-height:{height}px;max-width:{width}px">
      <!-- <InternalNode node={tree} /> -->
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
    </div>
  {/if}
</div>

<style>
  .decision-tree-viewer .links path.link {
    fill: none;
    stroke: #555;
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
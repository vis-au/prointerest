<script lang="ts">
  import { hierarchy, tree as d3tree, type HierarchyPointLink, type HierarchyPointNode } from "d3-hierarchy";
  import { scaleLinear } from "d3-scale";
  import { linkVertical } from "d3-shape";

  import type { DecisionTree, InternalNode, LeafNode } from "$lib/types/decision-tree";
  import { truncateFloat } from "$lib/util/number-transform";
  import { doiLimit } from "$lib/state/doi-limit";

  export let id: string;
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
  const MAX_PATH_WIDTH = 2;
  const FONT_SIZE = 12;

  const MARGIN = {
    top: MAX_LEAF_NODE_HEIGHT / 2,
    right: 10,
    bottom: MAX_LEAF_NODE_HEIGHT / 2 + FONT_SIZE,
    left: 10
  };

  // path generator function
  const path = linkVertical<HierarchyPointLink<DecisionTree>, HierarchyPointLink<DecisionTree>>()
    .x(d => d["x"])
    .y(d => d["y"]);

  // tree layout generator function
  $: tree = d3tree<DecisionTree>()
    .size(
      [canvasWidth - MARGIN.left - MARGIN.right, canvasHeight - MARGIN.top - MARGIN.bottom]
    );

  // turn decision tree in to d3 hierarchy format
  $: root = hierarchy(decisionTree, d => d?.type === "internal" ? [d.left, d.right] : null);
  $: root.sum(node => {
    return node.type === "leaf" ? node.value[0] : 0;
  });

  // maps interest to the size of leaf nodes
  const scaleLeafSize = scaleLinear([0, 1], [0, MAX_LEAF_NODE_HEIGHT]);

  // maps interest to the width of links
  const scaleLinkSize = scaleLinear([0, root?.value || 1], [1, MAX_PATH_WIDTH]);

  // compute the tree layout
  $: treeData = root ? tree(root) : null;


  $: links = treeData?.links();

  // derive partitions of internal and leaf nodes
  $: internalNodes = treeData?.descendants()
    .filter(d => d.data?.type === "internal") as HierarchyPointNode<InternalNode>[];

  $: leafNodes = treeData?.descendants()
    .filter(d => d.data?.type === "leaf") as HierarchyPointNode<LeafNode>[];


  $: isNodeInteresting = (node: DecisionTree) => {
    return node.type === "internal"
      ? isNodeInteresting(node.left) || isNodeInteresting(node.right)
      : node.value[0] > $doiLimit;
  };


  let hoveredNode: HierarchyPointNode<DecisionTree> = null;
  let hoveredPath: DecisionTree[] = [];

  $: {
    let focusNode = hoveredNode;

    // focus all descendents
    hoveredPath = focusNode?.descendants().map(d => d.data) || [];

    // focus all predecessorss
    hoveredPath = hoveredPath.concat(focusNode?.ancestors().map(d => d.data) || []);
  }
  function hoverNode(node: HierarchyPointNode<DecisionTree>) {
    hoveredNode = node
  }

  function unhoverNode() {
    hoveredNode = null;
  }

  $: isNodeFocused = (node: HierarchyPointNode<DecisionTree>) => {
    return hoveredPath.indexOf(node.data) > -1;
  }

  $: isLinkFocused = (link: HierarchyPointLink<DecisionTree>) => {
    return hoveredPath.indexOf(link["source"].data) > -1
           && hoveredPath.indexOf(link["target"].data) > -1;

  }
</script>

<div class="decision-tree-viewer" {style}>
  {#if !decisionTree}
    <div style="width:{canvasWidth}px">no dt, yet</div>
  {:else}
    <svg id="{id}-canvas"
      class="canvas"
      viewBox="0 0 {width} {height}"
      width={canvasWidth}
      height={canvasHeight}>

      <g class="decision-tree-container" transform="translate({MARGIN.left}, {MARGIN.top})">
        <g class="links">
          { #each links as link }
            <path
              class="link
                {isNodeInteresting(link["target"]["data"]) ? "interesting" : ""}
                {isLinkFocused(link) ? "focus" : ""}
              "
              stroke-width={scaleLinkSize(link["target"].value)}
              d={path(link)}
            />
          {/each}
        </g>

        <g class="nodes">
          <g class="internal-nodes">
            {#each internalNodes as node}
              <g
                class="internal-node
                  {isNodeInteresting(node.data) ? "interesting" : ""}
                  {isNodeFocused(node) ? "focus" : ""}
                "
                transform="translate({node.x},{node.y})">
                <circle
                  class="node {hoveredNode === node ? "hover" : ""}"
                  r={INTERNAL_NODE_SIZE}
                  on:click={() => hoverNode(node)}
                  on:mouseover={() => hoverNode(node)}
                  on:focus={() => hoverNode(node)}
                  on:mouseout={() => unhoverNode()}
                  on:blur={() => unhoverNode()}
                />

                {#if isNodeInteresting(node.data)}
                  <text class="label"
                    font-size={FONT_SIZE}
                    alignment-baseline="middle"
                    dx={10}
                    dy={-INTERNAL_NODE_SIZE - 5}>

                    {`${node.data.feature} <= ${truncateFloat(node.data.threshold)}`}
                </text>
                {/if}
              </g>
            {/each}
          </g>

          <g class="leaf-nodes">
            {#each leafNodes as node}
              <g class="leaf-node
                  {isNodeInteresting(node.data) ? "interesting" : ""}
                  {isNodeFocused(node) ? "focus" : ""}
                "
                transform="translate({node.x - LEAF_NODE_WIDTH/2},{node.y})"
                on:click={() => hoverNode(node)}
                on:mouseover={() => hoverNode(node)}
                on:focus={() => hoverNode(node)}
                on:mouseout={() => unhoverNode()}
                on:blur={() => unhoverNode()}>

                <rect class="background"
                  width={LEAF_NODE_WIDTH}
                  height={scaleLeafSize.range()[1]} />
                <rect class="value"
                  width={LEAF_NODE_WIDTH}
                  height={scaleLeafSize(node.data.value[0])} />

                <text
                  class="value"
                  dx={LEAF_NODE_WIDTH/2}
                  dy={scaleLeafSize.range()[1] + FONT_SIZE}>
                  {truncateFloat(node.data.value[0])}
                </text>
              </g>
            {/each}
          </g>
        </g>
      </g>
    </svg>
  {/if}
</div>

<style>
  .decision-tree-viewer svg {
    text-rendering: optimizeSpeed;
    shape-rendering: geometricPrecision;
  }
  .decision-tree-viewer text {
    font-family: Lato;
  }

  .decision-tree-viewer .links path.link {
    fill: none;
    stroke: #aaa;
  }
  .decision-tree-viewer .links path.link.interesting {
    stroke: black;
  }
  .decision-tree-viewer .links path.link.focus {
    stroke: orange;
  }

  .decision-tree-viewer .nodes .internal-node circle.node {
    fill: white;
    stroke: #aaa;
    stroke-width: 1;
  }
  .decision-tree-viewer .nodes .internal-node.interesting circle.node {
    stroke: black;
    fill: black;
    cursor: pointer;
  }
  .decision-tree-viewer .nodes .internal-node.focus circle.node {
    fill: orange;
    stroke: none;
  }
  .decision-tree-viewer .nodes .internal-node text.label {
    text-anchor: middle;
  }

  .decision-tree-viewer .nodes .leaf-node {
    cursor: pointer;
  }
  .decision-tree-viewer .nodes .leaf-node rect.background {
    fill: white;
    stroke: #aaa;
    stroke-width: 1;
  }
  .decision-tree-viewer .nodes .leaf-node.focus rect.background {
    stroke: orange;
  }
  .decision-tree-viewer .nodes .leaf-node rect.value {
    fill: #aaa;
  }
  .decision-tree-viewer .nodes .leaf-node.interesting rect.value {
    fill: black;
  }
  .decision-tree-viewer .nodes .leaf-node.focus rect.value {
    fill: orange;
    stroke: none;
  }
  .decision-tree-viewer .nodes .leaf-node text.value {
    display: none;
    text-anchor: middle;
  }
  .decision-tree-viewer .nodes .leaf-node.focus text.value,
  .decision-tree-viewer .nodes .leaf-node:hover text.value {
    display: block;
  }
</style>
<script lang="ts">
  import { hierarchy, tree as d3tree, type HierarchyPointNode } from "d3-hierarchy";
  import { scaleLinear } from "d3-scale";
  import { select } from "d3-selection";
  import { linkVertical } from "d3-shape";
  import { afterUpdate } from "svelte";

  import type { DecisionTree } from "$lib/types/decision-tree";
  import { truncateFloat } from "$lib/util/number-transform";

  export let decisionTree: DecisionTree;
  export let height = 400;
  export let width = 800;
  export let style = "";

  // avoid overflow
  $: canvasWidth = width - 30;
  $: canvasHeight = height - 25;

  afterUpdate(render);

  let canvasElement: SVGElement = null;

  function render() {
    if (canvasElement === null) {
      return;
    }

    // define svg
    const svg = select(canvasElement);

    const INTERNAL_NODE_SIZE = 5;
    const MAX_LEAF_NODE_HEIGHT = 50;
    const LEAF_NODE_WIDTH = 10;
    const scaleLeafSize = scaleLinear([0, 1], [0, MAX_LEAF_NODE_HEIGHT]);
    const FONT_SIZE = 12;

    const margin = ({
      top: MAX_LEAF_NODE_HEIGHT,
      right: 10,
      bottom: MAX_LEAF_NODE_HEIGHT,
      left: 10
    });

    // turn decision tree in to d3 hierarchy format
    const root = hierarchy(decisionTree, d => d.type === "internal" ? [d.left, d.right] : null);

    // tree layout generator function
    const tree = d3tree<DecisionTree>()
      .nodeSize([INTERNAL_NODE_SIZE, INTERNAL_NODE_SIZE])
      .size(
        [canvasWidth - margin.left - margin.right, canvasHeight - margin.top - margin.bottom]
      );

    // compute the tree layout
    const treeData = tree(root);

    // path generator function
    const path = linkVertical<unknown, unknown>()
      .x(d => d["x"])
      .y(d => d["y"]);

    svg.selectAll("*").remove();

    // append g for framing
    const g = svg
      .append("g")
      .attr("class", "decision-tree")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // draw links
    g.append("g")
      .attr("class", "tree-link-g")
      .attr("class", "links")
      .selectAll("path").data(treeData.links())
        .join("path")
          .attr("d", path)
          .attr("class", "link")
          .attr("fill", "none")
          .attr("stroke", "#555")
          .attr("stroke-width", 1);

    // draw nodes
    const internalNodes = g.append("g")
      .attr("class", "internal-nodes")
      .selectAll("circle")
        .data(treeData.descendants().filter(d => d.data.type === "internal"));

     internalNodes.join("circle")
      .attr("class", "internal-node")
      .attr("fill", "white")
      .attr("r", INTERNAL_NODE_SIZE)
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("stroke", "#555")
      .attr("stroke-width", 1);

    const nodeTextAccessor = (d: HierarchyPointNode<DecisionTree>) => d.data.type === "internal"
      ? `${d.data.feature} <= ${truncateFloat(d.data.threshold)}`
      : truncateFloat(d.data.value[0]);

    internalNodes.join("text")
      .attr("text-anchor", d => d.data.type === "internal" ? "start" : "middle")
      .attr("text-anchor", "middle")
      .attr("dx", d => d.data.type === "internal" ? 10 : 0)
      .attr("dy", d => d.data.type === "leaf" ? scaleLeafSize.range()[1]/2 : -INTERNAL_NODE_SIZE - 5)
      .attr("alignment-baseline", "middle")
      .attr("transform", d => `translate(${d.x},${d.y})`)
      .attr("font-size", FONT_SIZE)
      .style("font-family", "Arial")
      .text(nodeTextAccessor);

    const leafNodes = g.append("g")
      .attr("class", "leaf-nodes")
      .selectAll("g.leaf-node")
        .data(treeData.descendants().filter(d => d.data.type === "leaf"));

    const leafNodeContainer = leafNodes.join("g")
      .attr("class", "leaf-node")
      .attr("transform", d => `translate(${d.x - LEAF_NODE_WIDTH/2}, ${d.y})`);

    // background rect showing the bounding box of the leaf nodes
    leafNodeContainer.append("rect")
      .attr("class", "leaf-node")
      .attr("fill", "white")
      .attr("width", LEAF_NODE_WIDTH)
      .attr("height", scaleLeafSize.range()[1])
      .attr("stroke", "#aaa")
      .attr("stroke-width", 1);

    // the actual leaf node containing the interest value predicted for this path
    leafNodeContainer.append("rect")
      .attr("class", "leaf-node")
      .attr("fill", "#000")
      .attr("width", LEAF_NODE_WIDTH)
      .attr("height", d => d.data.type === "leaf" ? scaleLeafSize(d.data.value[0]) : null);
  }
</script>

<div class="decision-tree-viewer" {style}>
  {#if !decisionTree}
    <span>no dt, yet</span>
  {:else}
    <div class="nodes" style="max-height:{height}px;max-width:{width}px">
      <!-- <InternalNode node={tree} /> -->
      <svg
        class="canvas"
        bind:this={canvasElement}
        viewBox="0 0 {width} {height}"
        width={canvasWidth}
        height={canvasHeight}
      />
    </div>
  {/if}
</div>

<style>
  .decision-tree-viewer .nodes {
    border: 1px solid #e8eaed;
    padding: 0;
    margin: 0;
    margin-top: 0.5rem;
    line-height: 150%;
    overflow: auto;
  }
</style>
<script lang="typescript">
  import { dimensions, totalSize } from "$lib/state/processed-data";
  import Header from "$lib/view/header/header.svelte";
  import MainView from "$lib/view/main/main-view.svelte";
  import { onMount } from "svelte";
  import { hexbinning } from "$lib/state/hexbinning";
  import { currentTransform } from "$lib/state/zoom";
  import ActiveDoiPanel from "$lib/view/header/doi/active-doi-panel.svelte";
  import { quadtree } from "$lib/state/quadtree";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { isResizing } from "$lib/state/is-resizing";
  import ResizingOverlay from "$lib/view/main/resizing-overlay.svelte";
  import { getDimensionNames, getTotalDatasize } from "$lib/util/requests";
  import { activeViewEncodings } from "$lib/state/active-view-encodings";
  import { viewPort } from "$lib/state/visible-data";
	import SplitView from "$lib/view/main/split-view.svelte";
	import SecondaryView from "$lib/view/main/secondary-view.svelte";
	import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";

  let innerWidth = 0;
  let innerHeight = 0;
  let mousePosition = [-1, -1];

  const headerHeight = 35;
  const margin = {
    horizontal: 2,
    vertical: headerHeight + 2
  };

  $: plotWidth = innerWidth - margin.horizontal;
  $: plotHeight = innerHeight - margin.vertical;
	$: topHeight = $isSecondaryViewCollapsed ? plotHeight : plotHeight * 0.73;
	$: bottomHeight = plotHeight - topHeight;
  $: $viewPort.maxX = innerWidth;
  $: $viewPort.maxY = topHeight;

  $: $scaleX?.range([0, plotWidth]);
  $: $scaleY?.range([0, topHeight]);

  onMount(() => {
    setTimeout(async () => {
      // triggers the rendering of the binned scatterplot
      $hexbinning = $hexbinning;
      // triggers the rendering of the scatterplot
      $currentTransform = $currentTransform;

      $quadtree = $quadtree.extent([
        [0, 0],
        [innerWidth, innerHeight]
      ]);

      $dimensions = await getDimensionNames();
      $activeViewEncodings.x = "trip_distance";
      $activeViewEncodings.y = "total_amount";

      $totalSize = await getTotalDatasize();
    }, 0);
  });
</script>

<div id="pro-interest">
  <Header height={headerHeight} />

	<SplitView bind:isCollapsed={$isSecondaryViewCollapsed}>
		<div slot="top">
			<MainView width={plotWidth} height={topHeight} />
		</div>
		<div slot="bottom" style="">
			<SecondaryView width={plotWidth} height={bottomHeight} />
		</div>
	</SplitView>

  <ActiveDoiPanel />
  <ResizingOverlay x={mousePosition[0]} y={$isResizing?.startY} />
</div>

<svelte:window bind:innerWidth bind:innerHeight />

<svelte:body on:mousemove={(e) => (mousePosition = [e.clientX, e.clientY])} />

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
  :global(body *) {
    font-family: Roboto;
    box-sizing: border-box;
  }
</style>

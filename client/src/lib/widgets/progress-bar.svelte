<script lang="ts">
  import { separateThousands } from "$lib/util/number-transform";

  export let id: string;
  export let progress: number;
  export let current: number;
  export let total: number;
  export let width: number = null;
  export let height: number;
</script>

<div
  id="{id}-progress-bar"
  class="progress-bar"
  style:width="{width}px"
  style:minHeight="{height}px"
  title="{separateThousands(current)}/{separateThousands(total)}"
>
  <div class="progress" style:width="{progress * 100}%" style:height="{height}px" />
</div>

<style>
  .progress-bar {
    border: 1px solid black;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    margin-top: 1px;
    background: #fff;
  }
  .progress-bar .progress {
    background: black;
  }
</style>

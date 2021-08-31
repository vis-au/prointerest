<script lang="typescript">

import Row from "$lib/widgets/row.svelte";
import PosteriorWeights from "./posterior-weights.svelte";
import PriorWeights from "./prior-weights.svelte";

</script>

<header>
  <div class="title">
    <img src="static/logo.svg" alt="the ProInterest logo" />
  </div>
  <Row id="doi-configuration">
    <PriorWeights />
    <PosteriorWeights />
  </Row>
</header>

<style>
  header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background: white;
    border-bottom: 1px solid #ddd;
  }

  header div.title {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  header div.title>img {
    height: 28px;
  }

</style>
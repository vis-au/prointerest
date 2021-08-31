<script lang="typescript">

export let title: string;

</script>

<div class="doi-config">
  <h2>{ title }</h2>
  <slot></slot>
</div>

<style>
  div.doi-config {
    background: white;
    min-width: 300px;
    min-height: 150px;
    padding: 1rem 1.5rem 1.5rem;
  }
  div.doi-config h2 {
    margin: 10px 0;
  }
</style>

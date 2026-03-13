<script lang="ts">
	let { children } = $props();
</script>

<div class="network-layout">
	{@render children()}
</div>

<style>
	.network-layout {
		height: 100%;
		min-height: 0;
	}
</style>

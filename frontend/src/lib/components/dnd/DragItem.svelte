<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		children,
		id,
		className = ''
	}: {
		children?: Snippet;
		id: number;
		className?: string;
	} = $props();
</script>

<div class={className} data-drag-id={id}>
	{@render children?.()}
</div>

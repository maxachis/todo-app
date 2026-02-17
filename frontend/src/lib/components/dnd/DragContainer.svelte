<script lang="ts">
import { dndzone, dragHandleZone } from 'svelte-dnd-action';
	import type { Snippet } from 'svelte';

	let {
		children,
		items = [],
		type = 'default',
		flipDurationMs = 150,
		centreDraggedOnCursor = false,
		useDragHandleZone = false,
		dropFromOthersDisabled = false,
		dragDisabled = false,
		onConsider = (_event: CustomEvent<any>) => {},
		onFinalize = (_event: CustomEvent<any>) => {},
		className = ''
	}: {
		children?: Snippet;
		items?: any[];
		type?: string;
		flipDurationMs?: number;
		centreDraggedOnCursor?: boolean;
		useDragHandleZone?: boolean;
		dropFromOthersDisabled?: boolean;
		dragDisabled?: boolean;
		onConsider?: (event: CustomEvent<any>) => void;
		onFinalize?: (event: CustomEvent<any>) => void;
		className?: string;
	} = $props();
</script>

{#if useDragHandleZone}
	<div
		class={className}
		use:dragHandleZone={{ items, type, flipDurationMs, centreDraggedOnCursor, dropFromOthersDisabled, dragDisabled }}
		onconsider={onConsider}
		onfinalize={onFinalize}
	>
		{@render children?.()}
	</div>
{:else}
	<div
		class={className}
		use:dndzone={{ items, type, flipDurationMs, centreDraggedOnCursor, dropFromOthersDisabled, dragDisabled }}
		onconsider={onConsider}
		onfinalize={onFinalize}
	>
		{@render children?.()}
	</div>
{/if}

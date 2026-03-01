<script lang="ts">
import { dndzone, dragHandleZone } from 'svelte-dnd-action';
	import type { Snippet } from 'svelte';

	const dropTargetStyle = { outline: 'rgba(180, 88, 40, 0.7) solid 2px' };

	let {
		children,
		items = [],
		type = 'default',
		flipDurationMs = 150,
		centreDraggedOnCursor = false,
		useDragHandleZone = false,
		dropFromOthersDisabled = false,
		dragDisabled = false,
		delayTouchStart = 200 as boolean | number,
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
		delayTouchStart?: boolean | number;
		onConsider?: (event: CustomEvent<any>) => void;
		onFinalize?: (event: CustomEvent<any>) => void;
		className?: string;
	} = $props();
</script>

{#if useDragHandleZone}
	<div
		class={className}
		use:dragHandleZone={{ items, type, flipDurationMs, centreDraggedOnCursor, dropFromOthersDisabled, dragDisabled, delayTouchStart, dropTargetStyle }}
		onconsider={onConsider}
		onfinalize={onFinalize}
	>
		{@render children?.()}
	</div>
{:else}
	<div
		class={className}
		use:dndzone={{ items, type, flipDurationMs, centreDraggedOnCursor, dropFromOthersDisabled, dragDisabled, delayTouchStart, dropTargetStyle }}
		onconsider={onConsider}
		onfinalize={onFinalize}
	>
		{@render children?.()}
	</div>
{/if}

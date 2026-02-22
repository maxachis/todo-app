<script lang="ts">
	interface Props {
		onDragStart?: () => void;
		onDrag?: (deltaX: number) => void;
		onDragEnd?: () => void;
	}

	let { onDragStart, onDrag, onDragEnd }: Props = $props();

	let dragging = $state(false);
	let startX = 0;

	function handlePointerDown(e: PointerEvent) {
		e.stopPropagation();
		e.preventDefault();
		dragging = true;
		startX = e.clientX;
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
		onDragStart?.();
	}

	function handlePointerMove(e: PointerEvent) {
		if (!dragging) return;
		const deltaX = e.clientX - startX;
		startX = e.clientX;
		onDrag?.(deltaX);
	}

	function handlePointerUp(_e: PointerEvent) {
		if (!dragging) return;
		dragging = false;
		onDragEnd?.();
	}
</script>

<div
	class="resize-handle"
	class:active={dragging}
	role="separator"
	aria-orientation="vertical"
	onpointerdown={handlePointerDown}
	onpointermove={handlePointerMove}
	onpointerup={handlePointerUp}
>
	<div class="resize-line"></div>
</div>

<style>
	.resize-handle {
		width: 6px;
		cursor: col-resize;
		display: flex;
		align-items: stretch;
		justify-content: center;
		user-select: none;
		touch-action: none;
		flex-shrink: 0;
	}

	.resize-line {
		width: 2px;
		background: var(--border);
		border-radius: 1px;
		transition: background var(--transition);
	}

	.resize-handle:hover .resize-line,
	.resize-handle.active .resize-line {
		background: var(--accent);
	}
</style>

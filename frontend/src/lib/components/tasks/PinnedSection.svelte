<script lang="ts">
	import { dndzone } from 'svelte-dnd-action';
	import type { Task } from '$lib';
	import { completeTask, selectTask } from '$lib/stores/tasks';

	interface PinnedEntry { task: Task; parentTitle: string }

	let {
		entries,
		onReorder = (_taskIds: number[]) => {}
	}: {
		entries: PinnedEntry[];
		onReorder?: (taskIds: number[]) => void;
	} = $props();

	let sortablePinned = $state<(PinnedEntry & { id: number })[]>([]);

	$effect(() => {
		sortablePinned = entries.map((e) => ({ ...e, id: e.task.id }));
	});

	function jumpToTask(taskId: number): void {
		const el = document.querySelector(`[data-task-id="${taskId}"]`);
		if (el) {
			el.scrollIntoView({ behavior: 'smooth', block: 'center' });
			el.classList.add('flash');
			setTimeout(() => el.classList.remove('flash'), 800);
		}
		selectTask(taskId);
	}

	function handleConsider(event: CustomEvent<{ items: (PinnedEntry & { id: number })[] }>): void {
		sortablePinned = event.detail.items;
	}

	function handleFinalize(event: CustomEvent<{ items: (PinnedEntry & { id: number })[] }>): void {
		sortablePinned = event.detail.items;
		onReorder(sortablePinned.map((e) => e.id));
	}
</script>

{#if sortablePinned.length > 0}
	<div class="pinned-section">
		<h3 class="pinned-header">&#128204; Pinned</h3>
		<div
			class="pinned-dnd-zone"
			use:dndzone={{ items: sortablePinned, type: 'pinned-dnd', flipDurationMs: 150, centreDraggedOnCursor: false, delayTouchStart: 200, dropTargetStyle: { outline: 'rgba(180, 88, 40, 0.7) solid 2px' } }}
			onconsider={handleConsider}
			onfinalize={handleFinalize}
		>
			{#each sortablePinned as entry (entry.id)}
				<button class="pinned-task" onclick={() => jumpToTask(entry.task.id)}>
					<!-- svelte-ignore a11y_click_events_have_key_events -->
					<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
					<label class="checkbox-wrap" onclick={(e) => e.stopPropagation()}>
						<input
							type="checkbox"
							checked={false}
							onchange={() => completeTask(entry.task.id)}
							class="checkbox-native"
						/>
						<span class="checkbox-custom">
							<svg viewBox="0 0 14 14" fill="none" class="check-icon">
								<path d="M3.5 7.2L6 9.7L10.5 4.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
							</svg>
						</span>
					</label>
					<span class="pinned-title">
						{#if entry.parentTitle}<span class="parent-prefix">{entry.parentTitle} &rsaquo;</span> {/if}{entry.task.title}
					</span>
					{#if entry.task.tags.length > 0}
						<span class="pinned-tags">
							{#each entry.task.tags.slice(0, 2) as tag}
								<span class="tag">{tag.name}</span>
							{/each}
						</span>
					{/if}
				</button>
			{/each}
		</div>
	</div>
{/if}

<style>
	.pinned-section {
		background: var(--pinned-bg);
		border: 1px solid var(--pinned-border);
		border-radius: var(--radius-md);
		padding: 0.55rem 0.7rem;
		margin-bottom: 0.75rem;
	}

	.pinned-header {
		margin: 0 0 0.35rem;
		font-family: var(--font-display);
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--pinned-text);
	}

	.pinned-dnd-zone {
		display: grid;
	}

	.pinned-task {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		width: 100%;
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0.3rem 0.4rem;
		border-radius: var(--radius-sm);
		text-align: left;
		font-family: var(--font-body);
		transition: background var(--transition);
	}

	.pinned-task:hover {
		background: var(--pinned-tag-bg);
	}

	.checkbox-wrap {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		-webkit-tap-highlight-color: transparent;
	}

	.checkbox-native {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
		clip-path: inset(50%);
		white-space: nowrap;
	}

	.checkbox-custom {
		position: relative;
		width: 1.15rem;
		height: 1.15rem;
		border-radius: 50%;
		border: 1.5px solid var(--border);
		background: transparent;
		transition:
			border-color 0.2s ease,
			background-color 0.2s ease,
			transform 0.15s ease,
			box-shadow 0.2s ease;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.checkbox-custom:hover {
		border-color: var(--accent);
		box-shadow: 0 0 0 3px var(--accent-light);
	}

	.checkbox-native:focus-visible + .checkbox-custom {
		border-color: var(--accent);
		box-shadow: 0 0 0 3px var(--accent-medium);
	}

	.check-icon {
		width: 0.7rem;
		height: 0.7rem;
		color: transparent;
		transition: color 0.15s ease 0.05s;
	}

	.pinned-title {
		font-size: 0.85rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		flex: 1;
		color: var(--text-primary);
	}

	.parent-prefix {
		color: var(--text-tertiary);
		font-size: 0.8rem;
	}

	.pinned-tags {
		display: flex;
		gap: 0.2rem;
	}

	.tag {
		background: var(--pinned-tag-bg);
		padding: 0.08rem 0.35rem;
		border-radius: var(--radius-sm);
		font-size: 0.65rem;
		font-weight: 500;
		color: var(--pinned-text);
	}

	:global(.flash) {
		animation: flash-highlight 0.8s ease;
	}

	@keyframes flash-highlight {
		0% { background: var(--pinned-border); }
		100% { background: transparent; }
	}
</style>

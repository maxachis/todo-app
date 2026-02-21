<script lang="ts">
	import { dndzone } from 'svelte-dnd-action';
	import type { Task } from '$lib';
	import { selectTask } from '$lib/stores/tasks';

	let {
		tasks,
		onReorder = (_taskIds: number[]) => {}
	}: {
		tasks: Task[];
		onReorder?: (taskIds: number[]) => void;
	} = $props();

	let sortablePinned = $state<Task[]>([]);

	$effect(() => {
		sortablePinned = [...tasks];
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

	function handleConsider(event: CustomEvent<{ items: Task[] }>): void {
		sortablePinned = event.detail.items as Task[];
	}

	function handleFinalize(event: CustomEvent<{ items: Task[] }>): void {
		sortablePinned = event.detail.items as Task[];
		onReorder(sortablePinned.map((task) => task.id));
	}
</script>

{#if sortablePinned.length > 0}
	<div class="pinned-section">
		<h3 class="pinned-header">&#128204; Pinned</h3>
		<div
			class="pinned-dnd-zone"
			use:dndzone={{ items: sortablePinned, type: 'pinned-dnd', flipDurationMs: 150, centreDraggedOnCursor: false }}
			onconsider={handleConsider}
			onfinalize={handleFinalize}
		>
			{#each sortablePinned as task (task.id)}
				<button class="pinned-task" onclick={() => jumpToTask(task.id)}>
					<span class="pinned-title">{task.title}</span>
					{#if task.tags.length > 0}
						<span class="pinned-tags">
							{#each task.tags.slice(0, 2) as tag}
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

	.pinned-title {
		font-size: 0.85rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		flex: 1;
		color: var(--text-primary);
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

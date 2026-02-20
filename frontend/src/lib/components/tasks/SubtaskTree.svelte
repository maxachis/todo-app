<script lang="ts">
	import type { Task } from '$lib';
	import { moveTaskWithOptions, refreshTasksView, taskDragLockedStore, setTaskDragLocked } from '$lib/stores/tasks';
	import { addToast } from '$lib/stores/toast';
	import DragContainer from '../dnd/DragContainer.svelte';
	import DragItem from '../dnd/DragItem.svelte';
	import TaskRow from './TaskRow.svelte';
	import SubtaskTree from './SubtaskTree.svelte';

	let {
		subtasks,
		sectionId,
		parentId,
		depth = 1
	}: {
		subtasks: Task[];
		sectionId: number;
		parentId: number;
		depth?: number;
	} = $props();

	let collapsed = $state(false);

	const completedSubtasks = $derived(
		subtasks.filter((t) => t.is_completed).sort((a, b) => a.position - b.position)
	);
	let sortableSubtasks = $state<Task[]>([]);

	let showDone = $state(false);

	$effect(() => {
		sortableSubtasks = subtasks
			.filter((t) => !t.is_completed)
			.sort((a, b) => a.position - b.position);
	});

	function handleConsider(event: CustomEvent<{ items: Task[] }>): void {
		sortableSubtasks = event.detail.items as Task[];
	}

	async function handleFinalize(event: CustomEvent<{ items: Task[] }>): Promise<void> {
		if ($taskDragLockedStore) return;
		const previous = [...sortableSubtasks];
		sortableSubtasks = event.detail.items as Task[];
		setTaskDragLocked(true);
		try {
			for (let index = 0; index < sortableSubtasks.length; index += 1) {
				const task = sortableSubtasks[index];
				await moveTaskWithOptions(task.id, {
					section_id: sectionId,
					parent_id: parentId,
					position: index
				}, { refresh: false });
			}
			await refreshTasksView();
		} catch {
			sortableSubtasks = previous;
			addToast({ message: 'Subtask drag failed. Reverted.', type: 'error' });
		} finally {
			setTimeout(() => setTaskDragLocked(false), 180);
		}
	}
</script>

<div class="subtask-tree" style="margin-left: {depth * 1.25}rem">
	<DragContainer
		items={sortableSubtasks}
		type="task-dnd"
		className="subtask-dnd-zone"
		dragDisabled={$taskDragLockedStore}
		onConsider={handleConsider}
		onFinalize={handleFinalize}
	>
		{#each sortableSubtasks as task (task.id)}
			<DragItem id={task.id}>
				<TaskRow {task} {depth} />
				{#if task.subtasks.length > 0}
					<SubtaskTree subtasks={task.subtasks} {sectionId} parentId={task.id} depth={depth + 1} />
				{/if}
			</DragItem>
		{/each}
	</DragContainer>

	{#if completedSubtasks.length > 0}
		<button class="done-toggle" onclick={() => (showDone = !showDone)}>
			{showDone ? '▼' : '▶'} Done ({completedSubtasks.length})
		</button>
		{#if showDone}
			{#each completedSubtasks as task (task.id)}
				<TaskRow {task} {depth} />
			{/each}
		{/if}
	{/if}
</div>

<style>
	.subtask-tree {
		display: grid;
		gap: 0.05rem;
		border-left: 2px solid var(--border-light);
		padding-left: 0.5rem;
	}

	.done-toggle {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--text-tertiary);
		font-size: 0.7rem;
		font-family: var(--font-body);
		padding: 0.15rem 0;
		transition: color var(--transition);
	}

	.done-toggle:hover {
		color: var(--text-secondary);
	}
</style>

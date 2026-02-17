<script lang="ts">
	import type { Task } from '$lib';
	import { moveTaskWithOptions, refreshTasksView, taskDragLockedStore, setTaskDragLocked } from '$lib/stores/tasks';
	import { addToast } from '$lib/stores/toast';
	import DragContainer from '../dnd/DragContainer.svelte';
	import DragItem from '../dnd/DragItem.svelte';
	import TaskRow from './TaskRow.svelte';
	import SubtaskTree from './SubtaskTree.svelte';

	let {
		tasks,
		sectionId
	}: {
		tasks: Task[];
		sectionId: number;
	} = $props();

	let showCompleted = $state(false);
	let sortableActiveTasks = $state<Task[]>([]);

	const completedTasks = $derived(
		tasks
			.filter((t) => t.is_completed && t.parent_id === null)
			.sort((a, b) => a.position - b.position)
	);

	$effect(() => {
		sortableActiveTasks = tasks
			.filter((t) => !t.is_completed && t.parent_id === null)
			.sort((a, b) => a.position - b.position);
	});

	function handleConsider(event: CustomEvent<{ items: Task[] }>): void {
		sortableActiveTasks = event.detail.items as Task[];
	}

	async function handleFinalize(event: CustomEvent<{ items: Task[] }>): Promise<void> {
		if ($taskDragLockedStore) return;
		const previous = [...sortableActiveTasks];
		sortableActiveTasks = event.detail.items as Task[];
		setTaskDragLocked(true);
		try {
			for (let index = 0; index < sortableActiveTasks.length; index += 1) {
				const task = sortableActiveTasks[index];
				await moveTaskWithOptions(task.id, {
					section_id: sectionId,
					parent_id: null,
					position: index
				}, { refresh: false });
			}
			await refreshTasksView();
		} catch {
			sortableActiveTasks = previous;
			addToast({ message: 'Task drag failed. Reverted.', type: 'error' });
		} finally {
			setTimeout(() => setTaskDragLocked(false), 180);
		}
	}
</script>

<div class="task-list">
	<DragContainer
		items={sortableActiveTasks}
		type="task-dnd"
		className="task-dnd-zone"
		dragDisabled={$taskDragLockedStore}
		onConsider={handleConsider}
		onFinalize={handleFinalize}
	>
		{#each sortableActiveTasks as task (task.id)}
			<DragItem id={task.id} className="task-item">
				<TaskRow {task} />
				<SubtaskTree subtasks={task.subtasks} sectionId={sectionId} parentId={task.id} />
			</DragItem>
		{/each}
	</DragContainer>

	{#if completedTasks.length > 0}
		<div class="completed-section">
			<button class="completed-toggle" onclick={() => (showCompleted = !showCompleted)}>
				<span class="chevron">{showCompleted ? '▼' : '▶'}</span>
				Completed ({completedTasks.length})
			</button>
			{#if showCompleted}
				{#each completedTasks as task (task.id)}
					<TaskRow {task} />
				{/each}
			{/if}
		</div>
	{/if}
</div>

<style>
	.task-list {
		display: grid;
		gap: 0.1rem;
	}

	.completed-section {
		margin-top: 0.5rem;
		border-top: 1px solid var(--border-light);
		padding-top: 0.4rem;
	}

	.completed-toggle {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--text-tertiary);
		font-size: 0.78rem;
		font-weight: 600;
		font-family: var(--font-body);
		padding: 0.25rem 0;
		display: flex;
		align-items: center;
		gap: 0.3rem;
		transition: color var(--transition);
	}

	.completed-toggle:hover {
		color: var(--text-secondary);
	}

	.chevron {
		font-size: 0.6rem;
	}
</style>

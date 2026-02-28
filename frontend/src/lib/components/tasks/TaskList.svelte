<script lang="ts">
	import type { Task } from '$lib';
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

	const activeTasks = $derived(
		tasks
			.filter((t) => !t.is_completed && t.parent_id === null)
			.sort((a, b) => a.position - b.position)
	);

	const completedTasks = $derived(
		tasks
			.filter((t) => t.is_completed && t.parent_id === null)
			.sort((a, b) => a.position - b.position)
	);
</script>

<div class="task-list">
	{#each activeTasks as task (task.id)}
		<TaskRow {task} />
		<SubtaskTree subtasks={task.subtasks} sectionId={sectionId} parentId={task.id} />
	{/each}

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

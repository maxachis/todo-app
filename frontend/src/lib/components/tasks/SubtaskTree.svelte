<script lang="ts">
	import type { Task } from '$lib';
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

	let showDone = $state(false);

	const activeSubtasks = $derived(
		subtasks.filter((t) => !t.is_completed).sort((a, b) => a.position - b.position)
	);

	const completedSubtasks = $derived(
		subtasks.filter((t) => t.is_completed).sort((a, b) => a.position - b.position)
	);
</script>

<div class="subtask-tree" style="margin-left: {depth * 1.25}rem">
	{#each activeSubtasks as task (task.id)}
		<TaskRow {task} {depth} />
		{#if task.subtasks.length > 0}
			<SubtaskTree subtasks={task.subtasks} {sectionId} parentId={task.id} depth={depth + 1} />
		{/if}
	{/each}

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

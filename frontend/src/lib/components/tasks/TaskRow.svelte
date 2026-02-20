<script lang="ts">
	import type { Task } from '$lib';
	import { selectedListDetail } from '$lib/stores/lists';
	import { selectedTaskStore, selectTask, completeTask, uncompleteTask, togglePin, moveTask, taskDragLockedStore, setTaskDragLocked } from '$lib/stores/tasks';
	import { addToast } from '$lib/stores/toast';

	let {
		task,
		depth = 0
	}: {
		task: Task;
		depth?: number;
	} = $props();

	let editing = $state(false);
	let title = $state('');
	let dropMode = $state<'before' | 'nest' | null>(null);

	const isSelected = $derived($selectedTaskStore === task.id);

	const openSubtaskCount = $derived(
		task.subtasks.filter((s) => !s.is_completed).length
	);
	const totalSubtaskCount = $derived(task.subtasks.length);

	const dueDateFormatted = $derived(() => {
		if (!task.due_date) return null;
		const d = new Date(task.due_date + 'T00:00:00');
		return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
	});

	function handleClick(event: MouseEvent): void {
		selectTask(task.id);
		(event.currentTarget as HTMLElement | null)?.focus();
	}

	async function handleCheck(): Promise<void> {
		if (task.is_completed) {
			await uncompleteTask(task.id);
		} else {
			await completeTask(task.id);
			addToast({
				message: `"${task.title}" completed`,
				type: 'success',
				actionLabel: 'Undo',
				onAction: () => uncompleteTask(task.id)
			});
		}
	}

	async function handlePin(event: MouseEvent): Promise<void> {
		event.stopPropagation();
		try {
			await togglePin(task.id);
		} catch {
			addToast({ message: 'Max 3 pinned tasks per list', type: 'error' });
		}
	}

	function startEdit(): void {
		editing = true;
		title = task.title;
	}

	function commitEdit(): void {
		editing = false;
		if (title.trim() && title !== task.title) {
			import('$lib/stores/tasks').then(({ updateTask }) => {
				updateTask(task.id, { title: title.trim() });
			});
		}
	}

	function findTaskById(tasks: Task[], taskId: number): Task | null {
		for (const candidate of tasks) {
			if (candidate.id === taskId) return candidate;
			const nested = findTaskById(candidate.subtasks, taskId);
			if (nested) return nested;
		}
		return null;
	}

	function siblingsForTask(target: Task): Task[] {
		const list = $selectedListDetail;
		if (!list) return [];
		const section = list.sections.find((s) => s.id === target.section_id);
		if (!section) return [];
		if (target.parent_id === null) {
			return section.tasks
				.filter((t) => t.parent_id === null)
				.sort((a, b) => a.position - b.position);
		}
		const parent = findTaskById(section.tasks, target.parent_id);
		return (parent?.subtasks ?? []).slice().sort((a, b) => a.position - b.position);
	}

	function midpointDropMode(event: DragEvent): 'before' | 'nest' {
		const bounds = (event.currentTarget as HTMLElement).getBoundingClientRect();
		return event.clientY >= bounds.top + bounds.height / 2 ? 'nest' : 'before';
	}

	async function handleDropOnTask(event: DragEvent): Promise<void> {
		event.preventDefault();
		event.stopPropagation();
		dropMode = null;

		const dragTaskId = Number(event.dataTransfer?.getData('text/task-id'));
		if (Number.isNaN(dragTaskId) || dragTaskId === task.id) return;
		if ($taskDragLockedStore) return;

		try {
			setTaskDragLocked(true);
			if (midpointDropMode(event) === 'nest') {
				await moveTask(dragTaskId, {
					section_id: task.section_id,
					parent_id: task.id,
					position: 0
				});
				return;
			}

			const siblings = siblingsForTask(task);
			const index = siblings.findIndex((sibling) => sibling.id === task.id);
			await moveTask(dragTaskId, {
				section_id: task.section_id,
				parent_id: task.parent_id ?? null,
				position: index < 0 ? 0 : index
			});
		} catch {
			addToast({ message: 'Task drag failed. Reverted.', type: 'error' });
		} finally {
			setTimeout(() => setTaskDragLocked(false), 180);
		}
	}
</script>

<div
	class="task-row"
	class:selected={isSelected}
	class:completed={task.is_completed}
	class:drop-before={dropMode === 'before'}
	class:drop-nest={dropMode === 'nest'}
	role="button"
	tabindex="0"
	onclick={handleClick}
	ondblclick={startEdit}
	onkeydown={(e) => {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			handleClick(e as unknown as MouseEvent);
		}
	}}
	data-task-id={task.id}
	data-section-id={task.section_id}
	data-parent-id={task.parent_id}
	draggable={!task.is_completed}
	ondragstart={(event) => {
		if ($taskDragLockedStore) {
			event.preventDefault();
			return;
		}
		event.dataTransfer?.setData('text/task-id', String(task.id));
		event.dataTransfer?.setData('text/section-id', String(task.section_id));
	}}
	ondragover={(event) => {
		if (task.is_completed) return;
		const draggedTaskId = Number(event.dataTransfer?.getData('text/task-id'));
		if (Number.isNaN(draggedTaskId) || draggedTaskId === task.id) return;
		event.preventDefault();
		dropMode = midpointDropMode(event);
	}}
	ondragleave={() => {
		dropMode = null;
	}}
	ondrop={handleDropOnTask}
>
	<input
		type="checkbox"
		checked={task.is_completed}
		onclick={(e) => e.stopPropagation()}
		onchange={handleCheck}
		class="checkbox"
	/>

	{#if editing}
		<input
			class="title-input"
			bind:value={title}
			onblur={commitEdit}
			onkeydown={(e) => {
				if (e.key === 'Enter') commitEdit();
				if (e.key === 'Escape') editing = false;
			}}
		/>
	{:else}
		<span class="title" class:completed-text={task.is_completed}>{task.title}</span>
	{/if}

	<div class="meta">
		{#if task.tags.length > 0}
			<div class="tags">
				{#each task.tags as tag}
					<span class="tag">{tag.name}</span>
				{/each}
			</div>
		{/if}
		{#if dueDateFormatted()}
			<span class="due-date">{dueDateFormatted()}</span>
		{/if}
		{#if totalSubtaskCount > 0}
			<span class="subtask-count">{totalSubtaskCount} subtasks — {openSubtaskCount} open</span>
		{/if}
	</div>

	{#if !task.is_completed}
		<button
			class="pin-btn"
			class:pinned={task.is_pinned}
			onclick={handlePin}
			aria-label={task.is_pinned ? 'Unpin task' : 'Pin task'}
		>
			📌
		</button>
	{/if}
</div>

<style>
	.task-row {
		display: grid;
		grid-template-columns: auto 1fr auto auto;
		gap: 0.45rem;
		align-items: center;
		padding: 0.45rem 0.55rem;
		border-radius: var(--radius-sm);
		cursor: pointer;
		min-height: 2.1rem;
		transition: background var(--transition);
	}

	.task-row:hover {
		background: var(--bg-surface-hover);
	}

	.task-row.selected {
		background: var(--accent-light);
		box-shadow: inset 3px 0 0 var(--accent);
	}

	.task-row.completed {
		opacity: 0.5;
	}

	.task-row.drop-before {
		box-shadow: inset 0 2px 0 var(--accent);
	}

	.task-row.drop-nest {
		box-shadow: inset 3px 0 0 var(--accent);
	}

	.checkbox {
		cursor: pointer;
		width: 1rem;
		height: 1rem;
		accent-color: var(--accent);
	}

	.title {
		font-size: 0.88rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		color: var(--text-primary);
	}

	.completed-text {
		text-decoration: line-through;
		color: var(--text-tertiary);
	}

	.title-input {
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.2rem 0.4rem;
		font-size: 0.88rem;
		font-family: var(--font-body);
		color: var(--text-primary);
	}

	.title-input:focus {
		outline: none;
	}

	.meta {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		font-size: 0.72rem;
		color: var(--text-secondary);
		white-space: nowrap;
	}

	.tags {
		display: flex;
		gap: 0.2rem;
	}

	.tag {
		background: var(--tag-bg);
		color: var(--tag-text);
		padding: 0.1rem 0.4rem;
		border-radius: var(--radius-sm);
		font-size: 0.68rem;
		font-weight: 500;
	}

	.due-date {
		color: var(--accent);
		font-weight: 600;
	}

	.subtask-count {
		color: var(--text-tertiary);
	}

	.pin-btn {
		background: transparent;
		border: none;
		cursor: pointer;
		font-size: 0.8rem;
		opacity: 0;
		transition: opacity var(--transition);
		padding: 0.15rem;
	}

	.task-row:hover .pin-btn,
	.pin-btn.pinned {
		opacity: 1;
	}

	.pin-btn:not(.pinned) {
		filter: grayscale(1);
	}
</style>

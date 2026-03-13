<script lang="ts">
	import { untrack } from 'svelte';
	import type { Task } from '$lib';
	import { moveTaskWithOptions, moveTask, refreshTasksView, taskDragLockedStore, setTaskDragLocked, draggedTaskIdStore, nestIntentStore } from '$lib/stores/tasks';
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

	let sortableActiveTasks = $state<Task[]>([]);
	let removalTimeout: ReturnType<typeof setTimeout> | null = null;

	$effect(() => {
		const activeTasks = tasks
			.filter((t) => !t.is_completed && t.parent_id === null)
			.sort((a, b) => a.position - b.position);

		// Detect tasks that just completed (in current list but not in new filtered set)
		// Use untrack() to avoid reactive dependency on sortableActiveTasks — without this,
		// writing sortableActiveTasks below would re-trigger this effect, causing cascading
		// DnD zone reconfigurations with large task counts.
		const activeIds = new Set(activeTasks.map((t) => t.id));
		const justCompleted = untrack(() => sortableActiveTasks).filter((t) => !activeIds.has(t.id));

		if (removalTimeout !== null) {
			clearTimeout(removalTimeout);
			removalTimeout = null;
		}

		if (justCompleted.length > 0) {
			// Keep completed tasks visible briefly so the check animation plays
			// and the scroll position adjusts smoothly (prevents black flash)
			const completedInPlace = justCompleted.map((t) => {
				const updated = tasks.find((task) => task.id === t.id);
				return updated ?? t;
			});
			sortableActiveTasks = [...activeTasks, ...completedInPlace];
			removalTimeout = setTimeout(() => {
				sortableActiveTasks = activeTasks;
				removalTimeout = null;
			}, 300);
		} else {
			sortableActiveTasks = activeTasks;
		}
	});

	function handleConsider(event: CustomEvent<{ items: Task[]; info: { id: string } }>): void {
		sortableActiveTasks = event.detail.items as Task[];
		draggedTaskIdStore.set(Number(event.detail.info.id));
	}

	async function handleFinalize(event: CustomEvent<{ items: Task[]; info: { id: string } }>): Promise<void> {
		const nestIntent = $nestIntentStore;
		draggedTaskIdStore.set(null);
		nestIntentStore.set(null);

		if ($taskDragLockedStore) return;
		const draggedId = Number(event.detail.info.id);

		if (nestIntent) {
			setTaskDragLocked(true);
			try {
				await moveTask(draggedId, {
					section_id: nestIntent.targetSectionId,
					parent_id: nestIntent.targetTaskId,
					position: 0
				});
			} catch {
				addToast({ message: 'Task nesting failed. Reverted.', type: 'error' });
			} finally {
				setTimeout(() => setTaskDragLocked(false), 180);
			}
			return;
		}

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
</div>

<style>
	.task-list {
		display: grid;
		gap: 0.1rem;
	}

	.task-list :global(.task-dnd-zone) {
		min-height: 1.5rem;
	}

</style>

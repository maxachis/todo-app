<script lang="ts">
	import {
		selectedListDetail,
		selectedListStore,
		listsStore,
		createSection,
		updateSection,
		deleteSection,
		moveSection,
		selectList,
		updateList
	} from '$lib/stores/lists';
	import { projectsStore, loadProjects } from '$lib/stores/projects';
	import { keyboard } from '$lib/actions/keyboard';
	import SectionList from '$lib/components/sections/SectionList.svelte';
	import PinnedSection from '$lib/components/tasks/PinnedSection.svelte';
	import EmojiPicker from '$lib/components/lists/EmojiPicker.svelte';
	import ExportButton from '$lib/components/shared/ExportButton.svelte';
	import { completeTask, deleteTask, moveTask, selectTask, selectedTaskStore } from '$lib/stores/tasks';
	import type { Task } from '$lib';

	let allCollapsed = $state(false);
	let creatingSectionName = $state('');
	let listNameEditing = $state(false);
	let listNameEditingListId = $state<number | null>(null);
	let listNameDraft = $state('');
	let listEmojiPickerOpen = $state(false);
	let previousListId = $state<number | null>(null);
	let pinnedOrderByList = $state<Record<number, number[]>>({});

	const currentList = $derived($selectedListDetail);

	const pinnedTasks = $derived(
		(() => {
			if (!currentList) return [];
			const pinned = currentList.sections
				.flatMap((s) => s.tasks)
				.filter((t) => t.is_pinned && !t.is_completed);
			const pinnedOrder = pinnedOrderByList[currentList.id] ?? [];
			return pinned.sort((a, b) => {
				const aIndex = pinnedOrder.indexOf(a.id);
				const bIndex = pinnedOrder.indexOf(b.id);
				if (aIndex >= 0 && bIndex >= 0) return aIndex - bIndex;
				if (aIndex >= 0) return -1;
				if (bIndex >= 0) return 1;
				const dateCmp = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
				return dateCmp !== 0 ? dateCmp : a.id - b.id;
			});
		})()
	);

	$effect(() => {
		loadProjects();
	});

	$effect(() => {
		if (currentList && !listNameEditing) {
			listNameDraft = currentList.name;
		}
	});

	$effect(() => {
		const currentId = currentList?.id ?? null;
		if (
			listNameEditing &&
			listNameEditingListId !== null &&
			previousListId !== null &&
			previousListId !== currentId &&
			listNameEditingListId === previousListId
		) {
			void commitListName(listNameEditingListId);
		}
		previousListId = currentId;
	});

	async function handleCreateSection(): Promise<void> {
		const name = creatingSectionName.trim();
		if (!name || !$selectedListStore) return;
		await createSection($selectedListStore, { name });
		creatingSectionName = '';
	}

	async function handleUpdateSection(id: number, changes: { name?: string; emoji?: string }): Promise<void> {
		await updateSection(id, changes);
	}

	async function handleDeleteSection(id: number): Promise<void> {
		if (!confirm('Delete this section and all its tasks?')) return;
		await deleteSection(id);
	}

	async function handleMoveSection(id: number, pos: number): Promise<void> {
		await moveSection(id, pos);
	}

	async function handleCycleList(direction: 'prev' | 'next'): Promise<void> {
		const currentId = $selectedListStore;
		const lists = $listsStore;
		if (!lists.length) return;
		const currentIndex = lists.findIndex((l) => l.id === currentId);
		const start = currentIndex >= 0 ? currentIndex : 0;
		const offset = direction === 'next' ? 1 : -1;
		const nextIndex = (start + offset + lists.length) % lists.length;
		await selectList(lists[nextIndex].id);
	}

	async function handleAssignProject(event: Event): Promise<void> {
		const target = event.target as HTMLSelectElement;
		if (!$selectedListStore) return;
		const raw = target.value;
		await updateList($selectedListStore, {
			project_id: raw === '' ? null : Number(raw)
		});
	}

	async function commitListName(targetListId: number | null = listNameEditingListId): Promise<void> {
		if (targetListId === null) return;
		const trimmed = listNameDraft.trim();
		listNameEditing = false;
		listNameEditingListId = null;
		const target = $listsStore.find((list) => list.id === targetListId);
		if (trimmed && target && trimmed !== target.name) {
			await updateList(targetListId, { name: trimmed });
		}
	}

	function startListNameEdit(): void {
		if (!currentList) return;
		listNameDraft = currentList.name;
		listNameEditing = true;
		listNameEditingListId = currentList.id;
	}

	async function handleListEmojiSelect(emoji: string): Promise<void> {
		if (!currentList) return;
		await updateList(currentList.id, { emoji });
		listEmojiPickerOpen = false;
	}

	function handlePinnedReorder(ids: number[]): void {
		if (!currentList) return;
		pinnedOrderByList = {
			...pinnedOrderByList,
			[currentList.id]: ids
		};
	}

	function findTaskById(tasks: Task[], taskId: number): Task | null {
		for (const task of tasks) {
			if (task.id === taskId) return task;
			const nested = findTaskById(task.subtasks, taskId);
			if (nested) return nested;
		}
		return null;
	}
</script>

{#if currentList}
	<section class="task-view">
		<div
			class="keyboard-scope"
			use:keyboard={{
				getCurrentTaskId: () => $selectedTaskStore,
				onSelectTask: selectTask,
				onCompleteTask: async (taskId) => {
					await completeTask(taskId);
				},
				onDeleteTask: deleteTask,
				onIndentTask: async (taskId, parentId, sectionId) => {
					await moveTask(taskId, { parent_id: parentId, section_id: sectionId, position: 0 });
				},
				onOutdentTask: async (taskId, sectionId) => {
					const section = currentList?.sections.find((s) => s.id === sectionId);
					if (!section) return;
					const task = findTaskById(section.tasks, taskId);
					if (!task || task.parent_id === null) return;

					const parent = findTaskById(section.tasks, task.parent_id);
					if (!parent) return;

					const targetParentId = parent.parent_id ?? null;
					let targetPosition = 0;

					if (targetParentId === null) {
						const topLevel = section.tasks
							.filter((t) => t.parent_id === null)
							.sort((a, b) => a.position - b.position);
						const parentIndex = topLevel.findIndex((t) => t.id === parent.id);
						targetPosition = parentIndex >= 0 ? parentIndex + 1 : topLevel.length;
					} else {
						const grandParent = findTaskById(section.tasks, targetParentId);
						const siblings = (grandParent?.subtasks ?? [])
							.sort((a, b) => a.position - b.position);
						const parentIndex = siblings.findIndex((t) => t.id === parent.id);
						targetPosition = parentIndex >= 0 ? parentIndex + 1 : siblings.length;
					}

					await moveTask(taskId, {
						parent_id: targetParentId,
						section_id: sectionId,
						position: targetPosition
					});
				},
				onCycleList: handleCycleList
			}}
		>
		<header class="list-header">
			<h1>
				<button
					type="button"
					class="list-emoji-btn"
					ondblclick={() => (listEmojiPickerOpen = true)}
					aria-label="Edit list emoji"
				>
					{currentList.emoji || '\u{1F4DD}'}
				</button>
				{#if listNameEditing}
					<input
						class="list-name-input"
						bind:value={listNameDraft}
						onblur={() => commitListName()}
						onkeydown={(event) => {
							if (event.key === 'Enter') commitListName();
							if (event.key === 'Escape') {
								listNameEditing = false;
								listNameEditingListId = null;
							}
						}}
					/>
				{:else}
					<span class="list-name" ondblclick={startListNameEdit} role="button" tabindex="0">{currentList.name}</span>
				{/if}
			</h1>
			<div class="header-actions">
				<select class="project-select" onchange={handleAssignProject} value={currentList.project_id ?? ''}>
					<option value="">No Project</option>
					{#each $projectsStore as project}
						<option value={project.id}>{project.name}</option>
					{/each}
				</select>
				<ExportButton listId={currentList.id} label="Export" />
				<button
					class="collapse-btn"
					onclick={() => (allCollapsed = !allCollapsed)}
				>
					{allCollapsed ? 'Expand All' : 'Collapse All'}
				</button>
			</div>
		</header>

		<PinnedSection tasks={pinnedTasks} onReorder={handlePinnedReorder} />

		<SectionList
			sections={currentList.sections}
			{allCollapsed}
			onUpdateSection={handleUpdateSection}
			onDeleteSection={handleDeleteSection}
			onMoveSection={handleMoveSection}
		/>

		<form class="section-create" onsubmit={(e) => { e.preventDefault(); handleCreateSection(); }}>
			<input bind:value={creatingSectionName} placeholder="Add section..." />
			<button type="submit">+ Section</button>
		</form>
		</div>
	</section>

	<EmojiPicker
		open={listEmojiPickerOpen}
		onClose={() => (listEmojiPickerOpen = false)}
		onSelect={handleListEmojiSelect}
	/>
{:else}
	<section class="task-view">
		<div class="empty-state">
			<p>Select or create a list.</p>
		</div>
	</section>
{/if}

<style>
	.task-view {
		display: grid;
		gap: 0.75rem;
	}

	.keyboard-scope {
		display: grid;
		gap: 0.75rem;
		outline: none;
	}

	.list-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
	}

	h1 {
		margin: 0;
		display: flex;
		align-items: center;
		gap: 0.35rem;
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--text-primary);
		letter-spacing: -0.01em;
	}

	.list-emoji-btn {
		border: none;
		background: transparent;
		padding: 0;
		font-size: inherit;
		line-height: 1;
		cursor: pointer;
	}

	.list-name {
		cursor: pointer;
	}

	.list-name-input {
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.15rem 0.35rem;
		font-family: var(--font-display);
		font-size: 1.1rem;
		color: var(--text-primary);
		background: var(--bg-input);
	}

	.list-name-input:focus {
		outline: none;
	}

	.header-actions {
		display: flex;
		gap: 0.35rem;
	}

	.collapse-btn {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.project-select {
		border: 1px solid var(--border);
		background: var(--bg-input);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.45rem;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-primary);
	}

	.project-select:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.collapse-btn:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.section-create {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.35rem;
		margin-top: 0.75rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--border-light);
	}

	.section-create input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		background: var(--bg-input);
		transition: border-color var(--transition);
	}

	.section-create input::placeholder {
		color: var(--text-tertiary);
	}

	.section-create input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.section-create button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.65rem;
		cursor: pointer;
		font-size: 0.82rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.section-create button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.empty-state {
		border: 2px dashed var(--border);
		border-radius: var(--radius-lg);
		min-height: 220px;
		display: grid;
		place-items: center;
		background: var(--bg-surface-hover);
	}

	p {
		margin: 0;
		color: var(--text-secondary);
		font-weight: 500;
	}
</style>

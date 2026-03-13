<script lang="ts">
	import type { Tag, Task, Person, Organization, List, Section, TaskPersonLink, TaskOrganizationLink } from '$lib';
	import { api } from '$lib';
	import { updateTask, selectedTaskDetail, selectTask, refreshTask, moveTask, deleteTask } from '$lib/stores/tasks';
	import { listsStore, loadListDetail } from '$lib/stores/lists';
	import NotesEditor from '../shared/NotesEditor.svelte';
	import LinkedEntities from '../shared/LinkedEntities.svelte';
	import TypeaheadSelect from '../shared/TypeaheadSelect.svelte';
	import RecurrenceEditor from './RecurrenceEditor.svelte';
	import NotebookMentions from '../shared/NotebookMentions.svelte';

	const task = $derived($selectedTaskDetail);

	let titleValue = $state('');
	let dueDateValue = $state('');
	let notesValue = $state('');

	let availableTags = $state<Tag[]>([]);

	let linkedPeopleIds = $state<number[]>([]);
	let linkedOrgIds = $state<number[]>([]);
	let allPeople = $state<Person[]>([]);
	let allOrgs = $state<Organization[]>([]);

	// List/Section triage
	let selectedListId = $state<number | null>(null);
	let selectedSectionId = $state<number | null>(null);
	let targetSections = $state<Section[]>([]);

	let prevTaskId = $state<number | null>(null);

	$effect(() => {
		const currentId = task?.id ?? null;
		if (task && currentId !== prevTaskId) {
			prevTaskId = currentId;
			titleValue = task.title;
			dueDateValue = task.due_date ?? '';
			notesValue = task.notes;
			loadAvailableTags(task.id);
			loadLinkedEntities(task.id);
			initListSection(task);
		}
		if (!task) {
			prevTaskId = null;
		}
	});

	function initListSection(t: Task): void {
		// Find which list this task's section belongs to
		const lists = $listsStore;
		for (const list of lists) {
			const section = list.sections.find((s) => s.id === t.section_id);
			if (section) {
				selectedListId = list.id;
				selectedSectionId = section.id;
				targetSections = list.sections;
				return;
			}
		}
	}

	async function handleListChange(event: Event): Promise<void> {
		const target = event.target as HTMLSelectElement;
		const newListId = Number(target.value);
		if (!task || Number.isNaN(newListId) || newListId === selectedListId) return;

		// Load the target list's sections
		const detail = await loadListDetail(newListId);
		targetSections = detail.sections;
		selectedListId = newListId;

		// Pre-select first section and move
		if (targetSections.length > 0) {
			selectedSectionId = targetSections[0].id;
			await moveTask(task.id, { section_id: targetSections[0].id });
		}
	}

	async function handleSectionChange(event: Event): Promise<void> {
		const target = event.target as HTMLSelectElement;
		const newSectionId = Number(target.value);
		if (!task || Number.isNaN(newSectionId) || newSectionId === task.section_id) return;
		selectedSectionId = newSectionId;
		await moveTask(task.id, { section_id: newSectionId });
	}

	async function loadLinkedEntities(taskId: number): Promise<void> {
		const [personLinks, orgLinks, people, orgs] = await Promise.all([
			api.taskLinks.people.list(taskId),
			api.taskLinks.organizations.list(taskId),
			api.people.getAll(),
			api.organizations.getAll()
		]);
		linkedPeopleIds = personLinks.map((l) => l.person_id);
		linkedOrgIds = orgLinks.map((l) => l.organization_id);
		allPeople = people;
		allOrgs = orgs;
	}

	async function addPersonLink(personId: number): Promise<void> {
		if (!task) return;
		await api.taskLinks.people.add(task.id, personId);
		linkedPeopleIds = [...linkedPeopleIds, personId];
	}

	async function removePersonLink(personId: number): Promise<void> {
		if (!task) return;
		await api.taskLinks.people.remove(task.id, personId);
		linkedPeopleIds = linkedPeopleIds.filter((id) => id !== personId);
	}

	async function addOrgLink(orgId: number): Promise<void> {
		if (!task) return;
		await api.taskLinks.organizations.add(task.id, orgId);
		linkedOrgIds = [...linkedOrgIds, orgId];
	}

	async function removeOrgLink(orgId: number): Promise<void> {
		if (!task) return;
		await api.taskLinks.organizations.remove(task.id, orgId);
		linkedOrgIds = linkedOrgIds.filter((id) => id !== orgId);
	}

	function personName(p: { id: number }): string {
		const person = allPeople.find((x) => x.id === p.id);
		return person ? `${person.first_name} ${person.last_name}`.trim() : `Person #${p.id}`;
	}

	function orgName(o: { id: number }): string {
		const org = allOrgs.find((x) => x.id === o.id);
		return org ? org.name : `Org #${o.id}`;
	}

	async function loadAvailableTags(taskId: number): Promise<void> {
		availableTags = await api.tags.list(taskId);
	}

	async function saveTitle(): Promise<void> {
		if (!task || titleValue === task.title) return;
		await updateTask(task.id, { title: titleValue.trim() });
	}

	async function saveDueDate(): Promise<void> {
		if (!task) return;
		const value = dueDateValue || null;
		if (value === task.due_date) return;
		await updateTask(task.id, { due_date: value });
	}

	async function saveRecurrence(payload: import('$lib').UpdateTaskInput): Promise<void> {
		if (!task) return;
		await updateTask(task.id, payload);
	}

	async function saveNotes(next: string): Promise<void> {
		if (!task || next === task.notes) return;
		notesValue = next;
		await updateTask(task.id, { notes: next });
	}

	const tagOptions = $derived(
		availableTags.map((t) => ({ id: t.id, label: t.name }))
	);

	async function onTagSelect(tagId: number): Promise<void> {
		if (!task) return;
		const tag = availableTags.find((t) => t.id === tagId);
		if (!tag) return;
		await api.tasks.addTag(task.id, tag.name);
		await refreshTask(task.id);
		await loadAvailableTags(task.id);
	}

	async function onTagCreate(name: string): Promise<{ id: number; label: string }> {
		if (!task) throw new Error('No task selected');
		const tags = await api.tasks.addTag(task.id, name);
		await refreshTask(task.id);
		await loadAvailableTags(task.id);
		const created = tags.find((t) => t.name.toLowerCase() === name.toLowerCase());
		return created ? { id: created.id, label: created.name } : { id: 0, label: name };
	}

	async function removeTag(tagId: number): Promise<void> {
		if (!task) return;
		await api.tasks.removeTag(task.id, tagId);
		await refreshTask(task.id);
	}

	async function handleDelete(): Promise<void> {
		if (!task) return;
		if (confirm('Delete this task?')) {
			await deleteTask(task.id);
		}
	}

	function jumpToParent(): void {
		if (!task?.parent_id) return;
		const el = document.querySelector(`[data-task-id="${task.parent_id}"]`);
		if (el) {
			el.scrollIntoView({ behavior: 'smooth', block: 'center' });
			el.classList.add('flash');
			setTimeout(() => el.classList.remove('flash'), 800);
		}
		selectTask(task.parent_id);
	}

</script>

{#if task}
	<div class="detail">
		{#if task.parent_id}
			<button class="parent-link" onclick={jumpToParent}>↑ Jump to parent task</button>
		{/if}

		<div class="field">
			<label for="detail-title">Title</label>
			<input
				id="detail-title"
				bind:value={titleValue}
				onblur={saveTitle}
				onkeydown={(e) => { if (e.key === 'Enter') e.currentTarget.blur(); }}
			/>
		</div>

		<div class="field">
			<label for="detail-due">Due Date</label>
			<input
				id="detail-due"
				type="date"
				bind:value={dueDateValue}
				onblur={saveDueDate}
				onchange={saveDueDate}
			/>
		</div>

		<div class="field">
			<RecurrenceEditor {task} onSave={saveRecurrence} />
		</div>

		<div class="field location-field">
			<label>List</label>
			<select value={selectedListId} onchange={handleListChange}>
				{#each $listsStore as list}
					<option value={list.id}>{list.emoji || '\u{1F4DD}'} {list.name}</option>
				{/each}
			</select>
		</div>

		{#if targetSections.length > 1 || (targetSections.length === 1 && targetSections[0].name !== '')}
			<div class="field location-field">
				<label>Section</label>
				<select value={selectedSectionId} onchange={handleSectionChange}>
					{#each targetSections as section}
						<option value={section.id}>{section.name || '(default)'}</option>
					{/each}
				</select>
			</div>
		{/if}

		<div class="field">
			<label>Tags</label>
			<div class="tags">
				{#each task.tags as tag}
					<span class="tag">
						{tag.name}
						<button onclick={() => removeTag(tag.id)}>✕</button>
					</span>
				{/each}
			</div>
			<TypeaheadSelect
				options={tagOptions}
				placeholder="Add tag..."
				onSelect={onTagSelect}
				onCreate={onTagCreate}
			/>
		</div>

		<div class="field linked-section">
			<label>Linked People &amp; Orgs</label>
			{#if linkedPeopleIds.length === 0 && linkedOrgIds.length === 0 && allPeople.length === 0 && allOrgs.length === 0}
				<p class="empty-links">No linked people or organizations</p>
			{:else}
				<LinkedEntities
					label="People"
					entities={allPeople}
					linkedIds={linkedPeopleIds}
					getDisplayName={personName}
					onAdd={addPersonLink}
					onRemove={removePersonLink}
				/>
				<LinkedEntities
					label="Organizations"
					entities={allOrgs}
					linkedIds={linkedOrgIds}
					getDisplayName={orgName}
					onAdd={addOrgLink}
					onRemove={removeOrgLink}
				/>
			{/if}
		</div>

		<div class="field">
			<label for="detail-notes">Notes</label>
			<div id="detail-notes">
				<NotesEditor
					value={notesValue}
					onSave={saveNotes}
				/>
			</div>
		</div>

		<NotebookMentions entityType="task" entityId={task.id} />

		<div class="field delete-section">
			<button class="delete-btn" onclick={handleDelete}>Delete Task</button>
		</div>
	</div>
{:else}
	<p class="placeholder">Select a task to view details.</p>
{/if}

<style>
	.detail {
		display: grid;
		gap: 0.85rem;
	}

	.parent-link {
		background: transparent;
		border: 1px solid var(--accent-medium);
		color: var(--accent);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.5rem;
		cursor: pointer;
		font-size: 0.8rem;
		font-family: var(--font-body);
		text-align: left;
		transition: all var(--transition);
	}

	.parent-link:hover {
		background: var(--accent-light);
	}

	.field {
		display: grid;
		gap: 0.3rem;
	}

	label {
		font-size: 0.7rem;
		font-weight: 600;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.06em;
	}

	input,
	select {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.55rem;
		font-size: 0.88rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
		transition: border-color var(--transition);
	}

	input:focus,
	select:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	input::placeholder {
		color: var(--text-tertiary);
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.3rem;
	}

	.tag {
		background: var(--tag-bg);
		color: var(--tag-text);
		padding: 0.18rem 0.45rem;
		border-radius: var(--radius-sm);
		font-size: 0.78rem;
		font-weight: 500;
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
	}

	.tag button {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--text-tertiary);
		font-size: 0.7rem;
		padding: 0;
		transition: color var(--transition);
	}

	.tag button:hover {
		color: var(--error);
	}

	.empty-links {
		color: var(--text-tertiary);
		font-size: 0.82rem;
		font-style: italic;
		margin: 0;
	}

	.delete-section {
		border-top: 1px solid var(--border-light);
		padding-top: 0.6rem;
	}

	.delete-btn {
		background: transparent;
		border: 1px solid var(--error, #dc3545);
		color: var(--error, #dc3545);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.75rem;
		font-size: 0.82rem;
		font-family: var(--font-body);
		cursor: pointer;
		transition: all var(--transition);
	}

	.delete-btn:hover {
		background: var(--error, #dc3545);
		color: #fff;
	}

	.linked-section {
		border-top: 1px solid var(--border-light);
		padding-top: 0.6rem;
	}

	.placeholder {
		color: var(--text-tertiary);
		margin: 0;
		font-style: italic;
	}

	@media (max-width: 640px) {
		.tag {
			min-height: 44px;
			display: inline-flex;
			align-items: center;
		}

		.tag button {
			min-height: 44px;
			min-width: 44px;
			display: inline-flex;
			align-items: center;
			justify-content: center;
		}

		input,
		select {
			padding: 0.55rem 0.65rem;
			font-size: 1rem;
		}

		.parent-link {
			min-height: 44px;
			display: inline-flex;
			align-items: center;
		}
	}
</style>

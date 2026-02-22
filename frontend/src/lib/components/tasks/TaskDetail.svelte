<script lang="ts">
	import type { Tag, Task, Person, Organization, TaskPersonLink, TaskOrganizationLink } from '$lib';
	import { api } from '$lib';
	import { updateTask, selectedTaskDetail, selectTask } from '$lib/stores/tasks';
	import MarkdownEditor from '../shared/MarkdownEditor.svelte';
	import LinkedEntities from '../shared/LinkedEntities.svelte';
	import RecurrenceEditor from './RecurrenceEditor.svelte';

	const task = $derived($selectedTaskDetail);

	let titleValue = $state('');
	let dueDateValue = $state('');
	let priorityValue = $state(0);
	let notesValue = $state('');

	let tagInput = $state('');
	let availableTags = $state<Tag[]>([]);

	let linkedPeopleIds = $state<number[]>([]);
	let linkedOrgIds = $state<number[]>([]);
	let allPeople = $state<Person[]>([]);
	let allOrgs = $state<Organization[]>([]);

	$effect(() => {
		if (task) {
			titleValue = task.title;
			dueDateValue = task.due_date ?? '';
			priorityValue = task.priority;
			notesValue = task.notes;
			loadAvailableTags(task.id);
			loadLinkedEntities(task.id);
		}
	});

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

	async function savePriority(): Promise<void> {
		if (!task || priorityValue === task.priority) return;
		await updateTask(task.id, { priority: priorityValue });
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

	async function addTag(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!task || !tagInput.trim()) return;
		await api.tasks.addTag(task.id, tagInput.trim());
		tagInput = '';
		await selectTask(task.id);
	}

	async function removeTag(tagId: number): Promise<void> {
		if (!task) return;
		await api.tasks.removeTag(task.id, tagId);
		await selectTask(task.id);
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

	const priorityLabels: Record<number, string> = {
		0: 'None',
		1: 'Low',
		3: 'Medium',
		5: 'High'
	};
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

		<div class="field">
			<label for="detail-priority">Priority</label>
			<select
				id="detail-priority"
				bind:value={priorityValue}
				onchange={savePriority}
			>
				{#each Object.entries(priorityLabels) as [val, label]}
					<option value={Number(val)}>{label}</option>
				{/each}
			</select>
		</div>

		<div class="field">
			<label for="tag-input">Tags</label>
			<div class="tags">
				{#each task.tags as tag}
					<span class="tag">
						{tag.name}
						<button onclick={() => removeTag(tag.id)}>✕</button>
					</span>
				{/each}
			</div>
			<form class="tag-form" onsubmit={addTag}>
				<input
					id="tag-input"
					bind:value={tagInput}
					placeholder="Add tag..."
					list="tag-suggestions"
				/>
				<datalist id="tag-suggestions">
					{#each availableTags as tag}
						<option value={tag.name}></option>
					{/each}
				</datalist>
				<button type="submit">+</button>
			</form>
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
				<MarkdownEditor
					value={notesValue}
					onSave={saveNotes}
				/>
			</div>
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

	.tag-form {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.25rem;
	}

	.tag-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.55rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.tag-form button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.empty-links {
		color: var(--text-tertiary);
		font-size: 0.82rem;
		font-style: italic;
		margin: 0;
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
</style>

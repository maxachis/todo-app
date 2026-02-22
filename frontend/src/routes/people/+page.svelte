<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Person, type Task, type List } from '$lib';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';

	let people: Person[] = $state([]);
	let selected: Person | null = $state(null);
	let linkedTaskIds = $state<number[]>([]);
	let allTasks = $state<{ id: number; title: string }[]>([]);

	let sortField: 'last_name' | 'first_name' | 'follow_up_cadence_days' = $state('last_name');
	let sortDirection: 'asc' | 'desc' = $state('asc');

	let sortedPeople: Person[] = $derived.by(() => {
		const dir = sortDirection === 'asc' ? 1 : -1;
		return [...people].sort((a, b) => {
			if (sortField === 'follow_up_cadence_days') {
				const aVal = a.follow_up_cadence_days;
				const bVal = b.follow_up_cadence_days;
				if (aVal == null && bVal == null) return 0;
				if (aVal == null) return 1;
				if (bVal == null) return -1;
				return (aVal - bVal) * dir;
			}
			const aStr = a[sortField] ?? '';
			const bStr = b[sortField] ?? '';
			return aStr.localeCompare(bStr) * dir;
		});
	});

	let newFirst = $state('');
	let newMiddle = $state('');
	let newLast = $state('');
	let newEmail = $state('');
	let newLinkedin = $state('');
	let newNotes = $state('');
	let newCadence = $state('');

	let editFirst = $state('');
	let editMiddle = $state('');
	let editLast = $state('');
	let editEmail = $state('');
	let editLinkedin = $state('');
	let editNotes = $state('');
	let editCadence = $state('');

	async function loadPeople(): Promise<void> {
		people = await api.people.getAll();
		if (selected) {
			selected = people.find((person) => person.id === selected?.id) ?? null;
		}
	}

	onMount(() => {
		loadPeople();
	});

	function selectPerson(person: Person): void {
		selected = person;
		editFirst = person.first_name;
		editMiddle = person.middle_name;
		editLast = person.last_name;
		editEmail = person.email;
		editLinkedin = person.linkedin_url;
		editNotes = person.notes;
		editCadence = person.follow_up_cadence_days?.toString() ?? '';
		loadLinkedTasks(person.id);
	}

	async function loadAllTasks(): Promise<void> {
		const lists: List[] = await api.lists.getAll();
		const flat: { id: number; title: string }[] = [];
		for (const list of lists) {
			for (const section of list.sections) {
				for (const task of section.tasks) {
					flat.push({ id: task.id, title: task.title });
				}
			}
		}
		allTasks = flat;
	}

	async function loadLinkedTasks(personId: number): Promise<void> {
		if (allTasks.length === 0) await loadAllTasks();
		const links = await api.taskLinks.people.listByPerson(personId);
		linkedTaskIds = links.map((l) => l.task_id);
	}

	async function addTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.people.add(taskId, selected.id);
		linkedTaskIds = [...linkedTaskIds, taskId];
	}

	async function removeTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.people.remove(taskId, selected.id);
		linkedTaskIds = linkedTaskIds.filter((id) => id !== taskId);
	}

	function taskName(t: { id: number }): string {
		return allTasks.find((x) => x.id === t.id)?.title ?? `Task #${t.id}`;
	}

	async function createPerson(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newFirst.trim() || !newLast.trim()) return;
		const person = await api.people.create({
			first_name: newFirst.trim(),
			last_name: newLast.trim(),
			middle_name: newMiddle.trim(),
			email: newEmail.trim(),
			linkedin_url: newLinkedin.trim(),
			notes: newNotes.trim(),
			follow_up_cadence_days: newCadence ? Number(newCadence) : null
		});
		people = [...people, person];
		newFirst = '';
		newMiddle = '';
		newLast = '';
		newEmail = '';
		newLinkedin = '';
		newNotes = '';
		newCadence = '';
	}

	async function savePerson(): Promise<void> {
		if (!selected) return;
		const updated = await api.people.update(selected.id, {
			first_name: editFirst.trim(),
			last_name: editLast.trim(),
			middle_name: editMiddle.trim(),
			email: editEmail.trim(),
			linkedin_url: editLinkedin.trim(),
			notes: editNotes,
			follow_up_cadence_days: editCadence ? Number(editCadence) : null
		});
		people = people.map((person) => (person.id === updated.id ? updated : person));
		selected = updated;
	}

	async function deletePerson(person: Person): Promise<void> {
		if (!confirm(`Delete ${person.first_name} ${person.last_name}?`)) return;
		await api.people.remove(person.id);
		people = people.filter((item) => item.id !== person.id);
		if (selected?.id === person.id) {
			selected = null;
		}
	}
</script>

<section class="network-page">
	<header>
		<h1>People</h1>
	</header>

	<div class="network-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createPerson}>
				<input bind:value={newFirst} placeholder="First name" />
				<input bind:value={newMiddle} placeholder="Middle name" />
				<input bind:value={newLast} placeholder="Last name" />
				<input bind:value={newEmail} type="email" placeholder="Email" />
				<input bind:value={newLinkedin} placeholder="LinkedIn URL" />
				<input bind:value={newCadence} placeholder="Follow-up cadence (days)" />
				<textarea bind:value={newNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Person</button>
			</form>

			<div class="sort-bar">
				<select bind:value={sortField}>
					<option value="last_name">Last Name</option>
					<option value="first_name">First Name</option>
					<option value="follow_up_cadence_days">Follow Up Days</option>
				</select>
				<button
					class="sort-direction"
					type="button"
					onclick={() => (sortDirection = sortDirection === 'asc' ? 'desc' : 'asc')}
					title={sortDirection === 'asc' ? 'Ascending' : 'Descending'}
				>
					{sortDirection === 'asc' ? '\u2191' : '\u2193'}
				</button>
			</div>

			<div class="list">
				{#each sortedPeople as person (person.id)}
					<button class="list-item" class:active={selected?.id === person.id} onclick={() => selectPerson(person)}>
						<div class="title">{person.last_name}, {person.first_name}</div>
						{#if person.follow_up_cadence_days}
							<div class="meta">Follow up: {person.follow_up_cadence_days} days</div>
						{/if}
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{selected.last_name}, {selected.first_name}</h2>
					<button class="danger" onclick={() => selected && deletePerson(selected)}>Delete</button>
				</div>
				{#if selected.email || selected.linkedin_url}
					<div class="contact-links">
						{#if selected.email}
							<a href="mailto:{selected.email}">{selected.email}</a>
						{/if}
						{#if selected.linkedin_url}
							<a href={selected.linkedin_url} target="_blank" rel="noopener noreferrer">LinkedIn</a>
						{/if}
					</div>
				{/if}
				<div class="detail-form">
					<label>
						<span>First name</span>
						<input bind:value={editFirst} />
					</label>
					<label>
						<span>Middle name</span>
						<input bind:value={editMiddle} />
					</label>
					<label>
						<span>Last name</span>
						<input bind:value={editLast} />
					</label>
					<label>
						<span>Email</span>
						<input bind:value={editEmail} type="email" />
					</label>
					<label>
						<span>LinkedIn URL</span>
						<input bind:value={editLinkedin} />
					</label>
					<label>
						<span>Follow-up cadence (days)</span>
						<input bind:value={editCadence} />
					</label>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes}></textarea>
					</label>
					<button class="primary" onclick={savePerson}>Save</button>
				</div>
				<div class="linked-tasks-section">
					<LinkedEntities
						label="Linked Tasks"
						entities={allTasks}
						linkedIds={linkedTaskIds}
						getDisplayName={taskName}
						onAdd={addTaskLink}
						onRemove={removeTaskLink}
					/>
				</div>
			{:else}
				<div class="empty-state">Select a person to view details.</div>
			{/if}
		</div>
	</div>
</section>

<style>
	.network-page {
		display: grid;
		gap: 1rem;
		height: 100%;
		min-height: 0;
		grid-template-rows: auto 1fr;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
	}

	.network-grid {
		display: grid;
		grid-template-columns: minmax(260px, 1fr) minmax(360px, 2fr);
		gap: 1rem;
		min-height: 0;
	}

	.panel {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.9rem;
		box-shadow: var(--shadow-sm);
		min-height: 0;
		overflow-y: auto;
	}

	.create-form {
		display: grid;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.create-form input,
	.create-form textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.create-form button,
	.detail-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		color: var(--text-primary);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		transition: all var(--transition);
	}

	.create-form button:hover,
	.detail-form button:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.sort-bar {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		margin-bottom: 0.5rem;
	}

	.sort-bar select {
		flex: 1;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.5rem;
		font-family: var(--font-body);
		font-size: 0.8rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.sort-direction {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-surface);
		color: var(--text-primary);
		padding: 0.3rem 0.5rem;
		cursor: pointer;
		font-size: 0.85rem;
		line-height: 1;
		transition: all var(--transition);
	}

	.sort-direction:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.list {
		display: grid;
		gap: 0.5rem;
	}

	.list-item {
		text-align: left;
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		padding: 0.5rem 0.6rem;
		background: var(--bg-surface);
		cursor: pointer;
		transition: background var(--transition), border-color var(--transition);
	}

	.list-item.active {
		background: var(--accent-light);
		border-color: var(--accent);
	}

	.title {
		font-weight: 600;
		color: var(--text-primary);
	}

	.meta {
		font-size: 0.75rem;
		color: var(--text-tertiary);
	}

	.detail-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.contact-links {
		display: flex;
		gap: 0.75rem;
		margin-bottom: 0.75rem;
		font-size: 0.85rem;
	}

	.contact-links a {
		color: var(--accent);
		text-decoration: none;
	}

	.contact-links a:hover {
		text-decoration: underline;
	}

	.detail-form {
		display: grid;
		gap: 0.5rem;
	}

	label {
		display: grid;
		gap: 0.25rem;
		font-size: 0.8rem;
		color: var(--text-secondary);
	}

	label input,
	label textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.detail-form .primary {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.danger {
		border: 1px solid var(--error-border);
		background: var(--error-bg);
		color: var(--error);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.6rem;
		cursor: pointer;
	}

	.linked-tasks-section {
		margin-top: 0.75rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--border-light);
	}

	.empty-state {
		color: var(--text-tertiary);
		font-size: 0.9rem;
	}

	@media (max-width: 1024px) {
		.network-grid {
			grid-template-columns: 1fr;
		}
	}
</style>

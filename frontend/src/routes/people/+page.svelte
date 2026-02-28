<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Person, type PersonTag, type Task, type List, type InteractionType } from '$lib';
	import { ApiError } from '$lib/api/client';
	import { addToast } from '$lib/stores/toast';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';

	let people: Person[] = $state([]);
	let selected: Person | null = $state(null);
	let linkedTaskIds = $state<number[]>([]);
	let allTasks = $state<{ id: number; title: string }[]>([]);
	let interactionTypes: InteractionType[] = $state([]);

	let sortField: 'last_name' | 'first_name' | 'follow_up_cadence_days' | 'follow_up_status' = $state('last_name');
	let sortDirection: 'asc' | 'desc' = $state('asc');
	let filterQuery = $state('');
	let tagFilter = $state('');
	let allPersonTags: PersonTag[] = $state([]);
	let availableTagsForPerson: PersonTag[] = $state([]);

	// Quick-log form state
	let quickLogTypeId = $state<number | null>(null);
	let quickLogDate = $state(todayStr());
	let quickLogNotes = $state('');

	type FollowUpTier = 'overdue' | 'due-soon' | 'on-track' | 'no-cadence';

	function todayStr(): string {
		const now = new Date();
		const y = now.getFullYear();
		const m = String(now.getMonth() + 1).padStart(2, '0');
		const d = String(now.getDate()).padStart(2, '0');
		return `${y}-${m}-${d}`;
	}

	function daysSince(dateStr: string | null): number | null {
		if (!dateStr) return null;
		const then = new Date(dateStr + 'T00:00:00');
		const now = new Date();
		now.setHours(0, 0, 0, 0);
		return Math.floor((now.getTime() - then.getTime()) / (1000 * 60 * 60 * 24));
	}

	function followUpTier(person: Person): FollowUpTier {
		const cadence = person.follow_up_cadence_days;
		if (cadence == null || cadence <= 0) return 'no-cadence';
		const days = daysSince(person.last_interaction_date);
		if (days == null) return 'overdue'; // has cadence, never contacted
		if (days > cadence) return 'overdue';
		if (days > cadence * 0.8) return 'due-soon';
		return 'on-track';
	}

	function followUpLabel(person: Person): string {
		const cadence = person.follow_up_cadence_days;
		if (cadence == null || cadence <= 0) return '';
		const days = daysSince(person.last_interaction_date);
		if (days == null) return `never / ${cadence}d`;
		return `${days}d / ${cadence}d`;
	}

	function overdueRatio(person: Person): number {
		const cadence = person.follow_up_cadence_days;
		if (cadence == null || cadence <= 0) return -1; // sort to bottom
		const days = daysSince(person.last_interaction_date);
		if (days == null) return Infinity; // never contacted, sort to top
		return days / cadence;
	}

	let filteredAndSortedPeople: Person[] = $derived.by(() => {
		const q = filterQuery.trim().toLowerCase();
		const filtered = q
			? people.filter(p =>
				p.first_name.toLowerCase().includes(q) ||
				p.last_name.toLowerCase().includes(q)
			)
			: people;
		const dir = sortDirection === 'asc' ? 1 : -1;
		return [...filtered].sort((a, b) => {
			if (sortField === 'follow_up_cadence_days') {
				const aVal = a.follow_up_cadence_days;
				const bVal = b.follow_up_cadence_days;
				if (aVal == null && bVal == null) return 0;
				if (aVal == null) return 1;
				if (bVal == null) return -1;
				return (aVal - bVal) * dir;
			}
			if (sortField === 'follow_up_status') {
				const aRatio = overdueRatio(a);
				const bRatio = overdueRatio(b);
				// No-cadence people always at bottom
				if (aRatio === -1 && bRatio === -1) return 0;
				if (aRatio === -1) return 1;
				if (bRatio === -1) return -1;
				// Default desc for status (most overdue first), flip for asc
				return (bRatio - aRatio) * dir;
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
	let newTagNames: string[] = $state([]);

	let editFirst = $state('');
	let editMiddle = $state('');
	let editLast = $state('');
	let editEmail = $state('');
	let editLinkedin = $state('');
	let editNotes = $state('');
	let editCadence = $state('');

	async function loadPeople(): Promise<void> {
		people = await api.people.getAll(tagFilter || undefined);
		if (selected) {
			selected = people.find((person) => person.id === selected?.id) ?? null;
		}
	}

	async function loadAllPersonTags(): Promise<void> {
		allPersonTags = await api.personTags.list();
	}

	async function loadAvailableTagsForPerson(personId: number): Promise<void> {
		availableTagsForPerson = await api.personTags.list(personId);
	}

	onMount(() => {
		loadPeople();
		loadAllPersonTags();
		api.interactionTypes.getAll().then((types) => (interactionTypes = types));
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
		quickLogTypeId = null;
		quickLogDate = todayStr();
		quickLogNotes = '';
		loadLinkedTasks(person.id);
		loadAvailableTagsForPerson(person.id);
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

	async function addTagToPerson(name: string): Promise<{ id: number; label: string }> {
		if (!selected) return { id: 0, label: name };
		const tags = await api.people.addTag(selected.id, name);
		selected = { ...selected, tags };
		people = people.map((p) => (p.id === selected!.id ? selected! : p));
		await loadAvailableTagsForPerson(selected.id);
		await loadAllPersonTags();
		const added = tags.find((t) => t.name === name);
		return { id: added?.id ?? 0, label: name };
	}

	async function removeTagFromPerson(tagId: number): Promise<void> {
		if (!selected) return;
		await api.people.removeTag(selected.id, tagId);
		selected = { ...selected, tags: selected.tags.filter((t) => t.id !== tagId) };
		people = people.map((p) => (p.id === selected!.id ? selected! : p));
		await loadAvailableTagsForPerson(selected.id);
	}

	async function setTagFilter(tag: string): Promise<void> {
		tagFilter = tag;
		await loadPeople();
	}

	function addNewTagName(name: string): { id: number; label: string } {
		const trimmed = name.trim();
		if (trimmed && !newTagNames.includes(trimmed)) {
			newTagNames = [...newTagNames, trimmed];
		}
		return { id: 0, label: trimmed };
	}

	function removeNewTagName(name: string): void {
		newTagNames = newTagNames.filter((t) => t !== name);
	}

	let newFormAvailableTags: { id: number; label: string }[] = $derived(
		allPersonTags
			.filter((t) => !newTagNames.includes(t.name))
			.map((t) => ({ id: t.id, label: t.name }))
	);

	async function createPerson(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newFirst.trim() || !newLast.trim()) return;
		try {
			const person = await api.people.create({
				first_name: newFirst.trim(),
				last_name: newLast.trim(),
				middle_name: newMiddle.trim(),
				email: newEmail.trim(),
				linkedin_url: newLinkedin.trim(),
				notes: newNotes.trim(),
				follow_up_cadence_days: newCadence ? Number(newCadence) : null
			});
			// Add tags to newly created person
			for (const tagName of newTagNames) {
				await api.people.addTag(person.id, tagName);
			}
			// Re-fetch the person to get tags included
			if (newTagNames.length > 0) {
				const refreshed = await api.people.get(person.id);
				people = [...people, refreshed];
			} else {
				people = [...people, person];
			}
			newFirst = '';
			newMiddle = '';
			newLast = '';
			newEmail = '';
			newLinkedin = '';
			newNotes = '';
			newCadence = '';
			newTagNames = [];
			await loadAllPersonTags();
		} catch (err) {
			if (err instanceof ApiError && err.status === 409) {
				const detail = (err.body as { detail?: string })?.detail ?? 'A person with that name already exists.';
				addToast({ message: detail, type: 'error' });
				return;
			}
			throw err;
		}
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

	async function quickLogInteraction(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!selected || !quickLogTypeId || !quickLogDate) return;
		await api.interactions.create({
			person_ids: [selected.id],
			interaction_type_id: quickLogTypeId,
			date: quickLogDate,
			notes: quickLogNotes
		});
		quickLogTypeId = null;
		quickLogDate = todayStr();
		quickLogNotes = '';
		await loadPeople();
	}

	function formatDate(dateStr: string): string {
		const d = new Date(dateStr + 'T00:00:00');
		return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
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
				<div class="tag-picker">
					{#if newTagNames.length > 0}
						<div class="tag-chips">
							{#each newTagNames as name}
								<span class="tag-chip">
									{name}
									<button type="button" class="tag-remove" onclick={() => removeNewTagName(name)}>&times;</button>
								</span>
							{/each}
						</div>
					{/if}
					<TypeaheadSelect
						options={newFormAvailableTags}
						placeholder="Add tags…"
						onSelect={(id) => {
							const tag = allPersonTags.find((t) => t.id === id);
							if (tag) addNewTagName(tag.name);
						}}
						onCreate={(name) => Promise.resolve(addNewTagName(name))}
					/>
				</div>
				<textarea bind:value={newNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Person</button>
			</form>

			<div class="sort-bar">
				<input class="filter-input" type="text" placeholder="Filter by name…" bind:value={filterQuery} />
				<select bind:value={sortField}>
					<option value="last_name">Last Name</option>
					<option value="first_name">First Name</option>
					<option value="follow_up_cadence_days">Follow Up Days</option>
					<option value="follow_up_status">Follow-up Status</option>
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

			{#if allPersonTags.length > 0}
				<div class="tag-filter-bar">
					<select onchange={(e) => setTagFilter((e.target as HTMLSelectElement).value)} value={tagFilter}>
						<option value="">All tags</option>
						{#each allPersonTags as tag (tag.id)}
							<option value={tag.name}>{tag.name}</option>
						{/each}
					</select>
					{#if tagFilter}
						<button class="clear-filter" type="button" onclick={() => setTagFilter('')}>Clear</button>
					{/if}
				</div>
			{/if}

			<div class="list">
				{#each filteredAndSortedPeople as person (person.id)}
					<button class="list-item" class:active={selected?.id === person.id} onclick={() => selectPerson(person)}>
						<div class="list-item-row">
							<div class="title">{person.last_name}, {person.first_name}</div>
							{#if followUpTier(person) !== 'no-cadence'}
								<span class="status-badge status-{followUpTier(person)}">
									{followUpLabel(person)}
								</span>
							{/if}
						</div>
						{#if person.tags.length > 0}
							<div class="list-item-tags">
								{#each person.tags as tag (tag.id)}
									<span class="tag-chip-small">{tag.name}</span>
								{/each}
							</div>
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

				{#if selected.follow_up_cadence_days}
					<div class="follow-up-summary">
						{#if selected.last_interaction_date}
							<span class="last-interaction">Last interaction: {formatDate(selected.last_interaction_date)}{selected.last_interaction_type ? ` \u2013 ${selected.last_interaction_type}` : ''}</span>
						{:else}
							<span class="last-interaction">No interactions recorded</span>
						{/if}
						{#if followUpTier(selected) === 'overdue'}
							<span class="overdue-warning">Overdue for follow-up</span>
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
					<div class="form-field">
						<span class="field-label">Tags</span>
						<div class="tag-picker">
							{#if selected.tags.length > 0}
								<div class="tag-chips">
									{#each selected.tags as tag (tag.id)}
										<span class="tag-chip">
											{tag.name}
											<button type="button" class="tag-remove" onclick={() => removeTagFromPerson(tag.id)}>&times;</button>
										</span>
									{/each}
								</div>
							{/if}
							<TypeaheadSelect
								options={availableTagsForPerson.map((t) => ({ id: t.id, label: t.name }))}
								placeholder="Add tag…"
								onSelect={(id) => {
									const tag = availableTagsForPerson.find((t) => t.id === id);
									if (tag) addTagToPerson(tag.name);
								}}
								onCreate={(name) => addTagToPerson(name)}
							/>
						</div>
					</div>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes}></textarea>
					</label>
					<button class="primary" onclick={savePerson}>Save</button>
				</div>

				<div class="quick-log-section">
					<h3>Quick Log Interaction</h3>
					<form class="quick-log-form" onsubmit={quickLogInteraction}>
						<TypeaheadSelect
							options={interactionTypes.map((t) => ({ id: t.id, label: t.name }))}
							placeholder="Interaction type"
							bind:value={quickLogTypeId}
						/>
						<input type="date" bind:value={quickLogDate} />
						<textarea bind:value={quickLogNotes} placeholder="Notes (optional)" rows="2"></textarea>
						<button type="submit">+ Log</button>
					</form>
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

	.filter-input {
		flex: 1;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.5rem;
		font-family: var(--font-body);
		font-size: 0.8rem;
		background: var(--bg-input);
		color: var(--text-primary);
		min-width: 0;
	}

	.sort-bar select {
		flex: none;
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

	.list-item-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
	}

	.title {
		font-weight: 600;
		color: var(--text-primary);
	}

	.status-badge {
		font-size: 0.7rem;
		font-weight: 600;
		padding: 0.15rem 0.4rem;
		border-radius: var(--radius-sm);
		white-space: nowrap;
		flex-shrink: 0;
	}

	.status-overdue {
		background: var(--error-bg);
		color: var(--error);
		border: 1px solid var(--error-border);
	}

	.status-due-soon {
		background: rgba(200, 155, 60, 0.1);
		color: #8a6914;
		border: 1px solid rgba(200, 155, 60, 0.3);
	}

	:global(:root[data-theme='dark']) .status-due-soon {
		color: #c9a84c;
	}

	.status-on-track {
		background: var(--success-bg);
		color: var(--success);
		border: 1px solid var(--success-border);
	}

	.tag-filter-bar {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		margin-bottom: 0.5rem;
	}

	.tag-filter-bar select {
		flex: 1;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.5rem;
		font-family: var(--font-body);
		font-size: 0.8rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.clear-filter {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-surface);
		color: var(--text-secondary);
		padding: 0.3rem 0.5rem;
		cursor: pointer;
		font-size: 0.8rem;
		transition: all var(--transition);
	}

	.clear-filter:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.list-item-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		margin-top: 0.25rem;
	}

	.tag-chip-small {
		font-size: 0.65rem;
		padding: 0.1rem 0.35rem;
		border-radius: var(--radius-sm);
		background: var(--accent-light);
		color: var(--accent);
		font-weight: 500;
	}

	.form-field {
		display: grid;
		gap: 0.25rem;
	}

	.field-label {
		font-size: 0.8rem;
		color: var(--text-secondary);
	}

	.tag-picker {
		display: grid;
		gap: 0.3rem;
	}

	.tag-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.3rem;
	}

	.tag-chip {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		font-size: 0.78rem;
		padding: 0.15rem 0.45rem;
		border-radius: var(--radius-sm);
		background: var(--accent-light);
		color: var(--accent);
		font-weight: 500;
	}

	.tag-remove {
		background: none;
		border: none;
		color: var(--accent);
		cursor: pointer;
		font-size: 0.85rem;
		line-height: 1;
		padding: 0;
		opacity: 0.6;
		transition: opacity var(--transition);
	}

	.tag-remove:hover {
		opacity: 1;
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

	.follow-up-summary {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
		padding: 0.5rem 0.65rem;
		border-radius: var(--radius-sm);
		background: var(--bg-surface-hover);
		font-size: 0.82rem;
	}

	.last-interaction {
		color: var(--text-secondary);
	}

	.overdue-warning {
		font-weight: 600;
		color: var(--error);
		font-size: 0.78rem;
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

	.quick-log-section {
		margin-top: 0.75rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--border-light);
	}

	.quick-log-section h3 {
		margin: 0 0 0.5rem;
		font-family: var(--font-display);
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.quick-log-form {
		display: grid;
		gap: 0.4rem;
	}

	.quick-log-form input,
	.quick-log-form textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.quick-log-form button {
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

	.quick-log-form button:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
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

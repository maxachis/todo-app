<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Lead, type Person, type Organization, type List } from '$lib';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';

	let leads: Lead[] = $state([]);
	let selected: Lead | null = $state(null);
	let linkedTaskIds = $state<number[]>([]);
	let allTasks = $state<{ id: number; title: string }[]>([]);
	let people: Person[] = $state([]);
	let organizations: Organization[] = $state([]);

	const statusOptions = [
		{ value: 'prospect', label: 'Prospect' },
		{ value: 'interested', label: 'Interested' },
		{ value: 'committed', label: 'Committed' },
		{ value: 'fulfilled', label: 'Fulfilled' },
		{ value: 'unfulfilled', label: 'Unfulfilled' }
	];

	// Create form state
	let newTitle = $state('');
	let newPersonId = $state<number | null>(null);
	let newOrgId = $state<number | null>(null);

	// Edit form state
	let editTitle = $state('');
	let editStatus = $state('prospect');
	let editNotes = $state('');
	let editPersonId = $state<number | null>(null);
	let editOrgId = $state<number | null>(null);

	async function loadLeads(): Promise<void> {
		leads = await api.leads.getAll();
		if (selected) {
			selected = leads.find((l) => l.id === selected?.id) ?? null;
		}
	}

	onMount(() => {
		loadLeads();
		api.people.getAll().then((p) => (people = p));
		api.organizations.getAll().then((o) => (organizations = o));
	});

	function selectLead(lead: Lead): void {
		selected = lead;
		editTitle = lead.title;
		editStatus = lead.status;
		editNotes = lead.notes;
		editPersonId = lead.person_id;
		editOrgId = lead.organization_id;
		loadLinkedTasks(lead.id);
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

	async function loadLinkedTasks(leadId: number): Promise<void> {
		if (allTasks.length === 0) await loadAllTasks();
		const links = await api.taskLinks.leads.listByLead(leadId);
		linkedTaskIds = links.map((l) => l.task_id);
	}

	async function addTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.leads.add(selected.id, taskId);
		linkedTaskIds = [...linkedTaskIds, taskId];
	}

	async function removeTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.leads.remove(selected.id, taskId);
		linkedTaskIds = linkedTaskIds.filter((id) => id !== taskId);
	}

	function taskName(t: { id: number }): string {
		return allTasks.find((x) => x.id === t.id)?.title ?? `Task #${t.id}`;
	}

	function contactLabel(lead: Lead): string {
		const parts: string[] = [];
		if (lead.person_name) parts.push(lead.person_name);
		if (lead.organization_name) parts.push(lead.organization_name);
		return parts.join(' · ');
	}

	async function createLead(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newTitle.trim()) return;
		if (!newPersonId && !newOrgId) return;
		const lead = await api.leads.create({
			title: newTitle.trim(),
			person_id: newPersonId,
			organization_id: newOrgId
		});
		leads = [lead, ...leads];
		newTitle = '';
		newPersonId = null;
		newOrgId = null;
	}

	async function selectPerson(personId: number): Promise<void> {
		editPersonId = personId;
		await saveLead();
	}

	async function selectOrganization(orgId: number): Promise<void> {
		editOrgId = orgId;
		await saveLead();
	}

	async function saveLead(): Promise<void> {
		if (!selected) return;
		const updated = await api.leads.update(selected.id, {
			title: editTitle.trim(),
			status: editStatus,
			notes: editNotes,
			person_id: editPersonId,
			organization_id: editOrgId
		});
		leads = leads.map((l) => (l.id === updated.id ? updated : l));
		selected = updated;
	}

	async function deleteLead(lead: Lead): Promise<void> {
		if (!confirm(`Delete "${lead.title}"?`)) return;
		await api.leads.remove(lead.id);
		leads = leads.filter((l) => l.id !== lead.id);
		if (selected?.id === lead.id) {
			selected = null;
		}
	}
</script>

<section class="network-page">
	<header>
		<h1>Leads</h1>
	</header>

	<div class="network-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createLead}>
				<input bind:value={newTitle} placeholder="Lead title" />
				<TypeaheadSelect
					options={people.map((p) => ({ id: p.id, label: `${p.first_name} ${p.last_name}` }))}
					placeholder="Person (optional)"
					bind:value={newPersonId}
				/>
				<TypeaheadSelect
					options={organizations.map((o) => ({ id: o.id, label: o.name }))}
					placeholder="Organization (optional)"
					bind:value={newOrgId}
				/>
				<button type="submit">+ Lead</button>
			</form>

			<div class="list">
				{#each leads as lead (lead.id)}
					<button class="list-item" class:active={selected?.id === lead.id} onclick={() => selectLead(lead)}>
						<div class="list-item-row">
							<div class="list-item-content">
								<div class="title">{lead.title}</div>
								{#if contactLabel(lead)}
									<div class="contact">{contactLabel(lead)}</div>
								{/if}
							</div>
							<span class="status-badge status-{lead.status}">{lead.status}</span>
						</div>
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{selected.title}</h2>
					<button class="danger" onclick={() => selected && deleteLead(selected)}>Delete</button>
				</div>

				<div class="detail-form">
					<label>
						<span>Title</span>
						<input bind:value={editTitle} onblur={saveLead} />
					</label>
					<label>
						<span>Status</span>
						<select bind:value={editStatus} onchange={saveLead}>
							{#each statusOptions as opt}
								<option value={opt.value}>{opt.label}</option>
							{/each}
						</select>
					</label>
					<div class="typeahead-field">
						<span class="field-label">Person</span>
						<TypeaheadSelect
							options={people.map((p) => ({ id: p.id, label: `${p.first_name} ${p.last_name}` }))}
							placeholder="Select person"
							onSelect={selectPerson}
						/>
					</div>
					<div class="typeahead-field">
						<span class="field-label">Organization</span>
						<TypeaheadSelect
							options={organizations.map((o) => ({ id: o.id, label: o.name }))}
							placeholder="Select organization"
							onSelect={selectOrganization}
						/>
					</div>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes} onblur={saveLead}></textarea>
					</label>
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
				<div class="empty-state">Select a lead to view details.</div>
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

	.create-form input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.create-form button {
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

	.create-form button:hover {
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
		width: 100%;
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

	.list-item-content {
		min-width: 0;
	}

	.title {
		font-weight: 600;
		color: var(--text-primary);
	}

	.contact {
		font-size: 0.78rem;
		color: var(--text-secondary);
		margin-top: 0.15rem;
	}

	.status-badge {
		font-size: 0.7rem;
		font-weight: 600;
		padding: 0.15rem 0.4rem;
		border-radius: var(--radius-sm);
		white-space: nowrap;
		flex-shrink: 0;
		text-transform: capitalize;
	}

	.status-prospect {
		background: rgba(100, 140, 200, 0.12);
		color: #4a6fa5;
		border: 1px solid rgba(100, 140, 200, 0.3);
	}

	.status-interested {
		background: rgba(200, 155, 60, 0.1);
		color: #8a6914;
		border: 1px solid rgba(200, 155, 60, 0.3);
	}

	:global(:root[data-theme='dark']) .status-interested {
		color: #c9a84c;
	}

	.status-committed {
		background: var(--success-bg);
		color: var(--success);
		border: 1px solid var(--success-border);
	}

	.status-fulfilled {
		background: var(--success-bg);
		color: var(--success);
		border: 1px solid var(--success-border);
	}

	.status-unfulfilled {
		background: var(--error-bg);
		color: var(--error);
		border: 1px solid var(--error-border);
	}

	:global(:root[data-theme='dark']) .status-prospect {
		color: #7da3d4;
	}

	.detail-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	h2 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.15rem;
		font-weight: 600;
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
	label textarea,
	label select {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.typeahead-field {
		display: grid;
		gap: 0.25rem;
	}

	.field-label {
		font-size: 0.8rem;
		color: var(--text-secondary);
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

<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Organization, type OrgType, type List } from '$lib';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';

	let organizations: Organization[] = $state([]);
	let orgTypes: OrgType[] = $state([]);
	let selected: Organization | null = $state(null);
	let linkedTaskIds = $state<number[]>([]);
	let allTasks = $state<{ id: number; title: string }[]>([]);

	let newOrgName = $state('');
	let newOrgNotes = $state('');
	let newOrgTypeId = $state<number | null>(null);

	let newTypeName = $state('');

	let editName = $state('');
	let editNotes = $state('');
	let editOrgTypeId = $state<number | null>(null);

	async function loadData(): Promise<void> {
		orgTypes = await api.orgTypes.getAll();
		organizations = await api.organizations.getAll();
		if (selected) {
			selected = organizations.find((org) => org.id === selected?.id) ?? null;
		}
	}

	onMount(() => {
		loadData();
	});

	function selectOrg(org: Organization): void {
		selected = org;
		editName = org.name;
		editNotes = org.notes;
		editOrgTypeId = org.org_type_id;
		loadLinkedTasks(org.id);
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

	async function loadLinkedTasks(orgId: number): Promise<void> {
		if (allTasks.length === 0) await loadAllTasks();
		const links = await api.taskLinks.organizations.listByOrg(orgId);
		linkedTaskIds = links.map((l) => l.task_id);
	}

	async function addTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.organizations.add(taskId, selected.id);
		linkedTaskIds = [...linkedTaskIds, taskId];
	}

	async function removeTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.organizations.remove(taskId, selected.id);
		linkedTaskIds = linkedTaskIds.filter((id) => id !== taskId);
	}

	function taskName(t: { id: number }): string {
		return allTasks.find((x) => x.id === t.id)?.title ?? `Task #${t.id}`;
	}

	async function createOrgType(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newTypeName.trim()) return;
		const created = await api.orgTypes.create({ name: newTypeName.trim() });
		orgTypes = [...orgTypes, created].sort((a, b) => a.name.localeCompare(b.name));
		newTypeName = '';
		if (!newOrgTypeId) {
			newOrgTypeId = created.id;
		}
	}

	async function createOrganization(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newOrgName.trim() || !newOrgTypeId) return;
		const created = await api.organizations.create({
			name: newOrgName.trim(),
			org_type_id: newOrgTypeId,
			notes: newOrgNotes.trim()
		});
		organizations = [...organizations, created].sort((a, b) => a.name.localeCompare(b.name));
		newOrgName = '';
		newOrgNotes = '';
	}

	async function saveOrganization(): Promise<void> {
		if (!selected || !editOrgTypeId) return;
		const updated = await api.organizations.update(selected.id, {
			name: editName.trim(),
			org_type_id: editOrgTypeId,
			notes: editNotes
		});
		organizations = organizations.map((org) => (org.id === updated.id ? updated : org));
		selected = updated;
	}

	async function deleteOrganization(org: Organization): Promise<void> {
		if (!confirm(`Delete ${org.name}?`)) return;
		await api.organizations.remove(org.id);
		organizations = organizations.filter((item) => item.id !== org.id);
		if (selected?.id === org.id) {
			selected = null;
		}
	}
</script>

<section class="network-page">
	<header>
		<h1>Organizations</h1>
	</header>

	<div class="network-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createOrgType}>
				<input bind:value={newTypeName} placeholder="New org type" />
				<button type="submit">+ Type</button>
			</form>

			<form class="create-form" onsubmit={createOrganization}>
				<input bind:value={newOrgName} placeholder="Organization name" />
				<select bind:value={newOrgTypeId}>
					<option value={null} disabled selected>Org type</option>
					{#each orgTypes as type (type.id)}
						<option value={type.id}>{type.name}</option>
					{/each}
				</select>
				<textarea bind:value={newOrgNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Organization</button>
			</form>

			<div class="list">
				{#each organizations as org (org.id)}
					<button class="list-item" class:active={selected?.id === org.id} onclick={() => selectOrg(org)}>
						<div class="title">{org.name}</div>
						<div class="meta">{orgTypes.find((type) => type.id === org.org_type_id)?.name ?? '—'}</div>
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{selected.name}</h2>
					<button class="danger" onclick={() => selected && deleteOrganization(selected)}>Delete</button>
				</div>
				<div class="detail-form">
					<label>
						<span>Name</span>
						<input bind:value={editName} />
					</label>
					<label>
						<span>Org type</span>
						<select bind:value={editOrgTypeId}>
							{#each orgTypes as type (type.id)}
								<option value={type.id}>{type.name}</option>
							{/each}
						</select>
					</label>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes}></textarea>
					</label>
					<button class="primary" onclick={saveOrganization}>Save</button>
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
				<div class="empty-state">Select an organization to view details.</div>
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
	.create-form select,
	.create-form textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
	}

	.create-form button,
	.detail-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
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

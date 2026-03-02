<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { api, type ContactDraft, type ContactDraftMatches, type OrgType } from '$lib';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';
	import { addToast } from '$lib/stores/toast';
	import { ApiError } from '$lib/api/client';

	const refreshInboxCount = getContext<() => Promise<void>>('refreshInboxCount');

	let drafts: ContactDraft[] = $state([]);
	let selected: ContactDraft | null = $state(null);
	let matches: ContactDraftMatches | null = $state(null);
	let orgTypes: OrgType[] = $state([]);

	// Triage mode: null, 'person', or 'org'
	let promoteMode: 'person' | 'org' | null = $state(null);

	// Person form state
	let personFirst = $state('');
	let personLast = $state('');
	let personMiddle = $state('');
	let personEmail = $state('');
	let personLinkedin = $state('');
	let personNotes = $state('');
	let personCadence = $state<number | null>(null);

	// Org form state
	let orgName = $state('');
	let orgTypeId = $state<number | null>(null);
	let orgNotes = $state('');

	async function loadDrafts(): Promise<void> {
		drafts = await api.contactDrafts.list();
	}

	onMount(async () => {
		await loadDrafts();
		const types = await api.orgTypes.getAll();
		orgTypes = types;
	});

	function selectDraft(draft: ContactDraft): void {
		selected = draft;
		matches = null;
		promoteMode = null;
		api.contactDrafts.matches(draft.id).then((m) => (matches = m));
	}

	function selectNext(): void {
		const remaining = drafts.filter((d) => d.id !== selected?.id);
		if (remaining.length > 0) {
			selectDraft(remaining[0]);
		} else {
			selected = null;
			matches = null;
		}
	}

	function removeDraft(id: number): void {
		drafts = drafts.filter((d) => d.id !== id);
		refreshInboxCount();
	}

	async function handleDismiss(): Promise<void> {
		if (!selected) return;
		await api.contactDrafts.dismiss(selected.id);
		const dismissedId = selected.id;
		selectNext();
		removeDraft(dismissedId);
	}

	async function handleLink(type: 'person' | 'org', id: number): Promise<void> {
		if (!selected) return;
		const draftId = selected.id;
		if (type === 'person') {
			await api.contactDrafts.link(draftId, { person_id: id });
		} else {
			await api.contactDrafts.link(draftId, { org_id: id });
		}
		selectNext();
		removeDraft(draftId);
	}

	function startPromotePerson(): void {
		if (!selected) return;
		promoteMode = 'person';
		const tokens = selected.name.split(/\s+/);
		personFirst = tokens[0] || '';
		personLast = tokens.length > 1 ? tokens.slice(1).join(' ') : '';
		personMiddle = '';
		personEmail = '';
		personLinkedin = '';
		personNotes = selected.quick_notes;
		personCadence = null;
	}

	function startPromoteOrg(): void {
		if (!selected) return;
		promoteMode = 'org';
		orgName = selected.name;
		orgTypeId = null;
		orgNotes = selected.quick_notes;
	}

	function cancelPromote(): void {
		promoteMode = null;
	}

	async function submitPerson(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!selected) return;
		if (!personFirst.trim() || !personLast.trim()) {
			addToast({ message: 'First and last name are required.', type: 'error' });
			return;
		}
		try {
			await api.contactDrafts.promoteToPerson(selected.id, {
				first_name: personFirst.trim(),
				last_name: personLast.trim(),
				middle_name: personMiddle.trim(),
				email: personEmail.trim(),
				linkedin_url: personLinkedin.trim(),
				notes: personNotes || null,
				follow_up_cadence_days: personCadence
			});
			const draftId = selected.id;
			promoteMode = null;
			selectNext();
			removeDraft(draftId);
		} catch (err) {
			if (err instanceof ApiError && err.status === 409) {
				addToast({ message: String(err.body), type: 'error' });
			} else {
				throw err;
			}
		}
	}

	async function submitOrg(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!selected) return;
		if (!orgName.trim()) {
			addToast({ message: 'Name is required.', type: 'error' });
			return;
		}
		if (!orgTypeId) {
			addToast({ message: 'Org type is required.', type: 'error' });
			return;
		}
		try {
			await api.contactDrafts.promoteToOrg(selected.id, {
				name: orgName.trim(),
				org_type_id: orgTypeId,
				notes: orgNotes || null
			});
			const draftId = selected.id;
			promoteMode = null;
			selectNext();
			removeDraft(draftId);
		} catch (err) {
			if (err instanceof ApiError && err.status === 409) {
				addToast({ message: String(err.body), type: 'error' });
			} else {
				throw err;
			}
		}
	}

	async function createOrgType(name: string): Promise<{ id: number; label: string }> {
		const created = await api.orgTypes.create({ name });
		orgTypes = [...orgTypes, created];
		return { id: created.id, label: created.name };
	}

	function checkHasMatches(m: ContactDraftMatches | null): boolean {
		if (!m) return false;
		return m.people.length > 0 || m.organizations.length > 0;
	}

	const hasMatches = $derived(checkHasMatches(matches));
</script>

<section class="crm-page">
	<header>
		<h1>Contacts Inbox</h1>
	</header>

	<div class="crm-grid">
		<div class="panel list-panel">
			<div class="list">
				{#each drafts as draft (draft.id)}
					<button class="list-item" class:active={selected?.id === draft.id} onclick={() => selectDraft(draft)}>
						<div class="title">{draft.name}</div>
						{#if draft.quick_notes}
							<div class="quick-notes-preview">{draft.quick_notes.length > 60 ? draft.quick_notes.slice(0, 60) + '...' : draft.quick_notes}</div>
						{/if}
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{selected.name}</h2>
				</div>

				{#if selected.quick_notes}
					<p class="quick-notes">{selected.quick_notes}</p>
				{/if}

				{#if selected.source_page_slug}
					<p class="source-page">
						From: <a href="/notebook/{selected.source_page_slug}">{selected.source_page_title || selected.source_page_slug}</a>
					</p>
				{/if}

				{#if matches && hasMatches && promoteMode === null}
					<div class="matches-section">
						<h3>Possible matches</h3>
						{#each matches.people as person}
							<button class="match-btn" onclick={() => handleLink('person', person.id)}>
								→ Link to {person.first_name} {person.last_name}
							</button>
						{/each}
						{#each matches.organizations as org}
							<button class="match-btn" onclick={() => handleLink('org', org.id)}>
								→ Link to {org.name}
							</button>
						{/each}
					</div>
				{/if}

				{#if promoteMode === null}
					<div class="actions">
						<button class="action-btn person-btn" onclick={startPromotePerson}>→ Person</button>
						<button class="action-btn org-btn" onclick={startPromoteOrg}>→ Org</button>
						<button class="action-btn dismiss-btn" onclick={handleDismiss}>Dismiss</button>
					</div>
				{:else if promoteMode === 'person'}
					<form class="promote-form" onsubmit={submitPerson}>
						<h3>Promote to Person</h3>
						<label>
							<span>First name *</span>
							<input bind:value={personFirst} required />
						</label>
						<label>
							<span>Last name *</span>
							<input bind:value={personLast} required />
						</label>
						<label>
							<span>Middle name</span>
							<input bind:value={personMiddle} />
						</label>
						<label>
							<span>Email</span>
							<input type="email" bind:value={personEmail} />
						</label>
						<label>
							<span>LinkedIn URL</span>
							<input bind:value={personLinkedin} />
						</label>
						<label>
							<span>Follow-up cadence (days)</span>
							<input type="number" bind:value={personCadence} min="1" />
						</label>
						<label>
							<span>Notes</span>
							<textarea rows="3" bind:value={personNotes}></textarea>
						</label>
						<div class="form-actions">
							<button type="button" onclick={cancelPromote}>Cancel</button>
							<button type="submit" class="primary">Create Person</button>
						</div>
					</form>
				{:else if promoteMode === 'org'}
					<form class="promote-form" onsubmit={submitOrg}>
						<h3>Promote to Organization</h3>
						<label>
							<span>Name *</span>
							<input bind:value={orgName} required />
						</label>
						<div class="typeahead-field">
							<span class="field-label">Org Type *</span>
							<TypeaheadSelect
								options={orgTypes.map((t) => ({ id: t.id, label: t.name }))}
								placeholder="Select or create org type"
								bind:value={orgTypeId}
								onCreate={createOrgType}
							/>
						</div>
						<label>
							<span>Notes</span>
							<textarea rows="3" bind:value={orgNotes}></textarea>
						</label>
						<div class="form-actions">
							<button type="button" onclick={cancelPromote}>Cancel</button>
							<button type="submit" class="primary">Create Organization</button>
						</div>
					</form>
				{/if}
			{:else}
				<div class="empty-state">
					{#if drafts.length === 0}
						No contacts to triage. Use <code>@new[Name]</code> in notebook pages to capture contacts.
					{:else}
						Select a contact draft to triage.
					{/if}
				</div>
			{/if}
		</div>
	</div>
</section>

<style>
	.quick-notes-preview {
		font-size: 0.78rem;
		color: var(--text-secondary);
		margin-top: 0.15rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.quick-notes {
		margin: 0 0 0.75rem;
		color: var(--text-secondary);
		font-size: 0.9rem;
		line-height: 1.5;
		white-space: pre-wrap;
	}

	.source-page {
		margin: 0 0 1rem;
		font-size: 0.8rem;
		color: var(--text-tertiary);
	}

	.source-page a {
		color: var(--accent);
		text-decoration: none;
	}

	.source-page a:hover {
		text-decoration: underline;
	}

	.matches-section {
		margin-bottom: 1rem;
		padding: 0.5rem 0;
	}

	.matches-section h3 {
		margin: 0 0 0.5rem;
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--text-secondary);
	}

	.match-btn {
		display: block;
		width: 100%;
		text-align: left;
		padding: 0.35rem 0.5rem;
		margin-bottom: 0.25rem;
		font-size: 0.85rem;
		background: var(--bg-surface-hover);
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		cursor: pointer;
		color: var(--accent);
		font-family: var(--font-body);
		transition: background var(--transition);
	}

	.match-btn:hover {
		background: var(--accent-light);
	}

	.actions {
		display: flex;
		gap: 0.5rem;
		margin-top: 1rem;
	}

	.action-btn {
		padding: 0.4rem 0.8rem;
		font-size: 0.85rem;
		font-family: var(--font-body);
		border-radius: var(--radius-sm);
		border: 1px solid var(--border-light);
		cursor: pointer;
		transition: all var(--transition);
	}

	.person-btn {
		background: var(--accent-light);
		color: var(--accent);
		border-color: var(--accent);
	}

	.person-btn:hover {
		background: var(--accent);
		color: white;
	}

	.org-btn {
		background: var(--bg-surface);
		color: var(--text-primary);
	}

	.org-btn:hover {
		background: var(--bg-surface-hover);
	}

	.dismiss-btn {
		background: transparent;
		color: var(--text-tertiary);
		border-color: transparent;
		margin-left: auto;
	}

	.dismiss-btn:hover {
		color: var(--error);
		background: var(--error-bg);
	}

	.promote-form {
		margin-top: 1rem;
		display: grid;
		gap: 0.5rem;
	}

	.promote-form h3 {
		margin: 0 0 0.25rem;
		font-size: 0.9rem;
		font-weight: 600;
	}

	.promote-form label {
		display: grid;
		gap: 0.15rem;
	}

	.promote-form label span {
		font-size: 0.78rem;
		color: var(--text-secondary);
	}

	.promote-form input,
	.promote-form textarea {
		padding: 0.4rem;
		font-size: 0.85rem;
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		background: var(--bg-input);
		color: var(--text-primary);
		font-family: var(--font-body);
	}

	.form-actions {
		display: flex;
		gap: 0.5rem;
		justify-content: flex-end;
		margin-top: 0.25rem;
	}

	.form-actions button {
		padding: 0.35rem 0.75rem;
		font-size: 0.85rem;
		border-radius: var(--radius-sm);
		border: 1px solid var(--border-light);
		cursor: pointer;
		font-family: var(--font-body);
		background: var(--bg-surface);
		color: var(--text-primary);
		transition: all var(--transition);
	}

	.form-actions button:hover {
		background: var(--bg-surface-hover);
	}

	.form-actions .primary {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.form-actions .primary:hover {
		opacity: 0.9;
	}

	.typeahead-field {
		display: grid;
		gap: 0.15rem;
	}

	.empty-state code {
		background: var(--bg-surface-hover);
		padding: 0.1rem 0.3rem;
		border-radius: var(--radius-sm);
		font-size: 0.85rem;
	}
</style>

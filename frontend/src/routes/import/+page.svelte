<script lang="ts">
	import type { ImportSummary } from '$lib';
	import { api } from '$lib';

	let file = $state<File | null>(null);
	let loading = $state(false);
	let summary = $state<ImportSummary | null>(null);
	let error = $state<string | null>(null);

	async function handleSubmit(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!file) return;

		loading = true;
		error = null;
		summary = null;

		try {
			summary = await api.import.upload(file);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Import failed';
		} finally {
			loading = false;
		}
	}

	function handleFileChange(event: Event): void {
		const input = event.target as HTMLInputElement;
		file = input.files?.[0] ?? null;
		summary = null;
		error = null;
	}
</script>

<section class="import-page">
	<header>
		<h1>Import</h1>
		<p>Import tasks from a file. Supported formats: app JSON export, app CSV export, or TickTick CSV.</p>
	</header>

	<form class="import-form" onsubmit={handleSubmit}>
		<input type="file" accept=".csv,.json" onchange={handleFileChange} />
		<button type="submit" disabled={!file || loading}>
			{loading ? 'Importing...' : 'Import'}
		</button>
	</form>

	{#if error}
		<div class="error-box">{error}</div>
	{/if}

	{#if summary}
		<div class="summary-box">
			<h3>Import Complete</h3>
			<ul>
				<li>Tasks created: {summary.tasks_created}</li>
				<li>Tasks skipped (duplicates): {summary.tasks_skipped}</li>
				<li>Lists created: {summary.lists_created}</li>
				<li>Sections created: {summary.sections_created}</li>
				<li>Tags created: {summary.tags_created}</li>
				<li>Parent links resolved: {summary.parents_linked}</li>
				{#if summary.errors > 0}
					<li class="errors">Errors: {summary.errors}</li>
				{/if}
			</ul>
			{#if summary.error_details.length > 0}
				<div class="error-details">
					{#each summary.error_details as detail}
						<p>{detail}</p>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</section>

<style>
	.import-page {
		display: grid;
		gap: 1rem;
		max-width: 600px;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	p {
		margin: 0.25rem 0 0;
		color: var(--text-secondary);
	}

	.import-form {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	.import-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.import-form button:hover:not(:disabled) {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.import-form button:disabled {
		opacity: 0.45;
		cursor: not-allowed;
	}

	.error-box {
		background: var(--error-bg);
		border: 1px solid var(--error-border);
		border-radius: var(--radius-md);
		padding: 0.65rem 0.85rem;
		color: var(--error);
		font-size: 0.88rem;
	}

	.summary-box {
		background: var(--success-bg);
		border: 1px solid var(--success-border);
		border-radius: var(--radius-md);
		padding: 0.85rem 1.1rem;
	}

	.summary-box h3 {
		margin: 0 0 0.5rem;
		font-family: var(--font-display);
		font-size: 1.05rem;
		font-weight: 600;
		color: var(--success);
	}

	.summary-box ul {
		margin: 0;
		padding-left: 1.25rem;
		font-size: 0.85rem;
		color: var(--text-primary);
	}

	.summary-box li {
		margin-bottom: 0.2rem;
	}

	.errors {
		color: var(--error);
		font-weight: 600;
	}

	.error-details {
		margin-top: 0.5rem;
		font-size: 0.8rem;
		color: var(--error);
	}

	.error-details p {
		margin: 0.15rem 0;
		color: var(--error);
	}
</style>

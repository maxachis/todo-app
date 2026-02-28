<script lang="ts">
	import { untrack } from 'svelte';
	import { flip } from 'svelte/animate';
	import { dragHandleZone } from 'svelte-dnd-action';
	import type { Section } from '$lib';
	import SectionHeader from './SectionHeader.svelte';
	import TaskList from '../tasks/TaskList.svelte';
	import TaskCreateForm from '../tasks/TaskCreateForm.svelte';
	import TaskRow from '../tasks/TaskRow.svelte';
	import { addToast } from '$lib/stores/toast';
	import { moveSectionWithOptions, refreshSelectedListDetail } from '$lib/stores/lists';

	const FLIP_DURATION = 150;

	let {
		sections,
		allCollapsed = false,
		onCreateSection = () => {},
		onUpdateSection = (_id: number, _changes: { name?: string; emoji?: string }) => {},
		onDeleteSection = (_id: number) => {},
		onMoveSection = (_id: number, _pos: number) => {}
	}: {
		sections: Section[];
		allCollapsed?: boolean;
		onCreateSection?: () => void;
		onUpdateSection?: (id: number, changes: { name?: string; emoji?: string }) => void;
		onDeleteSection?: (id: number) => void;
		onMoveSection?: (id: number, pos: number) => void;
	} = $props();

	let collapsedIds = $state<Set<number>>(new Set());
	let showCompletedIds = $state<Set<number>>(new Set());
	let sortableSections = $state<Section[]>([]);
	let editingSectionId = $state<number | null>(null);

	$effect(() => {
		if (allCollapsed) {
			collapsedIds = new Set(untrack(() => sections).map((s) => s.id));
		} else {
			collapsedIds = new Set();
		}
	});

	$effect(() => {
		const deduped = [...sections]
			.sort((a, b) => a.position - b.position)
			.filter((section, index, arr) => arr.findIndex((s) => s.id === section.id) === index);
		sortableSections = deduped;
	});

	function toggleCollapse(sectionId: number): void {
		const next = new Set(collapsedIds);
		if (next.has(sectionId)) {
			next.delete(sectionId);
		} else {
			next.add(sectionId);
		}
		collapsedIds = next;
	}

	function toggleShowCompleted(sectionId: number): void {
		const next = new Set(showCompletedIds);
		if (next.has(sectionId)) {
			next.delete(sectionId);
		} else {
			next.add(sectionId);
		}
		showCompletedIds = next;
	}

	function getCompletedTasks(section: Section) {
		return section.tasks
			.filter((t) => t.is_completed && t.parent_id === null)
			.sort((a, b) => a.position - b.position);
	}

	function handleStartEdit(sectionId: number): void {
		editingSectionId = sectionId;
	}

	function handleStopEdit(sectionId: number): void {
		if (editingSectionId === sectionId) {
			editingSectionId = null;
		}
	}

	function handleSectionConsider(event: CustomEvent<{ items: Section[] }>): void {
		sortableSections = event.detail.items as Section[];
	}

	async function handleSectionFinalize(event: CustomEvent<{ items: Section[] }>): Promise<void> {
		const previous = [...sections];
		const items = event.detail.items as Section[];
		sortableSections = items.filter((section, index, arr) => arr.findIndex((s) => s.id === section.id) === index);
		try {
			for (let i = 0; i < sortableSections.length; i += 1) {
				await moveSectionWithOptions(sortableSections[i].id, i, { refresh: false });
			}
			await refreshSelectedListDetail();
		} catch {
			sortableSections = previous;
			addToast({ message: 'Section reorder failed. Changes reverted.', type: 'error' });
		}
	}
</script>

<div class="section-list">
	<div
		class="sections-dnd"
		use:dragHandleZone={{ items: sortableSections, type: 'section-dnd', flipDurationMs: FLIP_DURATION, useCursorForDetection: true }}
		onconsider={handleSectionConsider}
		onfinalize={handleSectionFinalize}
	>
		{#each sortableSections as section (section.id)}
			<div class="section-block" animate:flip={{ duration: FLIP_DURATION }}>
				<SectionHeader
					{section}
					collapsed={collapsedIds.has(section.id)}
					{editingSectionId}
					onStartEdit={handleStartEdit}
					onStopEdit={handleStopEdit}
					onToggleCollapse={() => toggleCollapse(section.id)}
					onUpdate={(changes) => onUpdateSection(section.id, changes)}
					onDelete={() => onDeleteSection(section.id)}
				/>
				{#if !collapsedIds.has(section.id)}
					<TaskList tasks={section.tasks} sectionId={section.id} />
					<TaskCreateForm sectionId={section.id} />
					{@const completedTasks = getCompletedTasks(section)}
					{#if completedTasks.length > 0}
						<div class="completed-section">
							<button class="completed-toggle" onclick={() => toggleShowCompleted(section.id)}>
								<span class="chevron">{showCompletedIds.has(section.id) ? '▼' : '▶'}</span>
								Completed ({completedTasks.length})
							</button>
							{#if showCompletedIds.has(section.id)}
								{#each completedTasks as task (task.id)}
									<TaskRow {task} />
								{/each}
							{/if}
						</div>
					{/if}
				{/if}
			</div>
		{/each}
	</div>
</div>

<style>
	.section-list {
		display: grid;
		gap: 1.25rem;
	}

	.completed-section {
		margin-top: 0.5rem;
		border-top: 1px solid var(--border-light);
		padding-top: 0.4rem;
	}

	.section-block {
		display: grid;
	}

	.completed-toggle {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--text-tertiary);
		font-size: 0.78rem;
		font-weight: 600;
		font-family: var(--font-body);
		padding: 0.25rem 0;
		margin: 0;
		display: flex;
		align-items: center;
		gap: 0.3rem;
		transition: color var(--transition);
	}

	.completed-toggle:hover {
		color: var(--text-secondary);
	}

	.chevron {
		font-size: 0.6rem;
	}
</style>

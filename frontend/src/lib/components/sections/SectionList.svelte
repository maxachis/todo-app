<script lang="ts">
	import type { Section } from '$lib';
	import SectionHeader from './SectionHeader.svelte';
	import TaskList from '../tasks/TaskList.svelte';
	import TaskCreateForm from '../tasks/TaskCreateForm.svelte';
	import DragContainer from '../dnd/DragContainer.svelte';
	import DragItem from '../dnd/DragItem.svelte';
	import { addToast } from '$lib/stores/toast';
	import { moveSectionWithOptions, refreshSelectedListDetail } from '$lib/stores/lists';

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
	let sortableSections = $state<Section[]>([]);
	let editingSectionId = $state<number | null>(null);

	$effect(() => {
		if (allCollapsed) {
			collapsedIds = new Set(sections.map((s) => s.id));
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

	function handleStartEdit(sectionId: number): void {
		editingSectionId = sectionId;
	}

	function handleStopEdit(sectionId: number): void {
		if (editingSectionId === sectionId) {
			editingSectionId = null;
		}
	}

	function handleSectionConsider(event: CustomEvent<{ items: Section[] }>): void {
		const items = event.detail.items as Section[];
		sortableSections = items.filter((section, index, arr) => arr.findIndex((s) => s.id === section.id) === index);
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
	<DragContainer
		items={sortableSections}
		type="section-dnd"
		className="sections-dnd"
		useDragHandleZone={true}
		onConsider={handleSectionConsider}
		onFinalize={handleSectionFinalize}
	>
		{#each sortableSections as section (section.id)}
			<DragItem id={section.id} className="section-block">
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
				{/if}
			</DragItem>
		{/each}
	</DragContainer>
</div>

<style>
	.section-list {
		display: grid;
		gap: 1.25rem;
	}
</style>

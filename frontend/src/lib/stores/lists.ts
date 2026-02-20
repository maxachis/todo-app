import { derived, get, writable } from 'svelte/store';

import {
  api,
  type CreateListInput,
  type CreateSectionInput,
  type List,
  type Section,
  type Task,
  type UpdateListInput,
  type UpdateSectionInput
} from '$lib';

export const listsStore = writable<List[]>([]);
export const selectedListStore = writable<number | null>(null);

export const selectedListDetail = derived(
  [listsStore, selectedListStore],
  ([$lists, $selectedId]) => $lists.find((l) => l.id === $selectedId) ?? null
);

export async function loadLists(): Promise<void> {
  const lists = await api.lists.getAll();
  listsStore.set(lists);
  let resolvedSelectedId: number | null = null;
  selectedListStore.update((current) => {
    resolvedSelectedId = current ?? lists[0]?.id ?? null;
    return resolvedSelectedId;
  });
  if (resolvedSelectedId !== null) {
    await loadListDetail(resolvedSelectedId);
  }
}

export async function loadListDetail(listId: number): Promise<List> {
  const detail = await api.lists.get(listId);
  listsStore.update((lists) =>
    lists.map((list) => (list.id === listId ? detail : list))
  );
  return detail;
}

export async function selectList(listId: number | null): Promise<void> {
  selectedListStore.set(listId);
  if (listId !== null) {
    await loadListDetail(listId);
  }
}

export async function createList(payload: CreateListInput): Promise<List> {
  const created = await api.lists.create(payload);
  listsStore.update((lists) => [...lists, created].sort((a, b) => a.position - b.position));
  selectedListStore.set(created.id);
  return created;
}

export async function updateList(listId: number, payload: UpdateListInput): Promise<List> {
  const updated = await api.lists.update(listId, payload);
  listsStore.update((lists) =>
    lists.map((list) => {
      if (list.id !== listId) return list;
      return {
        ...updated,
        sections: list.sections
      };
    })
  );
  return updated;
}

export async function deleteList(listId: number): Promise<void> {
  await api.lists.remove(listId);
  listsStore.update((lists) => lists.filter((list) => list.id !== listId));
  selectedListStore.update((selected) => (selected === listId ? null : selected));
}

export async function moveList(listId: number, position: number): Promise<List> {
  const updated = await api.lists.move(listId, { position });
  await loadLists();
  return updated;
}

// --- Section CRUD ---

function updateListSections(listId: number, fn: (sections: Section[]) => Section[]): void {
  listsStore.update((lists) =>
    lists.map((list) =>
      list.id === listId ? { ...list, sections: fn(list.sections) } : list
    )
  );
}

export async function createSection(listId: number, payload: CreateSectionInput): Promise<Section> {
  const created = await api.sections.create(listId, payload);
  updateListSections(listId, (sections) =>
    [...sections, created].sort((a, b) => a.position - b.position)
  );
  return created;
}

export async function updateSection(sectionId: number, payload: UpdateSectionInput): Promise<Section> {
  const updated = await api.sections.update(sectionId, payload);
  const listId = updated.list_id;
  updateListSections(listId, (sections) =>
    sections.map((s) => (s.id === sectionId ? { ...updated, tasks: s.tasks } : s))
  );
  return updated;
}

export async function deleteSection(sectionId: number): Promise<void> {
  const selectedId = get(selectedListStore);
  await api.sections.remove(sectionId);
  if (selectedId !== null) {
    updateListSections(selectedId, (sections) => sections.filter((s) => s.id !== sectionId));
  }
}

export async function moveSection(sectionId: number, position: number): Promise<void> {
  await moveSectionWithOptions(sectionId, position, { refresh: true });
}

export async function moveSectionWithOptions(
  sectionId: number,
  position: number,
  options: { refresh?: boolean } = {}
): Promise<void> {
  const selectedId = get(selectedListStore);
  await api.sections.move(sectionId, { position });
  const refresh = options.refresh ?? true;
  if (refresh && selectedId !== null) {
    await loadListDetail(selectedId);
  }
}

export async function refreshSelectedListDetail(): Promise<void> {
  const selectedId = get(selectedListStore);
  if (selectedId !== null) {
    await loadListDetail(selectedId);
  }
}

// --- Task helpers (update tasks within sections) ---

function replaceTaskInTree(tasks: Task[], updated: Task): Task[] {
  return tasks.map((task) => {
    if (task.id === updated.id) return updated;
    return { ...task, subtasks: replaceTaskInTree(task.subtasks, updated) };
  });
}

function removeTaskFromTree(tasks: Task[], taskId: number): Task[] {
  return tasks
    .filter((t) => t.id !== taskId)
    .map((t) => ({ ...t, subtasks: removeTaskFromTree(t.subtasks, taskId) }));
}

function updateSectionTasks(listId: number, sectionId: number, fn: (tasks: Task[]) => Task[]): void {
  updateListSections(listId, (sections) =>
    sections.map((s) => (s.id === sectionId ? { ...s, tasks: fn(s.tasks) } : s))
  );
}

export function replaceTaskInList(listId: number, sectionId: number, updated: Task): void {
  updateSectionTasks(listId, sectionId, (tasks) => replaceTaskInTree(tasks, updated));
}

export function removeTaskFromList(listId: number, sectionId: number, taskId: number): void {
  updateSectionTasks(listId, sectionId, (tasks) => removeTaskFromTree(tasks, taskId));
}

export function addTaskToSection(listId: number, sectionId: number, task: Task): void {
  updateSectionTasks(listId, sectionId, (tasks) => [...tasks, task]);
}

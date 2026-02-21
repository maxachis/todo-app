import { get, writable } from 'svelte/store';

import { api, type CreateTaskInput, type MoveTaskInput, type Task, type UpdateTaskInput } from '$lib';
import { loadListDetail, replaceTaskInList, removeTaskFromList, addTaskToSection, selectedListStore } from './lists';
import { addToast } from './toast';

export const selectedTaskStore = writable<number | null>(null);
export const selectedTaskDetail = writable<Task | null>(null);
export const taskDragLockedStore = writable(false);

export function setTaskDragLocked(locked: boolean): void {
  taskDragLockedStore.set(locked);
}

export async function selectTask(taskId: number | null): Promise<void> {
  selectedTaskStore.set(taskId);
  if (taskId !== null) {
    const task = await api.tasks.get(taskId);
    selectedTaskDetail.set(task);
  } else {
    selectedTaskDetail.set(null);
  }
}

export async function createTask(sectionId: number, payload: CreateTaskInput): Promise<Task> {
  const created = await api.tasks.create(sectionId, payload);
  const listId = get(selectedListStore);
  if (listId !== null) {
    addTaskToSection(listId, sectionId, created);
  }
  return created;
}

export async function updateTask(taskId: number, payload: UpdateTaskInput): Promise<Task> {
  const updated = await api.tasks.update(taskId, payload);
  const listId = get(selectedListStore);
  if (listId !== null) {
    replaceTaskInList(listId, updated.section_id, updated);
  }
  selectedTaskDetail.update((current) => (current?.id === taskId ? updated : current));
  return updated;
}

export async function deleteTask(taskId: number): Promise<void> {
  const detail = get(selectedTaskDetail);
  await api.tasks.remove(taskId);
  const listId = get(selectedListStore);
  if (listId !== null && detail) {
    removeTaskFromList(listId, detail.section_id, taskId);
  }
  selectedTaskStore.update((s) => (s === taskId ? null : s));
  selectedTaskDetail.update((d) => (d?.id === taskId ? null : d));
}

export async function completeTask(taskId: number): Promise<Task> {
  const updated = await api.tasks.complete(taskId);
  await refreshListDetail();
  selectedTaskDetail.update((d) => (d?.id === taskId ? updated : d));

  if (updated.next_occurrence_id && updated.recurrence_type !== 'none') {
    const nextTask = await api.tasks.get(updated.next_occurrence_id);
    const dateStr = nextTask.due_date
      ? new Date(nextTask.due_date + 'T00:00:00').toLocaleDateString(undefined, {
          month: 'short',
          day: 'numeric'
        })
      : 'soon';
    addToast({ message: `Next: ${dateStr}`, type: 'info' });
  }

  return updated;
}

export async function uncompleteTask(taskId: number): Promise<Task> {
  const updated = await api.tasks.uncomplete(taskId);
  await refreshListDetail();
  selectedTaskDetail.update((d) => (d?.id === taskId ? updated : d));
  return updated;
}

export async function moveTask(taskId: number, payload: MoveTaskInput): Promise<Task> {
  return moveTaskWithOptions(taskId, payload, { refresh: true });
}

export async function moveTaskWithOptions(
  taskId: number,
  payload: MoveTaskInput,
  options: { refresh?: boolean } = {}
): Promise<Task> {
  const refresh = options.refresh ?? true;
  const updated = await api.tasks.move(taskId, payload);
  if (refresh) {
    await refreshListDetail();
  }
  selectedTaskDetail.update((d) => (d?.id === taskId ? updated : d));
  return updated;
}

export async function refreshTasksView(): Promise<void> {
  await refreshListDetail();
}

export async function togglePin(taskId: number): Promise<Task> {
  const updated = await api.tasks.pinToggle(taskId);
  await refreshListDetail();
  selectedTaskDetail.update((d) => (d?.id === taskId ? updated : d));
  return updated;
}

async function refreshListDetail(): Promise<void> {
  const listId = get(selectedListStore);
  if (listId !== null) {
    await loadListDetail(listId);
  }
}

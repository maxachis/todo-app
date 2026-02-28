import { api, type List } from '$lib';

export type EntityType = 'people' | 'organizations' | 'interactions' | 'leads';

export interface LinkedTasksManager {
	allTasks: { id: number; title: string }[];
	linkedTaskIds: number[];
	loadAllTasks: () => Promise<void>;
	loadLinkedTasks: (entityId: number) => Promise<void>;
	addTaskLink: (entityId: number, taskId: number) => Promise<void>;
	removeTaskLink: (entityId: number, taskId: number) => Promise<void>;
	taskName: (t: { id: number }) => string;
}

export function createLinkedTasksManager(entityType: EntityType): LinkedTasksManager {
	let allTasks: { id: number; title: string }[] = $state([]);
	let linkedTaskIds: number[] = $state([]);

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

	async function loadLinkedTasks(entityId: number): Promise<void> {
		if (allTasks.length === 0) await loadAllTasks();
		let links: { task_id: number }[];
		switch (entityType) {
			case 'people':
				links = await api.taskLinks.people.listByPerson(entityId);
				break;
			case 'organizations':
				links = await api.taskLinks.organizations.listByOrg(entityId);
				break;
			case 'interactions':
				links = await api.taskLinks.interactions.list(entityId);
				break;
			case 'leads':
				links = await api.taskLinks.leads.listByLead(entityId);
				break;
		}
		linkedTaskIds = links.map((l) => l.task_id);
	}

	async function addTaskLink(entityId: number, taskId: number): Promise<void> {
		switch (entityType) {
			case 'people':
				await api.taskLinks.people.add(taskId, entityId);
				break;
			case 'organizations':
				await api.taskLinks.organizations.add(taskId, entityId);
				break;
			case 'interactions':
				await api.taskLinks.interactions.add(entityId, taskId);
				break;
			case 'leads':
				await api.taskLinks.leads.add(entityId, taskId);
				break;
		}
		linkedTaskIds = [...linkedTaskIds, taskId];
	}

	async function removeTaskLink(entityId: number, taskId: number): Promise<void> {
		switch (entityType) {
			case 'people':
				await api.taskLinks.people.remove(taskId, entityId);
				break;
			case 'organizations':
				await api.taskLinks.organizations.remove(taskId, entityId);
				break;
			case 'interactions':
				await api.taskLinks.interactions.remove(entityId, taskId);
				break;
			case 'leads':
				await api.taskLinks.leads.remove(entityId, taskId);
				break;
		}
		linkedTaskIds = linkedTaskIds.filter((id) => id !== taskId);
	}

	function taskName(t: { id: number }): string {
		return allTasks.find((x) => x.id === t.id)?.title ?? `Task #${t.id}`;
	}

	return {
		get allTasks() { return allTasks; },
		get linkedTaskIds() { return linkedTaskIds; },
		loadAllTasks,
		loadLinkedTasks,
		addTaskLink,
		removeTaskLink,
		taskName
	};
}

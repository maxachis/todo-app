import { writable } from 'svelte/store';

import { api, type CreateProjectInput, type Project, type UpdateProjectInput } from '$lib';

export const projectsStore = writable<Project[]>([]);

export async function loadProjects(): Promise<void> {
  projectsStore.set(await api.projects.getAll());
}

export async function createProject(payload: CreateProjectInput): Promise<Project> {
  const project = await api.projects.create(payload);
  projectsStore.update((projects) => [...projects, project].sort((a, b) => a.position - b.position));
  return project;
}

export async function updateProject(projectId: number, payload: UpdateProjectInput): Promise<Project> {
  const project = await api.projects.update(projectId, payload);
  projectsStore.update((projects) =>
    projects.map((existing) => (existing.id === projectId ? project : existing))
  );
  return project;
}

export async function toggleProject(projectId: number): Promise<Project> {
  const project = await api.projects.toggle(projectId);
  projectsStore.update((projects) =>
    projects.map((existing) => (existing.id === projectId ? project : existing))
  );
  return project;
}

export async function deleteProject(projectId: number): Promise<void> {
  await api.projects.remove(projectId);
  projectsStore.update((projects) => projects.filter((project) => project.id !== projectId));
}

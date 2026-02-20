import { apiRequest } from './client';
import type {
  CreateListInput,
  CreateProjectInput,
  CreateSectionInput,
  CreateTaskInput,
  CreateTimeEntryInput,
  ImportSummary,
  List,
  MoveInput,
  MoveTaskInput,
  Project,
  SearchResponse,
  Section,
  Tag,
  Task,
  TimeEntry,
  TimesheetResponse,
  UpdateListInput,
  UpdateProjectInput,
  UpdateSectionInput,
  UpdateTaskInput
} from './types';

export const api = {
  lists: {
    getAll: () => apiRequest<List[]>('/lists/'),
    get: (id: number) => apiRequest<List>(`/lists/${id}/`),
    create: (payload: CreateListInput) =>
      apiRequest<List>('/lists/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdateListInput) =>
      apiRequest<List>(`/lists/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/lists/${id}/`, { method: 'DELETE' }),
    move: (id: number, payload: MoveInput) =>
      apiRequest<List>(`/lists/${id}/move/`, { method: 'PATCH', body: JSON.stringify(payload) })
  },
  sections: {
    create: (listId: number, payload: CreateSectionInput) =>
      apiRequest<Section>(`/lists/${listId}/sections/`, {
        method: 'POST',
        body: JSON.stringify(payload)
      }),
    update: (id: number, payload: UpdateSectionInput) =>
      apiRequest<Section>(`/sections/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/sections/${id}/`, { method: 'DELETE' }),
    move: (id: number, payload: MoveInput) =>
      apiRequest<Section>(`/sections/${id}/move/`, {
        method: 'PATCH',
        body: JSON.stringify(payload)
      })
  },
  tasks: {
    create: (sectionId: number, payload: CreateTaskInput) =>
      apiRequest<Task>(`/sections/${sectionId}/tasks/`, {
        method: 'POST',
        body: JSON.stringify(payload)
      }),
    get: (id: number) => apiRequest<Task>(`/tasks/${id}/`),
    update: (id: number, payload: UpdateTaskInput) =>
      apiRequest<Task>(`/tasks/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/tasks/${id}/`, { method: 'DELETE' }),
    complete: (id: number) => apiRequest<Task>(`/tasks/${id}/complete/`, { method: 'POST' }),
    uncomplete: (id: number) => apiRequest<Task>(`/tasks/${id}/uncomplete/`, { method: 'POST' }),
    move: (id: number, payload: MoveTaskInput) =>
      apiRequest<Task>(`/tasks/${id}/move/`, { method: 'PATCH', body: JSON.stringify(payload) }),
    pinToggle: (id: number) => apiRequest<Task>(`/tasks/${id}/pin/`, { method: 'POST' }),
    addTag: (taskId: number, name: string) =>
      apiRequest<Tag[]>(`/tasks/${taskId}/tags/`, {
        method: 'POST',
        body: JSON.stringify({ name })
      }),
    removeTag: (taskId: number, tagId: number) =>
      apiRequest<void>(`/tasks/${taskId}/tags/${tagId}/`, { method: 'DELETE' })
  },
  tags: {
    list: (excludeTask?: number) =>
      apiRequest<Tag[]>(excludeTask ? `/tags/?exclude_task=${excludeTask}` : '/tags/')
  },
  search: {
    run: (query: string) => apiRequest<SearchResponse>(`/search/?q=${encodeURIComponent(query)}`)
  },
  export: {
    all: async (format: 'json' | 'csv' | 'markdown'): Promise<Blob> => {
      const response = await fetch(`/api/export/${format}/`, { credentials: 'same-origin' });
      if (!response.ok) {
        throw new Error(`Export failed: ${response.status}`);
      }
      return response.blob();
    },
    one: async (listId: number, format: 'json' | 'csv' | 'markdown'): Promise<Blob> => {
      const response = await fetch(`/api/export/${listId}/${format}/`, {
        credentials: 'same-origin'
      });
      if (!response.ok) {
        throw new Error(`Export failed: ${response.status}`);
      }
      return response.blob();
    }
  },
  import: {
    upload: (file: File) => {
      const body = new FormData();
      body.append('csv_file', file);
      return apiRequest<ImportSummary>('/import/', { method: 'POST', body });
    }
  },
  projects: {
    getAll: () => apiRequest<Project[]>('/projects/'),
    create: (payload: CreateProjectInput) =>
      apiRequest<Project>('/projects/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdateProjectInput) =>
      apiRequest<Project>(`/projects/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/projects/${id}/`, { method: 'DELETE' }),
    toggle: (id: number) => apiRequest<Project>(`/projects/${id}/toggle/`, { method: 'POST' }),
    getTasks: (id: number) => apiRequest<Task[]>(`/projects/${id}/tasks/`)
  },
  timesheet: {
    get: (week?: string) =>
      apiRequest<TimesheetResponse>(week ? `/timesheet/?week=${week}` : '/timesheet/'),
    create: (payload: CreateTimeEntryInput) =>
      apiRequest<TimeEntry>('/timesheet/', { method: 'POST', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/timesheet/${id}/`, { method: 'DELETE' })
  }
};

import { apiRequest } from './client';
import type {
  CreateInteractionInput,
  CreateListInput,
  CreateOrganizationInput,
  CreatePersonInput,
  CreateProjectInput,
  CreateSectionInput,
  CreateTaskInput,
  CreateTimeEntryInput,
  GraphData,
  ImportSummary,
  Interaction,
  InteractionTaskLink,
  InteractionType,
  List,
  MoveInput,
  MoveTaskInput,
  Organization,
  OrgType,
  Person,
  Project,
  RelationshipOrganizationPerson,
  RelationshipPersonPerson,
  SearchResponse,
  Section,
  Tag,
  Task,
  TaskOrganizationLink,
  TaskPersonLink,
  TimeEntry,
  TimesheetResponse,
  UpcomingTask,
  UpdateInteractionInput,
  UpdateListInput,
  UpdateOrganizationInput,
  UpdatePersonInput,
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
      body.append('file', file);
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
  upcoming: {
    get: () => apiRequest<UpcomingTask[]>('/upcoming/')
  },
  timesheet: {
    get: (week?: string) =>
      apiRequest<TimesheetResponse>(week ? `/timesheet/?week=${week}` : '/timesheet/'),
    create: (payload: CreateTimeEntryInput) =>
      apiRequest<TimeEntry>('/timesheet/', { method: 'POST', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/timesheet/${id}/`, { method: 'DELETE' })
  },
  people: {
    getAll: () => apiRequest<Person[]>('/people/'),
    get: (id: number) => apiRequest<Person>(`/people/${id}/`),
    create: (payload: CreatePersonInput) =>
      apiRequest<Person>('/people/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdatePersonInput) =>
      apiRequest<Person>(`/people/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/people/${id}/`, { method: 'DELETE' })
  },
  organizations: {
    getAll: () => apiRequest<Organization[]>('/organizations/'),
    get: (id: number) => apiRequest<Organization>(`/organizations/${id}/`),
    create: (payload: CreateOrganizationInput) =>
      apiRequest<Organization>('/organizations/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdateOrganizationInput) =>
      apiRequest<Organization>(`/organizations/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/organizations/${id}/`, { method: 'DELETE' })
  },
  orgTypes: {
    getAll: () => apiRequest<OrgType[]>('/org-types/'),
    create: (payload: { name: string }) =>
      apiRequest<OrgType>('/org-types/', { method: 'POST', body: JSON.stringify(payload) })
  },
  interactionTypes: {
    getAll: () => apiRequest<InteractionType[]>('/interaction-types/')
  },
  interactions: {
    getAll: () => apiRequest<Interaction[]>('/interactions/'),
    get: (id: number) => apiRequest<Interaction>(`/interactions/${id}/`),
    create: (payload: CreateInteractionInput) =>
      apiRequest<Interaction>('/interactions/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdateInteractionInput) =>
      apiRequest<Interaction>(`/interactions/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/interactions/${id}/`, { method: 'DELETE' })
  },
  relationships: {
    people: {
      getAll: () => apiRequest<RelationshipPersonPerson[]>('/relationships/people/'),
      create: (payload: { person_1_id: number; person_2_id: number; notes?: string }) =>
        apiRequest<RelationshipPersonPerson>('/relationships/people/', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      remove: (id: number) => apiRequest<void>(`/relationships/people/${id}/`, { method: 'DELETE' })
    },
    organizations: {
      getAll: () => apiRequest<RelationshipOrganizationPerson[]>('/relationships/organizations/'),
      create: (payload: { organization_id: number; person_id: number; notes?: string }) =>
        apiRequest<RelationshipOrganizationPerson>('/relationships/organizations/', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      remove: (id: number) =>
        apiRequest<void>(`/relationships/organizations/${id}/`, { method: 'DELETE' })
    }
  },
  graph: {
    get: () => apiRequest<GraphData>('/graph/')
  },
  taskLinks: {
    people: {
      list: (taskId: number) => apiRequest<TaskPersonLink[]>(`/tasks/${taskId}/people/`),
      listByPerson: (personId: number) =>
        apiRequest<TaskPersonLink[]>(`/people/${personId}/tasks/`),
      add: (taskId: number, personId: number) =>
        apiRequest<TaskPersonLink>(`/tasks/${taskId}/people/`, {
          method: 'POST',
          body: JSON.stringify({ id: personId })
        }),
      remove: (taskId: number, personId: number) =>
        apiRequest<void>(`/tasks/${taskId}/people/${personId}/`, { method: 'DELETE' })
    },
    organizations: {
      list: (taskId: number) =>
        apiRequest<TaskOrganizationLink[]>(`/tasks/${taskId}/organizations/`),
      listByOrg: (organizationId: number) =>
        apiRequest<TaskOrganizationLink[]>(`/organizations/${organizationId}/tasks/`),
      add: (taskId: number, organizationId: number) =>
        apiRequest<TaskOrganizationLink>(`/tasks/${taskId}/organizations/`, {
          method: 'POST',
          body: JSON.stringify({ id: organizationId })
        }),
      remove: (taskId: number, organizationId: number) =>
        apiRequest<void>(`/tasks/${taskId}/organizations/${organizationId}/`, { method: 'DELETE' })
    },
    interactions: {
      list: (interactionId: number) =>
        apiRequest<InteractionTaskLink[]>(`/interactions/${interactionId}/tasks/`),
      add: (interactionId: number, taskId: number) =>
        apiRequest<InteractionTaskLink>(`/interactions/${interactionId}/tasks/`, {
          method: 'POST',
          body: JSON.stringify({ id: taskId })
        }),
      remove: (interactionId: number, taskId: number) =>
        apiRequest<void>(`/interactions/${interactionId}/tasks/${taskId}/`, { method: 'DELETE' })
    }
  }
};

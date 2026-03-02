import { apiRequest } from './client';
import type {
  ContactDraft,
  ContactDraftMatches,
  CreateInteractionInput,
  CreateLeadInput,
  CreateListInput,
  FollowUpDueItem,
  CreateOrganizationInput,
  CreatePersonInput,
  CreateProjectInput,
  CreateSectionInput,
  CreateTaskInput,
  CreateTimeEntryInput,
  GraphData,
  ImportSummary,
  Interaction,
  InteractionMedium,
  InteractionTaskLink,
  InteractionType,
  Lead,
  LeadTaskLink,
  LinkDraftInput,
  List,
  MoveInput,
  MoveTaskInput,
  Organization,
  OrgPersonRelationshipType,
  OrgType,
  Person,
  PersonPersonRelationshipType,
  PersonTag,
  PromoteToOrgInput,
  PromoteToPersonInput,
  Project,
  ProjectLink,
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
  TrendsData,
  UpcomingTask,
  UpdateInteractionInput,
  UpdateLeadInput,
  UpdateListInput,
  UpdateOrganizationInput,
  UpdatePersonInput,
  UpdateProjectInput,
  UpdateSectionInput,
  UpdateTaskInput,
  Page,
  PageBacklink,
  PageCreateInput,
  PageListItem,
  PageUpdateInput
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
    getTasks: (id: number) => apiRequest<Task[]>(`/projects/${id}/tasks/`),
    links: {
      list: (projectId: number) =>
        apiRequest<ProjectLink[]>(`/projects/${projectId}/links/`),
      create: (projectId: number, payload: { url: string; descriptor: string }) =>
        apiRequest<ProjectLink>(`/projects/${projectId}/links/`, {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      update: (projectId: number, linkId: number, payload: { url?: string; descriptor?: string }) =>
        apiRequest<ProjectLink>(`/projects/${projectId}/links/${linkId}/`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        }),
      remove: (projectId: number, linkId: number) =>
        apiRequest<void>(`/projects/${projectId}/links/${linkId}/`, { method: 'DELETE' })
    }
  },
  upcoming: {
    get: () => apiRequest<UpcomingTask[]>('/upcoming/')
  },
  dashboard: {
    trends: () => apiRequest<TrendsData>('/dashboard/trends/'),
    followUpsDue: () => apiRequest<FollowUpDueItem[]>('/dashboard/follow-ups-due/')
  },
  timesheet: {
    get: (week?: string) =>
      apiRequest<TimesheetResponse>(week ? `/timesheet/?week=${week}` : '/timesheet/'),
    create: (payload: CreateTimeEntryInput) =>
      apiRequest<TimeEntry>('/timesheet/', { method: 'POST', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/timesheet/${id}/`, { method: 'DELETE' })
  },
  people: {
    getAll: (tag?: string) =>
      apiRequest<Person[]>(tag ? `/people/?tag=${encodeURIComponent(tag)}` : '/people/'),
    get: (id: number) => apiRequest<Person>(`/people/${id}/`),
    create: (payload: CreatePersonInput) =>
      apiRequest<Person>('/people/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdatePersonInput) =>
      apiRequest<Person>(`/people/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/people/${id}/`, { method: 'DELETE' }),
    addTag: (personId: number, name: string) =>
      apiRequest<PersonTag[]>(`/people/${personId}/tags/`, {
        method: 'POST',
        body: JSON.stringify({ name })
      }),
    removeTag: (personId: number, tagId: number) =>
      apiRequest<void>(`/people/${personId}/tags/${tagId}/`, { method: 'DELETE' })
  },
  personTags: {
    list: (excludePerson?: number) =>
      apiRequest<PersonTag[]>(
        excludePerson ? `/person-tags/?exclude_person=${excludePerson}` : '/person-tags/'
      )
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
    getAll: () => apiRequest<InteractionType[]>('/interaction-types/'),
    create: (payload: { name: string }) =>
      apiRequest<InteractionType>('/interaction-types/', { method: 'POST', body: JSON.stringify(payload) })
  },
  interactionMediums: {
    getAll: () => apiRequest<InteractionMedium[]>('/interaction-mediums/'),
    create: (payload: { name: string }) =>
      apiRequest<InteractionMedium>('/interaction-mediums/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: { name: string }) =>
      apiRequest<InteractionMedium>(`/interaction-mediums/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/interaction-mediums/${id}/`, { method: 'DELETE' })
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
      create: (payload: { person_1_id: number; person_2_id: number; relationship_type_id?: number | null; notes?: string }) =>
        apiRequest<RelationshipPersonPerson>('/relationships/people/', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      update: (id: number, payload: { relationship_type_id?: number | null; notes?: string }) =>
        apiRequest<RelationshipPersonPerson>(`/relationships/people/${id}/`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        }),
      remove: (id: number) => apiRequest<void>(`/relationships/people/${id}/`, { method: 'DELETE' })
    },
    organizations: {
      getAll: () => apiRequest<RelationshipOrganizationPerson[]>('/relationships/organizations/'),
      create: (payload: { organization_id: number; person_id: number; relationship_type_id?: number | null; notes?: string }) =>
        apiRequest<RelationshipOrganizationPerson>('/relationships/organizations/', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      update: (id: number, payload: { relationship_type_id?: number | null; notes?: string }) =>
        apiRequest<RelationshipOrganizationPerson>(`/relationships/organizations/${id}/`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        }),
      remove: (id: number) =>
        apiRequest<void>(`/relationships/organizations/${id}/`, { method: 'DELETE' })
    }
  },
  relationshipTypes: {
    people: {
      getAll: () => apiRequest<PersonPersonRelationshipType[]>('/relationship-types/people/'),
      create: (payload: { name: string }) =>
        apiRequest<PersonPersonRelationshipType>('/relationship-types/people/', {
          method: 'POST',
          body: JSON.stringify(payload)
        })
    },
    organizations: {
      getAll: () => apiRequest<OrgPersonRelationshipType[]>('/relationship-types/organizations/'),
      create: (payload: { name: string }) =>
        apiRequest<OrgPersonRelationshipType>('/relationship-types/organizations/', {
          method: 'POST',
          body: JSON.stringify(payload)
        })
    }
  },
  contactDrafts: {
    list: () => apiRequest<ContactDraft[]>('/contact-drafts/'),
    get: (id: number) => apiRequest<ContactDraft>(`/contact-drafts/${id}/`),
    dismiss: (id: number) =>
      apiRequest<ContactDraft>(`/contact-drafts/${id}/dismiss/`, { method: 'POST' }),
    remove: (id: number) => apiRequest<void>(`/contact-drafts/${id}/`, { method: 'DELETE' }),
    promoteToPerson: (id: number, data: PromoteToPersonInput) =>
      apiRequest<{ id: number; first_name: string; last_name: string }>(
        `/contact-drafts/${id}/promote/person/`,
        { method: 'POST', body: JSON.stringify(data) }
      ),
    promoteToOrg: (id: number, data: PromoteToOrgInput) =>
      apiRequest<{ id: number; name: string }>(
        `/contact-drafts/${id}/promote/org/`,
        { method: 'POST', body: JSON.stringify(data) }
      ),
    link: (id: number, data: LinkDraftInput) =>
      apiRequest<ContactDraft>(`/contact-drafts/${id}/link/`, {
        method: 'POST',
        body: JSON.stringify(data)
      }),
    matches: (id: number) =>
      apiRequest<ContactDraftMatches>(`/contact-drafts/${id}/matches/`)
  },
  leads: {
    getAll: () => apiRequest<Lead[]>('/leads/'),
    get: (id: number) => apiRequest<Lead>(`/leads/${id}/`),
    create: (payload: CreateLeadInput) =>
      apiRequest<Lead>('/leads/', { method: 'POST', body: JSON.stringify(payload) }),
    update: (id: number, payload: UpdateLeadInput) =>
      apiRequest<Lead>(`/leads/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
    remove: (id: number) => apiRequest<void>(`/leads/${id}/`, { method: 'DELETE' })
  },
  notebook: {
    pages: {
      list: (params?: { search?: string; page_type?: string }) => {
        const query = new URLSearchParams();
        if (params?.search) query.set('search', params.search);
        if (params?.page_type) query.set('page_type', params.page_type);
        const qs = query.toString();
        return apiRequest<PageListItem[]>(`/notebook/pages/${qs ? `?${qs}` : ''}`);
      },
      create: (payload: PageCreateInput) =>
        apiRequest<Page>('/notebook/pages/', { method: 'POST', body: JSON.stringify(payload) }),
      get: (slug: string) => apiRequest<Page>(`/notebook/pages/${slug}/`),
      update: (slug: string, payload: PageUpdateInput) =>
        apiRequest<Page>(`/notebook/pages/${slug}/`, { method: 'PUT', body: JSON.stringify(payload) }),
      remove: (slug: string) => apiRequest<void>(`/notebook/pages/${slug}/`, { method: 'DELETE' })
    },
    mentions: (entityType: string, entityId: number) =>
      apiRequest<PageBacklink[]>(`/notebook/mentions/${entityType}/${entityId}/`)
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
    },
    leads: {
      listByLead: (leadId: number) =>
        apiRequest<LeadTaskLink[]>(`/leads/${leadId}/tasks/`),
      add: (leadId: number, taskId: number) =>
        apiRequest<LeadTaskLink>(`/leads/${leadId}/tasks/`, {
          method: 'POST',
          body: JSON.stringify({ id: taskId })
        }),
      remove: (leadId: number, taskId: number) =>
        apiRequest<void>(`/leads/${leadId}/tasks/${taskId}/`, { method: 'DELETE' })
    }
  }
};

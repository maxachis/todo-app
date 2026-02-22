export interface Tag {
  id: number;
  name: string;
}

export interface Task {
  id: number;
  section_id: number;
  parent_id: number | null;
  title: string;
  notes: string;
  priority: number;
  due_date: string | null;
  due_time: string | null;
  is_completed: boolean;
  completed_at: string | null;
  created_at: string;
  position: number;
  external_id: string | null;
  is_pinned: boolean;
  tags: Tag[];
  subtasks: Task[];
  recurrence_type: string;
  recurrence_rule: Record<string, unknown>;
  next_occurrence_id: number | null;
}

export interface Section {
  id: number;
  list_id: number;
  name: string;
  emoji: string;
  position: number;
  tasks: Task[];
}

export interface List {
  id: number;
  name: string;
  emoji: string;
  position: number;
  project_id: number | null;
  sections: Section[];
}

export interface Project {
  id: number;
  name: string;
  description: string;
  is_active: boolean;
  position: number;
  total_hours: number | null;
  linked_lists_count: number | null;
  total_tasks: number | null;
  completed_tasks: number | null;
}

export interface TimeEntry {
  id: number;
  project_id: number;
  task_ids: number[];
  description: string;
  date: string;
  created_at: string;
}

export interface UpcomingTask {
  id: number;
  title: string;
  due_date: string;
  due_time: string | null;
  priority: number;
  is_pinned: boolean;
  list_id: number;
  list_name: string;
  list_emoji: string;
  section_id: number;
  section_name: string;
  tags: string[];
}

export interface SearchResultTask {
  id: number;
  title: string;
  section_name: string;
  tags: string[];
}

export interface SearchResultGroup {
  list: {
    id: number;
    name: string;
    emoji: string;
  };
  tasks: SearchResultTask[];
}

export interface SearchResponse {
  query: string;
  total_count: number;
  results: SearchResultGroup[];
}

export interface TimesheetSummaryItem {
  project_id: number;
  project_name: string;
  hours: number;
}

export interface TimesheetResponse {
  week_start: string;
  week_end: string;
  entries_by_date: Record<
    string,
    Array<{
      id: number;
      project_id: number;
      project_name: string;
      description: string;
      task_ids: number[];
      created_at: string;
    }>
  >;
  summary: {
    total_hours: number;
    per_project: TimesheetSummaryItem[];
  };
}

export interface ImportSummary {
  lists_created: number;
  sections_created: number;
  tags_created: number;
  tasks_created: number;
  tasks_skipped: number;
  parents_linked: number;
  errors: number;
  error_details: string[];
}

// Network types

export interface Person {
  id: number;
  first_name: string;
  middle_name: string;
  last_name: string;
  notes: string;
  follow_up_cadence_days: number | null;
  created_at: string;
  updated_at: string;
}

export interface CreatePersonInput {
  first_name: string;
  last_name: string;
  middle_name?: string;
  notes?: string;
  follow_up_cadence_days?: number | null;
}

export interface UpdatePersonInput {
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  notes?: string;
  follow_up_cadence_days?: number | null;
}

export interface OrgType {
  id: number;
  name: string;
}

export interface Organization {
  id: number;
  name: string;
  org_type_id: number;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface CreateOrganizationInput {
  name: string;
  org_type_id: number;
  notes?: string;
}

export interface UpdateOrganizationInput {
  name?: string;
  org_type_id?: number;
  notes?: string;
}

export interface InteractionType {
  id: number;
  name: string;
}

export interface Interaction {
  id: number;
  person_id: number;
  interaction_type_id: number;
  date: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface CreateInteractionInput {
  person_id: number;
  interaction_type_id: number;
  date: string;
  notes?: string;
}

export interface UpdateInteractionInput {
  person_id?: number;
  interaction_type_id?: number;
  date?: string;
  notes?: string;
}

export interface RelationshipPersonPerson {
  id: number;
  person_1_id: number;
  person_2_id: number;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface RelationshipOrganizationPerson {
  id: number;
  organization_id: number;
  person_id: number;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface GraphNode {
  data: {
    id: string;
    label: string;
    type: string;
    details: Record<string, string>;
  };
}

export interface GraphEdge {
  data: {
    id: string;
    source: string;
    target: string;
    type: string;
    notes: string;
  };
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface CreateListInput {
  name: string;
  emoji?: string;
  project_id?: number | null;
}

export interface UpdateListInput {
  name?: string;
  emoji?: string;
  project_id?: number | null;
}

export interface MoveInput {
  position: number;
}

export interface CreateSectionInput {
  name: string;
  emoji?: string;
}

export interface UpdateSectionInput {
  name?: string;
  emoji?: string;
}

export interface CreateTaskInput {
  title: string;
  parent_id?: number | null;
}

export interface UpdateTaskInput {
  title?: string;
  notes?: string;
  due_date?: string | null;
  due_time?: string | null;
  priority?: number;
  recurrence_type?: string;
  recurrence_rule?: Record<string, unknown>;
}

export interface MoveTaskInput {
  position?: number;
  section_id?: number;
  parent_id?: number | null;
  list_id?: number;
}

export interface CreateProjectInput {
  name: string;
  description?: string;
}

export interface UpdateProjectInput {
  name?: string;
  description?: string;
  is_active?: boolean;
}

export interface CreateTimeEntryInput {
  project_id: number;
  date: string;
  description?: string;
  task_ids?: number[];
}

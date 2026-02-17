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

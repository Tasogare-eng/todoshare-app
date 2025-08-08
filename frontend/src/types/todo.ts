export enum TodoStatus {
  PENDING = 'pending',
  COMPLETED = 'completed'
}

export enum TodoPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export interface Todo {
  id: string
  user_id: string
  title: string
  description?: string
  status: TodoStatus
  priority?: TodoPriority
  due_date?: string
  created_at: string
  updated_at?: string
  category_ids?: string[]
  categories?: Category[]
}

interface Category {
  id: string
  name: string
  color: string
  description?: string
}

export interface TodoCreate {
  title: string
  description?: string
  status?: TodoStatus
  priority?: TodoPriority
  due_date?: string
  category_ids?: string[]
}

export interface TodoUpdate {
  title?: string
  description?: string
  status?: TodoStatus
  priority?: TodoPriority
  due_date?: string
  category_ids?: string[]
}

export interface TodoListResponse {
  items: Todo[]
  total: number
  page: number
  per_page: number
  pages: number
}
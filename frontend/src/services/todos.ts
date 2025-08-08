import api from './api'
import type { Todo, TodoCreate, TodoUpdate, TodoListResponse, TodoStatus } from '@/types/todo'

export const todosApi = {
  async getTodos(params?: {
    page?: number
    per_page?: number
    status?: TodoStatus
    sort_by?: string
    sort_order?: string
    search?: string
    priority?: string
    category_ids?: string
    due_date_from?: string
    due_date_to?: string
  }): Promise<TodoListResponse> {
    const response = await api.get('/todos', { params })
    return response.data
  },

  async getTodo(id: string): Promise<Todo> {
    const response = await api.get(`/todos/${id}`)
    return response.data
  },

  async createTodo(data: TodoCreate): Promise<Todo> {
    const response = await api.post('/todos', data)
    return response.data
  },

  async updateTodo(id: string, data: TodoUpdate): Promise<Todo> {
    const response = await api.put(`/todos/${id}`, data)
    return response.data
  },

  async deleteTodo(id: string): Promise<void> {
    await api.delete(`/todos/${id}`)
  },

  async toggleTodoStatus(id: string): Promise<Todo> {
    const response = await api.patch(`/todos/${id}/toggle`)
    return response.data
  }
}
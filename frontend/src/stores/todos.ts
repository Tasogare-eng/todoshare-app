import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { todosApi } from '@/services/todos'
import type { Todo, TodoCreate, TodoUpdate, TodoStatus } from '@/types/todo'

export const useTodosStore = defineStore('todos', () => {
  // State
  const todos = ref<Todo[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(0)
  const totalTodos = ref(0)
  const perPage = ref(20)
  
  // Filter state
  const filterStatus = ref<TodoStatus | null>(null)
  const sortBy = ref('created_at')
  const sortOrder = ref('desc')
  const searchQuery = ref('')
  const filterPriority = ref<string | null>(null)
  const filterCategoryIds = ref<string[]>([])
  const filterDueDateFrom = ref<string | null>(null)
  const filterDueDateTo = ref<string | null>(null)

  // Getters
  const pendingTodos = computed(() => 
    todos.value.filter(todo => todo.status === 'pending')
  )
  
  const completedTodos = computed(() => 
    todos.value.filter(todo => todo.status === 'completed')
  )
  
  const todayTodos = computed(() => {
    const today = new Date().toDateString()
    return todos.value.filter(todo => {
      if (!todo.due_date) return false
      return new Date(todo.due_date).toDateString() === today
    })
  })

  // Actions
  const fetchTodos = async (page: number = 1) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await todosApi.getTodos({
        page,
        per_page: perPage.value,
        status: filterStatus.value || undefined,
        sort_by: sortBy.value,
        sort_order: sortOrder.value,
        search: searchQuery.value || undefined,
        priority: filterPriority.value || undefined,
        category_ids: filterCategoryIds.value.length > 0 ? filterCategoryIds.value.join(',') : undefined,
        due_date_from: filterDueDateFrom.value || undefined,
        due_date_to: filterDueDateTo.value || undefined
      })
      
      todos.value = response.items
      currentPage.value = response.page
      totalPages.value = response.pages
      totalTodos.value = response.total
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch todos'
      return false
    } finally {
      loading.value = false
    }
  }

  const createTodo = async (data: TodoCreate) => {
    try {
      loading.value = true
      error.value = null
      
      const newTodo = await todosApi.createTodo(data)
      
      // Add to list and refresh
      todos.value.unshift(newTodo)
      totalTodos.value++
      
      return newTodo
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create todo'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateTodo = async (id: string, data: TodoUpdate) => {
    try {
      loading.value = true
      error.value = null
      
      const updatedTodo = await todosApi.updateTodo(id, data)
      
      // Update in list
      const index = todos.value.findIndex(t => t.id === id)
      if (index !== -1) {
        todos.value[index] = updatedTodo
      }
      
      return updatedTodo
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update todo'
      return null
    } finally {
      loading.value = false
    }
  }

  const deleteTodo = async (id: string) => {
    try {
      loading.value = true
      error.value = null
      
      await todosApi.deleteTodo(id)
      
      // Remove from list
      todos.value = todos.value.filter(t => t.id !== id)
      totalTodos.value--
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete todo'
      return false
    } finally {
      loading.value = false
    }
  }

  const toggleTodoStatus = async (id: string) => {
    try {
      const updatedTodo = await todosApi.toggleTodoStatus(id)
      
      // Update in list
      const index = todos.value.findIndex(t => t.id === id)
      if (index !== -1) {
        todos.value[index] = updatedTodo
      }
      
      return updatedTodo
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to toggle todo status'
      return null
    }
  }

  const setFilter = (status: TodoStatus | null) => {
    filterStatus.value = status
    fetchTodos(1) // Reset to first page when filtering
  }

  const setSort = (field: string, order: string) => {
    sortBy.value = field
    sortOrder.value = order
    fetchTodos(currentPage.value)
  }

  const setSearch = (query: string) => {
    searchQuery.value = query
    fetchTodos(1)
  }

  const setAdvancedFilters = (filters: {
    status?: string | null
    priority?: string | null
    categoryIds?: string[]
    dueDateFrom?: string | null
    dueDateTo?: string | null
  }) => {
    if (filters.status !== undefined) filterStatus.value = filters.status as TodoStatus | null
    if (filters.priority !== undefined) filterPriority.value = filters.priority
    if (filters.categoryIds !== undefined) filterCategoryIds.value = filters.categoryIds
    if (filters.dueDateFrom !== undefined) filterDueDateFrom.value = filters.dueDateFrom
    if (filters.dueDateTo !== undefined) filterDueDateTo.value = filters.dueDateTo
    fetchTodos(1)
  }

  const clearAllFilters = () => {
    filterStatus.value = null
    filterPriority.value = null
    filterCategoryIds.value = []
    filterDueDateFrom.value = null
    filterDueDateTo.value = null
    searchQuery.value = ''
    fetchTodos(1)
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    todos: computed(() => todos.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    currentPage: computed(() => currentPage.value),
    totalPages: computed(() => totalPages.value),
    totalTodos: computed(() => totalTodos.value),
    
    // Filter state
    filterStatus: computed(() => filterStatus.value),
    sortBy: computed(() => sortBy.value),
    sortOrder: computed(() => sortOrder.value),
    searchQuery: computed(() => searchQuery.value),
    filterPriority: computed(() => filterPriority.value),
    filterCategoryIds: computed(() => filterCategoryIds.value),
    
    // Getters
    pendingTodos,
    completedTodos,
    todayTodos,
    
    // Actions
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodoStatus,
    setFilter,
    setSort,
    setSearch,
    setAdvancedFilters,
    clearAllFilters,
    clearError
  }
})
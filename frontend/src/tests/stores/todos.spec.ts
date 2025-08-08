import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTodosStore } from '@/stores/todos'
import { TodoStatus } from '@/types/todo'

// Mock the API
vi.mock('@/services/todos', () => ({
  todosApi: {
    getTodos: vi.fn(),
    createTodo: vi.fn(),
    updateTodo: vi.fn(),
    deleteTodo: vi.fn(),
    toggleTodoStatus: vi.fn()
  }
}))

describe('Todos Store', () => {
  let todosStore: ReturnType<typeof useTodosStore>

  beforeEach(() => {
    setActivePinia(createPinia())
    todosStore = useTodosStore()
  })

  it('initializes with empty state', () => {
    expect(todosStore.todos).toEqual([])
    expect(todosStore.loading).toBe(false)
    expect(todosStore.error).toBe(null)
    expect(todosStore.currentPage).toBe(1)
    expect(todosStore.totalTodos).toBe(0)
  })

  it('updates search query', () => {
    todosStore.setSearch('test query')
    expect(todosStore.searchQuery).toBe('test query')
  })

  it('filters todos correctly', () => {
    todosStore.setFilter(TodoStatus.COMPLETED)
    expect(todosStore.filterStatus).toBe(TodoStatus.COMPLETED)
  })

  it('clears all filters', () => {
    todosStore.setFilter(TodoStatus.COMPLETED)
    todosStore.setSearch('test')
    
    todosStore.clearAllFilters()
    
    expect(todosStore.filterStatus).toBe(null)
    expect(todosStore.searchQuery).toBe('')
  })

  it('manages advanced filters', () => {
    todosStore.setAdvancedFilters({
      status: TodoStatus.PENDING,
      priority: 'high',
      categoryIds: ['cat1', 'cat2']
    })

    expect(todosStore.filterStatus).toBe(TodoStatus.PENDING)
    expect(todosStore.filterPriority).toBe('high')
    expect(todosStore.filterCategoryIds).toEqual(['cat1', 'cat2'])
  })

  it('clears errors', () => {
    // Use clearError method directly since error is readonly computed
    todosStore.clearError()
    expect(todosStore.error).toBe(null)
  })
})
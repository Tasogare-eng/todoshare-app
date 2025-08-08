<template>
  <div class="todo-list">
    <div class="list-header">
      <div class="list-controls">
        <div class="filters">
          <button 
            :class="{ active: !filterStatus }"
            @click="setFilter(null)"
          >
            All ({{ totalTodos }})
          </button>
          <button 
            :class="{ active: filterStatus === TodoStatus.PENDING }"
            @click="setFilter(TodoStatus.PENDING)"
          >
            Pending ({{ pendingTodos.length }})
          </button>
          <button 
            :class="{ active: filterStatus === TodoStatus.COMPLETED }"
            @click="setFilter(TodoStatus.COMPLETED)"
          >
            Completed ({{ completedTodos.length }})
          </button>
        </div>
        
        <div class="sort-controls">
          <select v-model="currentSort" @change="updateSort">
            <option value="created_at:desc">Newest first</option>
            <option value="created_at:asc">Oldest first</option>
            <option value="due_date:asc">Due date (earliest)</option>
            <option value="due_date:desc">Due date (latest)</option>
            <option value="priority:desc">Priority (high to low)</option>
            <option value="title:asc">Title (A-Z)</option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      Loading todos...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="clearError" class="clear-error">×</button>
    </div>

    <div v-else-if="todos.length === 0" class="empty-state">
      <p>No todos found</p>
      <p v-if="filterStatus" class="filter-hint">
        Try changing your filter to see more todos
      </p>
    </div>

    <div v-else class="todos-container">
      <TodoCard
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        @update="handleUpdate"
        @delete="handleDelete"
        @toggle="handleToggle"
      />
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button 
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
        class="page-btn"
      >
        Previous
      </button>
      
      <span class="page-info">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      
      <button 
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
        class="page-btn"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useTodosStore } from '@/stores/todos'
import TodoCard from './TodoCard.vue'
import { TodoStatus } from '@/types/todo'

const todosStore = useTodosStore()

const { 
  todos, 
  loading, 
  error, 
  currentPage, 
  totalPages, 
  totalTodos,
  filterStatus,
  sortBy,
  sortOrder,
  pendingTodos,
  completedTodos
} = storeToRefs(todosStore)

const { 
  fetchTodos, 
  setFilter, 
  setSort, 
  clearError,
  updateTodo,
  deleteTodo,
  toggleTodoStatus
} = todosStore

const currentSort = ref(`${sortBy.value}:${sortOrder.value}`)

const updateSort = () => {
  const [field, order] = currentSort.value.split(':')
  setSort(field, order)
}

const goToPage = (page: number) => {
  fetchTodos(page)
}

const handleUpdate = async (id: string, data: any) => {
  await updateTodo(id, data)
}

const handleDelete = async (id: string) => {
  if (confirm('Are you sure you want to delete this todo?')) {
    await deleteTodo(id)
  }
}

const handleToggle = async (id: string) => {
  await toggleTodoStatus(id)
}

onMounted(() => {
  fetchTodos()
})
</script>

<style scoped>
.todo-list {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.list-header {
  margin-bottom: 2rem;
}

.list-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.filters {
  display: flex;
  gap: 0.5rem;
}

.filters button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.filters button:hover {
  background: #f5f5f5;
}

.filters button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.sort-controls select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.loading, .error, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
  position: relative;
}

.clear-error {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #c33;
}

.filter-hint {
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.todos-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #f5f5f5;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .list-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters {
    justify-content: center;
  }
  
  .filters button {
    flex: 1;
    min-width: 0;
  }
}
</style>
<template>
  <div class="todos-view">
    <div class="view-header">
      <div class="header-content">
        <h1>My Todos</h1>
        <p class="subtitle">Manage your tasks and stay organized</p>
      </div>
      <div class="header-actions">
        <SearchBar
          @search="handleSearch"
          @clear="handleClearSearch"
        />
        <button @click="showCreateForm = true" class="create-btn">
          <span class="btn-icon">+</span>
          New Todo
        </button>
      </div>
    </div>

    <!-- Create Todo Form Modal -->
    <div v-if="showCreateForm" class="modal-overlay" @click="closeCreateForm">
      <div class="modal-content" @click.stop>
        <TodoForm
          :loading="todosStore.loading"
          :error="todosStore.error"
          @submit="handleCreateTodo"
          @cancel="closeCreateForm"
          @close="closeCreateForm"
          @clear-error="todosStore.clearError"
        />
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <span class="stat-number">{{ todosStore.totalTodos }}</span>
          <span class="stat-label">Total</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <span class="stat-number">{{ todosStore.pendingTodos.length }}</span>
          <span class="stat-label">Pending</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-number">{{ todosStore.completedTodos.length }}</span>
          <span class="stat-label">Completed</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <span class="stat-number">{{ todosStore.todayTodos.length }}</span>
          <span class="stat-label">Due Today</span>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="content-layout">
        <aside class="filters-sidebar">
          <FilterPanel @filters-changed="handleFiltersChanged" />
        </aside>
        <main class="todos-main">
          <TodoList />
        </main>
      </div>
    </div>

    <!-- Quick Add Button (Mobile) -->
    <button class="fab" @click="showCreateForm = true">
      +
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useTodosStore } from '@/stores/todos'
import { useAuthStore } from '@/stores/auth'
import TodoList from '@/components/TodoList.vue'
import TodoForm from '@/components/TodoForm.vue'
import SearchBar from '@/components/SearchBar.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import type { TodoCreate } from '@/types/todo'

const authStore = useAuthStore()
const todosStore = useTodosStore()

const showCreateForm = ref(false)

const handleCreateTodo = async (data: TodoCreate) => {
  const result = await todosStore.createTodo(data)
  if (result) {
    showCreateForm.value = false
  }
}

const closeCreateForm = () => {
  showCreateForm.value = false
  todosStore.clearError()
}

const handleSearch = (query: string) => {
  todosStore.setSearch(query)
}

const handleClearSearch = () => {
  todosStore.setSearch('')
}

const handleFiltersChanged = (filters: any) => {
  todosStore.setAdvancedFilters({
    status: filters.status,
    priority: filters.priority,
    categoryIds: filters.categoryIds,
    dueDateFrom: filters.dueDateFrom,
    dueDateTo: filters.dueDateTo
  })
}

const handleKeypress = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    closeCreateForm()
  }
  
  if ((event.metaKey || event.ctrlKey) && event.key === 'n') {
    event.preventDefault()
    showCreateForm.value = true
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeypress)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeypress)
})
</script>

<style scoped>
.todos-view {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 1rem;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  gap: 1rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.header-content h1 {
  margin: 0;
  color: #343a40;
  font-size: 2rem;
  font-weight: 600;
}

.subtitle {
  margin: 0.25rem 0 0 0;
  color: #6c757d;
  font-size: 1rem;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn:hover {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 50%;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 600;
  color: #343a40;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.content-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  align-items: start;
}

.filters-sidebar {
  position: sticky;
  top: 1rem;
}

.todos-main {
  min-width: 0;
}

.fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  border: none;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
  transition: all 0.2s ease;
  z-index: 100;
  display: none;
}

.fab:hover {
  background: #0056b3;
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.5);
}

@media (max-width: 768px) {
  .view-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
    align-items: center;
  }

  .header-content h1 {
    font-size: 1.75rem;
  }

  .header-actions {
    width: 100%;
    justify-content: center;
  }

  .create-btn {
    display: none;
  }

  .fab {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .content-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .filters-sidebar {
    order: 2;
    position: relative;
    top: auto;
  }

  .todos-main {
    order: 1;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-icon {
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
  }

  .stat-number {
    font-size: 1.25rem;
  }

  .modal-overlay {
    padding: 0.5rem;
  }
}

@media (max-width: 480px) {
  .stats-section {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 0.75rem;
    gap: 0.75rem;
  }
}
</style>
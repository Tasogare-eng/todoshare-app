<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <nav class="flex items-center space-x-4 text-sm text-gray-600 mb-4">
          <router-link to="/dashboard" class="hover:text-primary-600 transition-colors">Dashboard</router-link>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          <router-link to="/todos" class="hover:text-primary-600 transition-colors">Todos</router-link>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          <span class="text-gray-900">{{ isEditMode ? 'Edit Todo' : 'New Todo' }}</span>
        </nav>
        
        <div class="flex items-center justify-between">
          <h1 class="text-3xl font-bold text-gray-900">
            {{ isEditMode ? 'Edit Todo' : 'Create New Todo' }}
          </h1>
          <router-link to="/todos" class="btn btn-secondary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Todos
          </router-link>
        </div>
      </div>

      <!-- Form Card -->
      <div class="card">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Title -->
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
              Title <span class="text-red-500">*</span>
            </label>
            <input
              id="title"
              v-model="formData.title"
              type="text"
              required
              :disabled="loading"
              placeholder="Enter todo title"
              class="input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.title }"
            />
            <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
          </div>

          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id="description"
              v-model="formData.description"
              rows="4"
              :disabled="loading"
              placeholder="Enter todo description"
              class="input resize-none"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.description }"
            ></textarea>
            <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
          </div>

          <!-- Priority and Due Date Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Priority -->
            <div>
              <label for="priority" class="block text-sm font-medium text-gray-700 mb-2">
                Priority
              </label>
              <select
                id="priority"
                v-model="formData.priority"
                :disabled="loading"
                class="input"
              >
                <option value="">Select priority</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <!-- Due Date -->
            <div>
              <label for="due_date" class="block text-sm font-medium text-gray-700 mb-2">
                Due Date
              </label>
              <input
                id="due_date"
                v-model="formData.due_date"
                type="datetime-local"
                :disabled="loading"
                class="input"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.due_date }"
              />
              <p v-if="errors.due_date" class="mt-1 text-sm text-red-600">{{ errors.due_date }}</p>
            </div>
          </div>

          <!-- Categories -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Categories
            </label>
            <div class="space-y-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg p-3">
              <div v-if="categories.length === 0" class="text-gray-500 text-sm text-center py-4">
                No categories available. 
                <router-link to="/categories" class="text-primary-600 hover:text-primary-500">
                  Create categories
                </router-link>
              </div>
              <label 
                v-for="category in categories" 
                :key="category.id"
                class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer"
              >
                <input
                  type="checkbox"
                  :value="category.id"
                  v-model="formData.category_ids"
                  :disabled="loading"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <div class="ml-3 flex items-center">
                  <div 
                    class="w-4 h-4 rounded-full mr-2"
                    :style="{ backgroundColor: category.color }"
                  ></div>
                  <span class="text-sm text-gray-700">{{ category.name }}</span>
                  <span v-if="category.description" class="text-xs text-gray-500 ml-2">
                    ({{ category.description }})
                  </span>
                </div>
              </label>
            </div>
          </div>

          <!-- Status (only in edit mode) -->
          <div v-if="isEditMode">
            <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              id="status"
              v-model="formData.status"
              :disabled="loading"
              class="input"
            >
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <!-- Form Actions -->
          <div class="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
            <router-link to="/todos" class="btn btn-secondary">
              Cancel
            </router-link>
            <button
              type="submit"
              :disabled="loading || !isFormValid"
              class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span v-if="loading">{{ isEditMode ? 'Updating...' : 'Creating...' }}</span>
              <span v-else>{{ isEditMode ? 'Update Todo' : 'Create Todo' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTodosStore } from '@/stores/todos'
import { useCategoriesStore } from '@/stores/categories'
import { TodoStatus } from '@/types/todo'
import type { TodoCreate, TodoUpdate } from '@/types/todo'

const router = useRouter()
const route = useRoute()
const todosStore = useTodosStore()
const categoriesStore = useCategoriesStore()

// State
const loading = ref(false)
const error = ref<string | null>(null)

// Form data
const formData = reactive({
  title: '',
  description: '',
  priority: '',
  due_date: '',
  status: TodoStatus.PENDING,
  category_ids: [] as string[]
})

// Form validation
const errors = reactive({
  title: '',
  description: '',
  due_date: ''
})

// Computed
const isEditMode = computed(() => !!route.params.id)
const todoId = computed(() => route.params.id as string)
const categories = computed(() => categoriesStore.categories)

const isFormValid = computed(() => {
  return formData.title.trim().length > 0 && !Object.values(errors).some(error => error)
})

// Methods
const validateForm = () => {
  // Reset errors
  errors.title = ''
  errors.description = ''
  errors.due_date = ''

  // Validate title
  if (!formData.title.trim()) {
    errors.title = 'Title is required'
  } else if (formData.title.trim().length > 200) {
    errors.title = 'Title must be less than 200 characters'
  }

  // Validate description
  if (formData.description && formData.description.length > 1000) {
    errors.description = 'Description must be less than 1000 characters'
  }

  // Validate due date
  if (formData.due_date) {
    const dueDate = new Date(formData.due_date)
    const now = new Date()
    if (dueDate < now) {
      errors.due_date = 'Due date cannot be in the past'
    }
  }

  return !Object.values(errors).some(error => error)
}

const loadTodo = async () => {
  if (!isEditMode.value) return

  try {
    loading.value = true
    const todo = todosStore.todos.find(t => t.id === todoId.value)
    
    if (!todo) {
      // Try to fetch the specific todo
      await todosStore.fetchTodos()
      const fetchedTodo = todosStore.todos.find(t => t.id === todoId.value)
      
      if (!fetchedTodo) {
        error.value = 'Todo not found'
        return
      }
      
      populateForm(fetchedTodo)
    } else {
      populateForm(todo)
    }
  } catch (err) {
    error.value = 'Failed to load todo'
    console.error('Error loading todo:', err)
  } finally {
    loading.value = false
  }
}

const populateForm = (todo: any) => {
  formData.title = todo.title
  formData.description = todo.description || ''
  formData.priority = todo.priority || ''
  formData.due_date = todo.due_date ? new Date(todo.due_date).toISOString().slice(0, 16) : ''
  formData.status = todo.status
  formData.category_ids = todo.category_ids || []
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    loading.value = true
    error.value = null

    const submitData = {
      title: formData.title.trim(),
      description: formData.description.trim() || undefined,
      priority: formData.priority || undefined,
      due_date: formData.due_date || undefined,
      status: formData.status,
      category_ids: formData.category_ids.length > 0 ? formData.category_ids : undefined
    }

    if (isEditMode.value) {
      await todosStore.updateTodo(todoId.value, submitData as TodoUpdate)
    } else {
      await todosStore.createTodo(submitData as TodoCreate)
    }

    // Redirect to todos list
    router.push('/todos')
  } catch (err: any) {
    error.value = err.message || `Failed to ${isEditMode.value ? 'update' : 'create'} todo`
    console.error(`Error ${isEditMode.value ? 'updating' : 'creating'} todo:`, err)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.title = ''
  formData.description = ''
  formData.priority = ''
  formData.due_date = ''
  formData.status = TodoStatus.PENDING
  formData.category_ids = []
  
  errors.title = ''
  errors.description = ''
  errors.due_date = ''
}

// Lifecycle
onMounted(async () => {
  // Load categories
  await categoriesStore.fetchCategories()
  
  // Load todo if in edit mode
  if (isEditMode.value) {
    await loadTodo()
  } else {
    resetForm()
  }
})
</script>
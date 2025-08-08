<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <nav class="flex items-center space-x-4 text-sm text-gray-600 mb-4">
          <router-link to="/dashboard" class="hover:text-primary-600 transition-colors">Dashboard</router-link>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          <span class="text-gray-900">Categories</span>
        </nav>
        
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Categories</h1>
            <p class="mt-1 text-gray-600">Organize your todos with custom categories</p>
          </div>
          <button @click="showCreateModal = true" class="btn btn-primary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Category
          </button>
        </div>
      </div>

      <!-- Categories Grid -->
      <div v-if="loading && categories.length === 0" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p class="text-gray-600">Loading categories...</p>
      </div>

      <div v-else-if="error && categories.length === 0" class="text-center py-12">
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg inline-block">
          {{ error }}
        </div>
      </div>

      <div v-else-if="categories.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No categories yet</h3>
        <p class="text-gray-600 mb-4">Create your first category to organize your todos</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Create Category
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="category in categories" 
          :key="category.id"
          class="card group hover:scale-105 transition-all duration-200"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <div 
                class="w-6 h-6 rounded-full mr-3 flex-shrink-0"
                :style="{ backgroundColor: category.color }"
              ></div>
              <div class="min-w-0 flex-1">
                <h3 class="font-semibold text-gray-900 truncate">{{ category.name }}</h3>
                <p v-if="category.description" class="text-sm text-gray-600 mt-1">
                  {{ category.description }}
                </p>
              </div>
            </div>
            
            <!-- Actions Menu -->
            <div class="relative">
              <button 
                @click="toggleMenu(category.id)"
                class="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-gray-100 rounded"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                </svg>
              </button>
              
              <!-- Dropdown Menu -->
              <div 
                v-if="activeMenu === category.id"
                class="absolute right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
              >
                <button 
                  @click="editCategory(category)"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-t-lg"
                >
                  Edit Category
                </button>
                <button 
                  @click="deleteCategory(category)"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-lg"
                >
                  Delete Category
                </button>
              </div>
            </div>
          </div>

          <!-- Category Stats -->
          <div class="flex items-center justify-between text-sm text-gray-500">
            <span>{{ getCategoryTodoCount(category.id) }} todos</span>
            <span class="text-xs">Created {{ formatDate(category.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Create/Edit Modal -->
      <div 
        v-if="showCreateModal || editingCategory"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        @click.self="closeModal"
      >
        <div class="bg-white rounded-xl p-6 w-full max-w-md">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">
            {{ editingCategory ? 'Edit Category' : 'Create New Category' }}
          </h2>
          
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <!-- Name -->
            <div>
              <label for="categoryName" class="block text-sm font-medium text-gray-700 mb-2">
                Name <span class="text-red-500">*</span>
              </label>
              <input
                id="categoryName"
                v-model="modalForm.name"
                type="text"
                required
                :disabled="modalLoading"
                placeholder="Enter category name"
                class="input"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': modalErrors.name }"
              />
              <p v-if="modalErrors.name" class="mt-1 text-sm text-red-600">{{ modalErrors.name }}</p>
            </div>

            <!-- Description -->
            <div>
              <label for="categoryDescription" class="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="categoryDescription"
                v-model="modalForm.description"
                rows="3"
                :disabled="modalLoading"
                placeholder="Enter category description (optional)"
                class="input resize-none"
              ></textarea>
            </div>

            <!-- Color -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Color
              </label>
              <div class="flex items-center space-x-3">
                <input
                  v-model="modalForm.color"
                  type="color"
                  :disabled="modalLoading"
                  class="h-10 w-20 border border-gray-300 rounded-md cursor-pointer"
                />
                <input
                  v-model="modalForm.color"
                  type="text"
                  :disabled="modalLoading"
                  placeholder="#007bff"
                  class="input flex-1"
                  pattern="^#[0-9A-Fa-f]{6}$"
                />
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="modalError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {{ modalError }}
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-end space-x-4 pt-4">
              <button
                type="button"
                @click="closeModal"
                :disabled="modalLoading"
                class="btn btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="modalLoading || !isModalFormValid"
                class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg v-if="modalLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span v-if="modalLoading">{{ editingCategory ? 'Updating...' : 'Creating...' }}</span>
                <span v-else>{{ editingCategory ? 'Update' : 'Create' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useCategoriesStore } from '@/stores/categories'
import { useTodosStore } from '@/stores/todos'
import type { Category } from '@/types/category'

const categoriesStore = useCategoriesStore()
const todosStore = useTodosStore()

// State
const loading = ref(false)
const error = ref<string | null>(null)
const showCreateModal = ref(false)
const editingCategory = ref<Category | null>(null)
const activeMenu = ref<string | null>(null)

// Modal state
const modalLoading = ref(false)
const modalError = ref<string | null>(null)
const modalForm = reactive({
  name: '',
  description: '',
  color: '#3B82F6'
})

const modalErrors = reactive({
  name: ''
})

// Computed
const categories = computed(() => categoriesStore.categories)

const isModalFormValid = computed(() => {
  return modalForm.name.trim().length > 0 && !modalErrors.name
})

// Methods
const toggleMenu = (categoryId: string) => {
  activeMenu.value = activeMenu.value === categoryId ? null : categoryId
}

const closeMenu = () => {
  activeMenu.value = null
}

const getCategoryTodoCount = (categoryId: string) => {
  return todosStore.todos.filter(todo => 
    todo.category_ids && todo.category_ids.includes(categoryId)
  ).length
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const resetModalForm = () => {
  modalForm.name = ''
  modalForm.description = ''
  modalForm.color = '#3B82F6'
  modalErrors.name = ''
  modalError.value = null
}

const closeModal = () => {
  showCreateModal.value = false
  editingCategory.value = null
  resetModalForm()
}

const editCategory = (category: Category) => {
  editingCategory.value = category
  modalForm.name = category.name
  modalForm.description = category.description || ''
  modalForm.color = category.color || '#3B82F6'
  closeMenu()
}

const deleteCategory = async (category: Category) => {
  closeMenu()
  
  if (!confirm(`Are you sure you want to delete "${category.name}"? This action cannot be undone.`)) {
    return
  }

  try {
    await categoriesStore.deleteCategory(category.id)
  } catch (err: any) {
    error.value = err.message || 'Failed to delete category'
  }
}

const validateModalForm = () => {
  modalErrors.name = ''

  if (!modalForm.name.trim()) {
    modalErrors.name = 'Name is required'
  } else if (modalForm.name.trim().length > 30) {
    modalErrors.name = 'Name must be less than 30 characters'
  }

  return !modalErrors.name
}

const handleSubmit = async () => {
  if (!validateModalForm()) return

  try {
    modalLoading.value = true
    modalError.value = null

    const categoryData = {
      name: modalForm.name.trim(),
      description: modalForm.description.trim() || undefined,
      color: modalForm.color
    }

    if (editingCategory.value) {
      await categoriesStore.updateCategory(editingCategory.value.id, categoryData)
    } else {
      await categoriesStore.createCategory(categoryData)
    }

    closeModal()
  } catch (err: any) {
    modalError.value = err.message || `Failed to ${editingCategory.value ? 'update' : 'create'} category`
  } finally {
    modalLoading.value = false
  }
}

// Click outside to close menu
const handleClickOutside = (event: Event) => {
  if (!event.target) return
  
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    closeMenu()
  }
}

// Lifecycle
onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  
  try {
    loading.value = true
    await Promise.all([
      categoriesStore.fetchCategories(),
      todosStore.fetchTodos() // To get todo counts
    ])
  } catch (err: any) {
    error.value = err.message || 'Failed to load categories'
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
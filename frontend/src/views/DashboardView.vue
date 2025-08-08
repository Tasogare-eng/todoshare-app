<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Dashboard Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">
                Welcome back, {{ authStore.user?.username }}! 👋
              </h1>
              <p class="text-gray-600 mt-1">Here's what's happening with your tasks today</p>
            </div>
            <router-link to="/todos/new" class="btn btn-primary">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Add Task
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-blue-100 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-600">Total Tasks</p>
              <p class="text-2xl font-bold text-gray-900">{{ totalTasks }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-green-100 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-600">Completed</p>
              <p class="text-2xl font-bold text-gray-900">{{ completedTasks }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-yellow-100 rounded-full">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-600">In Progress</p>
              <p class="text-2xl font-bold text-gray-900">{{ pendingTasks }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-purple-100 rounded-full">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2M7 4h10M7 4v16a2 2 0 002 2h6a2 2 0 002-2V4m-7 3v2m0 4v2" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-600">Categories</p>
              <p class="text-2xl font-bold text-gray-900">{{ totalCategories }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Tasks -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Recent Tasks</h2>
              <router-link to="/todos" class="text-primary-600 hover:text-primary-700 font-medium">
                View All
              </router-link>
            </div>
            
            <div v-if="recentTasks.length === 0" class="text-center py-12">
              <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <p class="text-gray-600 mb-4">No tasks yet. Create your first task to get started!</p>
              <router-link to="/todos/new" class="btn btn-primary">
                Create Task
              </router-link>
            </div>

            <div v-else class="space-y-4">
              <div v-for="task in recentTasks" :key="task.id" 
                   class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                <input type="checkbox" :checked="task.status === 'completed'" 
                       class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                <div class="ml-3 flex-1">
                  <p class="font-medium text-gray-900" :class="{ 'line-through text-gray-500': task.status === 'completed' }">
                    {{ task.title }}
                  </p>
                  <p v-if="task.due_date" class="text-sm text-gray-600">
                    Due: {{ formatDate(task.due_date) }}
                  </p>
                </div>
                <div v-if="task.priority" class="ml-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                        :class="getPriorityClass(task.priority)">
                    {{ task.priority }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions & Stats -->
        <div class="space-y-8">
          <!-- Quick Actions -->
          <div class="card">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
            <div class="space-y-3">
              <router-link to="/todos/new" 
                           class="block w-full btn btn-primary text-center">
                <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                New Task
              </router-link>
              
              <router-link to="/todos" 
                           class="block w-full btn btn-secondary text-center">
                <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                View All Tasks
              </router-link>
              
              <router-link to="/categories" 
                           class="block w-full btn btn-secondary text-center">
                <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                Manage Categories
              </router-link>
            </div>
          </div>

          <!-- Progress Chart -->
          <div class="card">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Today's Progress</h2>
            <div class="text-center">
              <div class="relative inline-flex items-center justify-center">
                <svg class="w-20 h-20 transform -rotate-90">
                  <circle cx="40" cy="40" r="36" stroke="currentColor" stroke-width="8" fill="transparent" class="text-gray-200" />
                  <circle cx="40" cy="40" r="36" stroke="currentColor" stroke-width="8" fill="transparent"
                          :stroke-dasharray="`${progressPercentage * 2.26} 226`"
                          class="text-primary-600 transition-all duration-500 ease-out" />
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-xl font-bold text-gray-900">{{ progressPercentage }}%</span>
                </div>
              </div>
              <p class="text-gray-600 mt-2">Tasks Completed</p>
              <p class="text-sm text-gray-500 mt-1">{{ completedTasks }} of {{ totalTasks }} tasks</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTodosStore } from '@/stores/todos'
import { useCategoriesStore } from '@/stores/categories'

const authStore = useAuthStore()
const todosStore = useTodosStore()
const categoriesStore = useCategoriesStore()

const totalTasks = computed(() => todosStore.todos.length)
const completedTasks = computed(() => todosStore.completedTodos.length)
const pendingTasks = computed(() => todosStore.pendingTodos.length)
const totalCategories = computed(() => categoriesStore.categories.length)

const recentTasks = computed(() => 
  todosStore.todos.slice(0, 5) // Show only first 5 tasks
)

const progressPercentage = computed(() => {
  if (totalTasks.value === 0) return 0
  return Math.round((completedTasks.value / totalTasks.value) * 100)
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const getPriorityClass = (priority: string) => {
  switch (priority.toLowerCase()) {
    case 'high':
      return 'bg-red-100 text-red-800'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'
    case 'low':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

onMounted(async () => {
  // Load initial data
  await todosStore.fetchTodos()
  await categoriesStore.fetchCategories()
})
</script>
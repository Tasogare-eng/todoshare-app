<template>
  <nav class="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-xl border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="text-xl font-bold text-gray-900">TodoShare</span>
          </router-link>
        </div>

        <!-- Navigation Links & Auth -->
        <div class="flex items-center space-x-4">
          <!-- Debug info (temporary) -->
          <div class="text-xs text-gray-400">
            Auth: {{ authStore.isAuthenticated ? 'Yes' : 'No' }} | 
            Token: {{ authStore.token ? 'Yes' : 'No' }} | 
            User: {{ authStore.user?.username || 'None' }}
          </div>
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
            <!-- Navigation Links for authenticated users -->
            <div class="hidden md:flex items-center space-x-6">
              <router-link to="/dashboard" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Dashboard</router-link>
              <router-link to="/todos" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Tasks</router-link>
            </div>
            
            <!-- User Menu -->
            <div class="relative">
              <button 
                @click="toggleUserMenu" 
                class="flex items-center space-x-2 text-gray-600 hover:text-gray-900 text-sm font-medium px-3 py-2 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <span>{{ authStore.user?.username }}</span>
                <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': showUserMenu }" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </button>
              
              <!-- Dropdown Menu -->
              <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2">
                <div class="px-4 py-2 border-b border-gray-200">
                  <p class="text-sm font-medium text-gray-900">{{ authStore.user?.username }}</p>
                  <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
                </div>
                <button 
                  @click="handleLogout" 
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </div>

          <!-- Auth buttons for non-authenticated users -->
          <div v-else class="flex items-center space-x-4">
            <router-link to="/login" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Sign in</router-link>
            <router-link 
              to="/register" 
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Get started
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showUserMenu = ref(false)

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    showUserMenu.value = false
    // Redirect to home page instead of login to avoid loop
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
    // Force logout even if API fails
    authStore.logout()
    showUserMenu.value = false
    router.push('/')
  }
}

// Close user menu when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as Element
  if (!target.closest('.user-menu')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>


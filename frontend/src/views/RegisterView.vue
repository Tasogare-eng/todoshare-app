<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-blue-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <router-link to="/" class="inline-flex items-center">
          <div class="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mr-3">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span class="text-2xl font-bold gradient-text">TodoShare</span>
        </router-link>
        <h1 class="mt-6 text-3xl font-bold text-gray-900">Create your account</h1>
        <p class="mt-2 text-sm text-gray-600">Join thousands of productive users</p>
      </div>

      <!-- Registration Form -->
      <div class="card">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              :disabled="authStore.loading"
              placeholder="Enter your username"
              class="input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': validationError }"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              :disabled="authStore.loading"
              placeholder="Enter your email"
              class="input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': validationError }"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              :disabled="authStore.loading"
              placeholder="Enter your password (min 8 characters)"
              class="input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': validationError }"
            />
            <p class="mt-2 text-sm text-gray-500">
              Password must contain uppercase, lowercase and numbers
            </p>
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              :disabled="authStore.loading"
              placeholder="Confirm your password"
              class="input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': validationError }"
            />
          </div>

          <!-- Error Messages -->
          <div v-if="validationError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ validationError }}
          </div>

          <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ authStore.error }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.loading || validationError"
            class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold text-lg py-3 px-4 rounded-lg transition-colors"
          >
            <svg v-if="authStore.loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span v-if="authStore.loading">Creating account...</span>
            <span v-else>Create Account</span>
          </button>
        </form>

        <!-- Footer -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Already have an account? 
            <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500 transition-colors">
              Sign in
            </router-link>
          </p>
        </div>
      </div>

      <!-- Additional Info -->
      <div class="text-center">
        <p class="text-xs text-gray-500">
          By creating an account, you agree to our 
          <a href="#" class="text-indigo-600 hover:text-indigo-500">Terms of Service</a> and 
          <a href="#" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validationError = computed(() => {
  if (form.value.password && form.value.confirmPassword) {
    if (form.value.password !== form.value.confirmPassword) {
      return 'Passwords do not match'
    }
  }
  
  if (form.value.password && form.value.password.length < 8) {
    return 'Password must be at least 8 characters long'
  }
  
  return null
})

const handleRegister = async () => {
  if (validationError.value) {
    return
  }

  const success = await authStore.register({
    username: form.value.username,
    email: form.value.email,
    password: form.value.password
  })

  if (success) {
    router.push('/dashboard')
  }
}

onMounted(() => {
  // Clear any previous errors
  authStore.clearError()
  
  // Redirect if already authenticated
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>


<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">Sign In</h1>
      <p class="login-subtitle">Welcome back to TodoShare</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="form.email" type="email" required
            :disabled="authStore.loading" placeholder="Enter your email" />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="relative">
            <input id="password" v-model="form.password"
              :type="showPassword ? 'text' : 'password'" required
              :disabled="authStore.loading" placeholder="Enter your password"
              class="input" />
            <button type="button" @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none"
              :disabled="authStore.loading">
              <svg v-if="showPassword" class="w-5 h-5" fill="none"
                stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2"
                  d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2"
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
        </div>

        <div v-if="authStore.error"
          class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-lg text-sm mt-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd" />
              </svg>
              <span>{{ authStore.error }}</span>
            </div>
            <button @click="authStore.clearError()"
              class="text-red-600 hover:text-red-800 font-bold text-lg leading-none"
              type="button" aria-label="Close error message">
              ×
            </button>
          </div>
        </div>

        <button type="submit" :disabled="authStore.loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-colors">
          <span v-if="authStore.loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">Or continue with</span>
          </div>
        </div>

        <!-- Google Login Button -->
        <button type="button" @click="handleGoogleLogin"
          :disabled="authStore.loading"
          class="w-full border border-gray-300 hover:border-gray-400 disabled:border-gray-200 disabled:cursor-not-allowed text-gray-700 font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-3">
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
            <path fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
            <path fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
          </svg>
          <span>Continue with Google</span>
        </button>
      </form>

      <div class="login-footer">
        <p>Don't have an account? <router-link to="/register">Sign
            up</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const showPassword = ref(false)

const handleLogin = async () => {
  // Clear previous errors before attempting login
  authStore.clearError()

  const success = await authStore.login(form.value)
  if (success) {
    router.push('/dashboard')
  }
}

const handleGoogleLogin = async () => {
  // Clear previous errors
  authStore.clearError()

  try {
    // Load Google Identity Services
    if (!window.google) {
      authStore.setError('Google login is not available')
      return
    }

    // Initialize Google login with FedCM disabled
    window.google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: async (response) => {
        console.log('Google login response received')
        const success = await authStore.googleLogin(response.credential)
        if (success) {
          router.push('/dashboard')
        } else {
          console.error('Google login failed in callback')
        }
      },
      auto_select: false,
      cancel_on_tap_outside: true
    })

    // Create a hidden div for Google button if it doesn't exist
    let googleButtonDiv = document.getElementById('googleButtonDiv')
    if (!googleButtonDiv) {
      googleButtonDiv = document.createElement('div')
      googleButtonDiv.id = 'googleButtonDiv'
      googleButtonDiv.style.display = 'none'
      document.body.appendChild(googleButtonDiv)
    }

    // Render the Google button (hidden)
    window.google.accounts.id.renderButton(
      googleButtonDiv,
      { 
        theme: 'outline',
        size: 'large',
        type: 'standard',
        shape: 'rectangular',
        text: 'continue_with',
        logo_alignment: 'left'
      }
    )

    // Programmatically click the rendered button
    setTimeout(() => {
      const googleButton = googleButtonDiv.querySelector('[role="button"]') as HTMLElement
      if (googleButton) {
        googleButton.click()
      } else {
        console.error('Google button not found')
        authStore.setError('Google login initialization failed')
      }
    }, 100)

  } catch (error) {
    console.error('Google login error:', error)
    authStore.setError('Google login failed')
  }
}

onMounted(() => {
  // Only redirect if already authenticated, don't clear errors
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-title {
  text-align: center;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 2rem;
  font-weight: bold;
}

.login-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #333;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

input:disabled {
  background-color: #f9f9f9;
  cursor: not-allowed;
}



.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.login-footer a {
  color: #4f46e5;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
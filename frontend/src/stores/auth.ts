import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, type UserLogin, type UserRegister } from '@/services/auth'
import { useLocalStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = useLocalStorage('auth_token', '')
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isLoading = computed(() => loading.value)

  // Actions
  const login = async (credentials: UserLogin) => {
    try {
      loading.value = true
      error.value = null

      const response = await authApi.login(credentials)
      token.value = response.access_token

      // Get user info after login
      await getCurrentUser()

      return true
    } catch (err: any) {
      console.error('Login error:', err)
      // Extract error message from various possible formats
      if (err.response?.data?.detail) {
        error.value = err.response.data.detail
      } else if (err.response?.status === 401) {
        error.value = 'Invalid email or password. Please try again.'
      } else if (err.response?.status === 422) {
        error.value = 'Please check your email and password format.'
      } else if (err.message) {
        error.value = err.message
      } else {
        error.value = 'Login failed. Please try again.'
      }
      return false
    } finally {
      loading.value = false
    }
  }

  const register = async (userData: UserRegister) => {
    try {
      loading.value = true
      error.value = null

      const newUser = await authApi.register(userData)
      
      // Auto-login after registration
      await login({
        email: userData.email,
        password: userData.password
      })

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await authApi.logout()
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of API call success
      token.value = ''
      user.value = null
      error.value = null
    }
  }

  const getCurrentUser = async () => {
    try {
      if (!token.value) return null

      const userData = await authApi.getCurrentUser()
      user.value = userData
      return userData
    } catch (err: any) {
      console.error('Get current user error:', err)
      // If token is invalid, clear it
      if (err.response?.status === 401) {
        token.value = ''
        user.value = null
      }
      return null
    }
  }

  const refreshToken = async () => {
    try {
      const response = await authApi.refreshToken()
      token.value = response.access_token
      return true
    } catch (err) {
      console.error('Token refresh error:', err)
      await logout()
      return false
    }
  }

  const clearError = () => {
    error.value = null
  }

  // Initialize user if token exists
  const initializeAuth = async () => {
    if (token.value) {
      await getCurrentUser()
    }
  }

  return {
    // State
    token: computed(() => token.value),
    user: computed(() => user.value),
    loading: isLoading,
    error: computed(() => error.value),
    
    // Getters
    isAuthenticated,
    
    // Actions
    login,
    register,
    logout,
    getCurrentUser,
    refreshToken,
    clearError,
    initializeAuth
  }
})
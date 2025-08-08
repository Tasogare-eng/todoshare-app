<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">Sign In</h1>
      <p class="login-subtitle">Welcome back to TodoShare</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            :disabled="authStore.loading"
            placeholder="Enter your email"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            :disabled="authStore.loading"
            placeholder="Enter your password"
          />
        </div>

        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          <span v-if="authStore.loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>

      <div class="login-footer">
        <p>Don't have an account? <router-link to="/register">Sign up</router-link></p>
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

const handleLogin = async () => {
  const success = await authStore.login(form.value)
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

.error-message {
  color: #e74c3c;
  text-align: center;
  padding: 0.5rem;
  background-color: #ffeaea;
  border-radius: 4px;
  font-size: 0.9rem;
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
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { useAuthStore } from '@/stores/auth'

import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Initialize auth state after pinia is set up
const authStore = useAuthStore()
authStore.initializeAuth()

app.mount('#app')
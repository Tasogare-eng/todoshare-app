<template>
  <div id="app">
    <NavBar v-if="showNavBar" />
    <main :class="{ 'no-padding': !showNavBar }">
      <RouterView />
    </main>
    <ToastNotification />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import ToastNotification from '@/components/ToastNotification.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()

// Don't show NavBar on home page (landing page has its own navigation)
const showNavBar = computed(() => {
  return route.name !== 'home'
})

onMounted(async () => {
  try {
    // Initialize authentication on app startup
    await authStore.initializeAuth()
  } catch (error) {
    console.error('Failed to initialize auth:', error)
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
}

main {
  padding-top: 5rem; /* Account for fixed header */
  padding-left: 1rem;
  padding-right: 1rem;
  padding-bottom: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f8f9fa;
}

main.no-padding {
  padding: 0;
  max-width: none;
  margin: 0;
  background-color: transparent;
}
</style>
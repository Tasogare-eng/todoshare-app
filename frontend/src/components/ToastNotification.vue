<template>
  <transition-group
    name="toast"
    tag="div"
    class="toast-container"
  >
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="['toast', `toast-${toast.type}`]"
      @click="removeToast(toast.id)"
    >
      <div class="toast-icon">
        {{ getIcon(toast.type) }}
      </div>
      <div class="toast-content">
        <div class="toast-title" v-if="toast.title">{{ toast.title }}</div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
      <button class="toast-close" @click.stop="removeToast(toast.id)">×</button>
    </div>
  </transition-group>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()
const toasts = computed(() => toastStore.toasts)

const getIcon = (type: string) => {
  switch (type) {
    case 'success': return '✅'
    case 'error': return '❌'
    case 'warning': return '⚠️'
    case 'info': return 'ℹ️'
    default: return 'ℹ️'
  }
}

const removeToast = (id: string) => {
  toastStore.removeToast(id)
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  min-width: 300px;
  max-width: 400px;
  cursor: pointer;
  pointer-events: auto;
  border-left: 4px solid;
  transition: all 0.3s ease;
}

.toast:hover {
  transform: translateX(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.toast-success {
  border-left-color: #28a745;
  background: #f8fff9;
}

.toast-error {
  border-left-color: #dc3545;
  background: #fff8f8;
}

.toast-warning {
  border-left-color: #ffc107;
  background: #fffdf7;
}

.toast-info {
  border-left-color: #17a2b8;
  background: #f7fdff;
}

.toast-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  color: #343a40;
}

.toast-message {
  font-size: 0.85rem;
  color: #6c757d;
  line-height: 1.4;
  word-wrap: break-word;
}

.toast-close {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 16px;
  flex-shrink: 0;
  transition: all 0.2s;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #495057;
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}

@media (max-width: 768px) {
  .toast-container {
    left: 1rem;
    right: 1rem;
    top: 1rem;
  }
  
  .toast {
    min-width: auto;
    max-width: none;
  }
}
</style>
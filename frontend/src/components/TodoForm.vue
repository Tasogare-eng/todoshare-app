<template>
  <div class="todo-form">
    <div class="form-header">
      <h3>{{ isEditMode ? 'Edit Todo' : 'Create New Todo' }}</h3>
      <button v-if="showCloseButton" @click="$emit('close')" class="close-btn">×</button>
    </div>

    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-group">
        <label for="title">Title *</label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          placeholder="Enter todo title"
          required
          :class="{ error: errors.title }"
          ref="titleInput"
        />
        <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="formData.description"
          placeholder="Enter description (optional)"
          rows="4"
          :class="{ error: errors.description }"
        ></textarea>
        <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="priority">Priority</label>
          <select id="priority" v-model="formData.priority">
            <option value="">No priority</option>
            <option value="low">🟢 Low</option>
            <option value="medium">🟡 Medium</option>
            <option value="high">🔴 High</option>
          </select>
        </div>

        <div class="form-group">
          <label for="due_date">Due Date</label>
          <input
            id="due_date"
            v-model="formData.due_date"
            type="datetime-local"
            :min="minDate"
          />
        </div>
      </div>

      <div class="form-group">
        <CategorySelector
          v-model:selected-category-ids="formData.category_ids"
          @change="handleCategoriesChange"
        />
      </div>

      <div v-if="isEditMode" class="form-group">
        <label for="status">Status</label>
        <select id="status" v-model="formData.status">
          <option value="pending">📋 Pending</option>
          <option value="completed">✅ Completed</option>
        </select>
      </div>

      <div class="form-actions">
        <button
          type="submit"
          :disabled="loading || !formData.title?.trim()"
          class="submit-btn"
        >
          {{ loading ? 'Saving...' : (isEditMode ? 'Update' : 'Create') }}
        </button>
        <button
          type="button"
          @click="handleCancel"
          class="cancel-btn"
        >
          Cancel
        </button>
      </div>
    </form>

    <div v-if="error" class="form-error">
      {{ error }}
      <button @click="clearError" class="clear-error">×</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import type { Todo, TodoCreate, TodoUpdate, TodoPriority } from '@/types/todo'
import { TodoStatus } from '@/types/todo'
import type { Category } from '@/types/category'
import CategorySelector from './CategorySelector.vue'

interface Props {
  todo?: Todo
  loading?: boolean
  error?: string | null
  showCloseButton?: boolean
}

interface Emits {
  (e: 'submit', data: TodoCreate | TodoUpdate): void
  (e: 'cancel'): void
  (e: 'close'): void
  (e: 'clear-error'): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  error: null,
  showCloseButton: true
})

const emit = defineEmits<Emits>()

const titleInput = ref<HTMLInputElement>()

const formData = reactive<{
  title: string
  description: string
  priority: TodoPriority | ''
  due_date: string
  status?: TodoStatus
  category_ids: string[]
}>({
  title: '',
  description: '',
  priority: '',
  due_date: '',
  status: TodoStatus.PENDING,
  category_ids: []
})

const errors = reactive<{
  title?: string
  description?: string
}>({})

const isEditMode = computed(() => !!props.todo)

const minDate = computed(() => {
  const now = new Date()
  return now.toISOString().slice(0, 16)
})

const validateForm = (): boolean => {
  errors.title = ''
  errors.description = ''

  if (!formData.title?.trim()) {
    errors.title = 'Title is required'
    return false
  }

  if (formData.title.trim().length > 200) {
    errors.title = 'Title must be less than 200 characters'
    return false
  }

  if (formData.description && formData.description.length > 1000) {
    errors.description = 'Description must be less than 1000 characters'
    return false
  }

  return true
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  const data = {
    title: formData.title.trim(),
    description: formData.description.trim() || undefined,
    priority: formData.priority || undefined,
    due_date: formData.due_date || undefined,
    category_ids: formData.category_ids,
    ...(isEditMode.value && { status: formData.status })
  }

  emit('submit', data)
}

const handleCancel = () => {
  resetForm()
  emit('cancel')
}

const clearError = () => {
  emit('clear-error')
}

const resetForm = () => {
  formData.title = ''
  formData.description = ''
  formData.priority = ''
  formData.due_date = ''
  formData.status = TodoStatus.PENDING
  formData.category_ids = []
  
  errors.title = ''
  errors.description = ''
}

const formatDateForInput = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toISOString().slice(0, 16)
}

const initializeForm = () => {
  if (props.todo) {
    formData.title = props.todo.title
    formData.description = props.todo.description || ''
    formData.priority = props.todo.priority || ''
    formData.due_date = props.todo.due_date ? formatDateForInput(props.todo.due_date) : ''
    formData.status = props.todo.status
    formData.category_ids = props.todo.category_ids || []
  } else {
    resetForm()
  }
}

const handleCategoriesChange = (categories: Category[]) => {
  // Optional callback for category changes
}

watch(() => props.todo, () => {
  initializeForm()
}, { immediate: true })

onMounted(async () => {
  await nextTick()
  titleInput.value?.focus()
})
</script>

<style scoped>
.todo-form {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.form-header h3 {
  margin: 0;
  color: #343a40;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #495057;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input.error,
.form-group textarea.error {
  border-color: #dc3545;
}

.form-group input.error:focus,
.form-group textarea.error:focus {
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.25);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: -0.25rem;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  justify-content: flex-end;
}

.submit-btn,
.cancel-btn {
  padding: 0.75rem 1.5rem;
  border: 1px solid;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
}

.submit-btn {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
  border-color: #0056b3;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background: white;
  color: #6c757d;
  border-color: #6c757d;
}

.cancel-btn:hover {
  background: #f8f9fa;
  color: #5a6268;
  border-color: #5a6268;
}

.form-error {
  background: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
  position: relative;
  border: 1px solid #f5c6cb;
}

.clear-error {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #721c24;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .todo-form {
    padding: 1rem;
    margin: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .submit-btn,
  .cancel-btn {
    width: 100%;
  }
}
</style>
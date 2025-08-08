<template>
  <div class="category-form">
    <div class="form-header">
      <h3>{{ isEditMode ? 'Edit Category' : 'Create New Category' }}</h3>
      <button v-if="showCloseButton" @click="$emit('close')" class="close-btn">×</button>
    </div>

    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-group">
        <label for="name">Category Name *</label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          placeholder="Enter category name"
          required
          maxlength="30"
          :class="{ error: errors.name }"
          ref="nameInput"
        />
        <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="formData.description"
          placeholder="Enter description (optional)"
          rows="3"
          maxlength="200"
          :class="{ error: errors.description }"
        ></textarea>
        <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
      </div>

      <div class="form-group">
        <label for="color">Color</label>
        <div class="color-selection">
          <div class="color-palette">
            <button
              v-for="colorOption in categoryColors"
              :key="colorOption.value"
              type="button"
              class="color-option"
              :class="{ selected: formData.color === colorOption.value }"
              :style="{ backgroundColor: colorOption.value }"
              :title="colorOption.name"
              @click="formData.color = colorOption.value"
            >
              <span v-if="formData.color === colorOption.value" class="check-mark">✓</span>
            </button>
          </div>
          <div class="custom-color">
            <input
              id="color"
              v-model="formData.color"
              type="color"
              class="color-picker"
            />
            <label for="color" class="color-picker-label">Custom</label>
          </div>
        </div>
      </div>

      <!-- Preview -->
      <div class="form-group">
        <label>Preview</label>
        <div class="category-preview">
          <CategoryBadge :category="previewCategory" />
        </div>
      </div>

      <div class="form-actions">
        <button
          type="submit"
          :disabled="loading || !formData.name?.trim()"
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
import type { Category, CategoryCreate, CategoryUpdate } from '@/types/category'
import { categoryColors } from '@/types/category'
import CategoryBadge from './CategoryBadge.vue'

interface Props {
  category?: Category
  loading?: boolean
  error?: string | null
  showCloseButton?: boolean
}

interface Emits {
  (e: 'submit', data: CategoryCreate | CategoryUpdate): void
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

const nameInput = ref<HTMLInputElement>()

const formData = reactive<{
  name: string
  description: string
  color: string
}>({
  name: '',
  description: '',
  color: '#007bff'
})

const errors = reactive<{
  name?: string
  description?: string
}>({})

const isEditMode = computed(() => !!props.category)

const previewCategory = computed(() => ({
  id: '1',
  user_id: '1',
  name: formData.name || 'Category Name',
  color: formData.color,
  description: formData.description,
  created_at: new Date().toISOString(),
  todo_count: 0
}))

const validateForm = (): boolean => {
  errors.name = ''
  errors.description = ''

  if (!formData.name?.trim()) {
    errors.name = 'Category name is required'
    return false
  }

  if (formData.name.trim().length > 30) {
    errors.name = 'Category name must be less than 30 characters'
    return false
  }

  if (formData.description && formData.description.length > 200) {
    errors.description = 'Description must be less than 200 characters'
    return false
  }

  return true
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  const data = {
    name: formData.name.trim(),
    description: formData.description.trim() || undefined,
    color: formData.color
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
  formData.name = ''
  formData.description = ''
  formData.color = '#007bff'
  
  errors.name = ''
  errors.description = ''
}

const initializeForm = () => {
  if (props.category) {
    formData.name = props.category.name
    formData.description = props.category.description || ''
    formData.color = props.category.color
  } else {
    resetForm()
  }
}

watch(() => props.category, () => {
  initializeForm()
}, { immediate: true })

onMounted(async () => {
  await nextTick()
  nameInput.value?.focus()
})
</script>

<style scoped>
.category-form {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
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
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
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
  min-height: 80px;
  font-family: inherit;
}

.error-message {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: -0.25rem;
}

.color-selection {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.color-palette {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.5rem;
}

.color-option {
  width: 40px;
  height: 40px;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.color-option:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.color-option.selected {
  border-color: #333;
  transform: scale(1.1);
}

.check-mark {
  font-size: 16px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.custom-color {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.color-picker {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.color-picker-label {
  font-size: 0.9rem;
  color: #6c757d;
  cursor: pointer;
}

.category-preview {
  padding: 0.5rem 0;
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
  .category-form {
    padding: 1rem;
    margin: 1rem;
  }

  .color-palette {
    grid-template-columns: repeat(4, 1fr);
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
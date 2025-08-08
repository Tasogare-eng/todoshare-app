<template>
  <div class="todo-card" :class="{ completed: todo.status === 'completed' }">
    <div class="todo-header">
      <div class="todo-checkbox">
        <input
          type="checkbox"
          :checked="todo.status === 'completed'"
          @change="$emit('toggle', todo.id)"
          :id="`todo-${todo.id}`"
        />
        <label :for="`todo-${todo.id}`"></label>
      </div>
      
      <div class="todo-priority" v-if="todo.priority">
        <span 
          :class="`priority-${todo.priority}`"
          :title="`Priority: ${todo.priority}`"
        >
          {{ prioritySymbol }}
        </span>
      </div>
      
      <div class="todo-actions">
        <button @click="startEdit" class="action-btn edit" title="Edit">
          ✏️
        </button>
        <button @click="$emit('delete', todo.id)" class="action-btn delete" title="Delete">
          🗑️
        </button>
      </div>
    </div>

    <div class="todo-content">
      <div v-if="!isEditing" class="todo-display">
        <h3 class="todo-title">{{ todo.title }}</h3>
        <p v-if="todo.description" class="todo-description">
          {{ todo.description }}
        </p>
        
        <!-- Categories -->
        <div v-if="todo.categories && todo.categories.length > 0" class="todo-categories">
          <CategoryBadge
            v-for="category in todo.categories"
            :key="category.id"
            :category="category"
            :clickable="false"
          />
        </div>
        
        <div class="todo-meta">
          <span v-if="todo.due_date" class="due-date" :class="{ overdue: isOverdue }">
            📅 {{ formatDate(todo.due_date) }}
          </span>
          <span class="created-at">
            Created {{ formatRelativeTime(todo.created_at) }}
          </span>
        </div>
      </div>

      <div v-else class="todo-edit">
        <input
          v-model="editData.title"
          class="edit-title"
          placeholder="Todo title"
          @keyup.enter="saveEdit"
          @keyup.escape="cancelEdit"
          ref="titleInput"
        />
        <textarea
          v-model="editData.description"
          class="edit-description"
          placeholder="Description (optional)"
          rows="3"
          @keyup.escape="cancelEdit"
        ></textarea>
        
        <div class="edit-controls">
          <div class="edit-fields">
            <select v-model="editData.priority" class="edit-priority">
              <option value="">No priority</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
            
            <input
              v-model="editData.due_date"
              type="datetime-local"
              class="edit-due-date"
            />
          </div>
          
          <div class="edit-actions">
            <button @click="saveEdit" class="save-btn">Save</button>
            <button @click="cancelEdit" class="cancel-btn">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, nextTick, reactive } from 'vue'
import type { Todo, TodoUpdate } from '@/types/todo'
import CategoryBadge from './CategoryBadge.vue'

interface Props {
  todo: Todo
}

interface Emits {
  (e: 'update', id: string, data: TodoUpdate): void
  (e: 'delete', id: string): void
  (e: 'toggle', id: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const isEditing = ref(false)
const titleInput = ref<HTMLInputElement>()

const editData = reactive<{
  title: string
  description: string
  priority: string
  due_date: string
}>({
  title: props.todo.title,
  description: props.todo.description || '',
  priority: props.todo.priority || '',
  due_date: props.todo.due_date ? formatDateForInput(props.todo.due_date) : ''
})

const prioritySymbol = computed(() => {
  switch (props.todo.priority) {
    case 'high': return '🔴'
    case 'medium': return '🟡'
    case 'low': return '🟢'
    default: return ''
  }
})

const isOverdue = computed(() => {
  if (!props.todo.due_date) return false
  return new Date(props.todo.due_date) < new Date() && props.todo.status !== 'completed'
})

const startEdit = async () => {
  editData.title = props.todo.title
  editData.description = props.todo.description || ''
  editData.priority = props.todo.priority || ''
  editData.due_date = props.todo.due_date ? formatDateForInput(props.todo.due_date) : ''
  
  isEditing.value = true
  
  await nextTick()
  titleInput.value?.focus()
}

const saveEdit = () => {
  if (!editData.title?.trim()) {
    alert('Title is required')
    return
  }

  const updateData: TodoUpdate = {
    title: editData.title.trim(),
    description: editData.description?.trim() || undefined,
    priority: editData.priority ? editData.priority as any : undefined,
    due_date: editData.due_date || undefined
  }

  emit('update', props.todo.id, updateData)
  isEditing.value = false
}

const cancelEdit = () => {
  isEditing.value = false
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMinutes < 1) return 'just now'
  if (diffMinutes < 60) return `${diffMinutes}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  
  return date.toLocaleDateString()
}

function formatDateForInput(dateString: string): string {
  const date = new Date(dateString)
  return date.toISOString().slice(0, 16)
}
</script>

<style scoped>
.todo-card {
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
  position: relative;
}

.todo-card:hover {
  border-color: #c6d0dc;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.todo-card.completed {
  background: #f8f9fa;
  opacity: 0.7;
}

.todo-card.completed .todo-title {
  text-decoration: line-through;
  color: #6c757d;
}

.todo-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.todo-checkbox {
  position: relative;
}

.todo-checkbox input[type="checkbox"] {
  opacity: 0;
  position: absolute;
}

.todo-checkbox label {
  display: block;
  width: 20px;
  height: 20px;
  border: 2px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.todo-checkbox input:checked + label {
  background: #007bff;
  border-color: #007bff;
}

.todo-checkbox input:checked + label::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 12px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.todo-priority {
  margin-left: auto;
}

.priority-high {
  color: #dc3545;
}

.priority-medium {
  color: #ffc107;
}

.priority-low {
  color: #28a745;
}

.todo-actions {
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.todo-card:hover .todo-actions {
  opacity: 1;
}

.action-btn {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.action-btn:hover {
  background: #f8f9fa;
}

.todo-content {
  width: 100%;
}

.todo-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 500;
  color: #343a40;
  line-height: 1.4;
}

.todo-description {
  margin: 0 0 0.75rem 0;
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.4;
  white-space: pre-wrap;
}

.todo-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.todo-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.due-date {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.due-date.overdue {
  color: #dc3545;
  font-weight: 500;
}

.todo-edit {
  width: 100%;
}

.edit-title {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.edit-description {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  resize: vertical;
  min-height: 60px;
}

.edit-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.edit-fields {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.edit-priority,
.edit-due-date {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
}

.save-btn,
.cancel-btn {
  padding: 0.25rem 0.75rem;
  border: 1px solid;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.save-btn:hover {
  background: #0056b3;
  border-color: #0056b3;
}

.cancel-btn {
  background: white;
  color: #6c757d;
  border-color: #6c757d;
}

.cancel-btn:hover {
  background: #f8f9fa;
}

@media (max-width: 768px) {
  .edit-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .edit-fields {
    justify-content: stretch;
  }
  
  .edit-priority,
  .edit-due-date {
    flex: 1;
  }
}
</style>
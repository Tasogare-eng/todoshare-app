<template>
  <div class="filter-panel" :class="{ collapsed: isCollapsed }">
    <div class="panel-header">
      <h3 class="panel-title">Filters</h3>
      <div class="panel-actions">
        <span v-if="activeFiltersCount > 0" class="filter-count">
          {{ activeFiltersCount }} active
        </span>
        <button 
          v-if="hasActiveFilters"
          @click="clearAllFilters"
          class="clear-all-btn"
          title="Clear all filters"
        >
          Clear all
        </button>
        <button
          @click="isCollapsed = !isCollapsed"
          class="collapse-btn"
          :title="isCollapsed ? 'Expand filters' : 'Collapse filters'"
        >
          {{ isCollapsed ? '▲' : '▼' }}
        </button>
      </div>
    </div>

    <div v-if="!isCollapsed" class="panel-content">
      <!-- Status Filter -->
      <div class="filter-group">
        <label class="filter-label">Status</label>
        <div class="filter-options">
          <button
            v-for="option in statusOptions"
            :key="option.value"
            @click="toggleFilter('status', option.value)"
            :class="['filter-chip', { active: filters.status === option.value }]"
          >
            <span class="chip-icon">{{ option.icon }}</span>
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- Priority Filter -->
      <div class="filter-group">
        <label class="filter-label">Priority</label>
        <div class="filter-options">
          <button
            v-for="option in priorityOptions"
            :key="option.value"
            @click="toggleFilter('priority', option.value)"
            :class="['filter-chip', { active: filters.priority === option.value }]"
          >
            <span class="chip-icon">{{ option.icon }}</span>
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- Categories Filter -->
      <div class="filter-group">
        <label class="filter-label">Categories</label>
        <div class="categories-filter">
          <div v-if="categoriesStore.categories.length === 0" class="no-categories">
            No categories available
          </div>
          <div v-else class="category-chips">
            <button
              v-for="category in categoriesStore.categories"
              :key="category.id"
              @click="toggleCategoryFilter(category.id)"
              :class="['category-chip', { active: selectedCategoryIds.includes(category.id) }]"
              :style="{ 
                backgroundColor: selectedCategoryIds.includes(category.id) ? category.color : 'transparent',
                borderColor: category.color,
                color: selectedCategoryIds.includes(category.id) ? 'white' : category.color
              }"
            >
              {{ category.name }}
            </button>
          </div>
        </div>
      </div>

      <!-- Due Date Filter -->
      <div class="filter-group">
        <label class="filter-label">Due Date</label>
        <div class="filter-options">
          <button
            v-for="option in dueDateOptions"
            :key="option.value"
            @click="setDateFilter(option.value)"
            :class="['filter-chip', { active: activeDateFilter === option.value }]"
          >
            <span class="chip-icon">{{ option.icon }}</span>
            {{ option.label }}
          </button>
        </div>
        
        <!-- Custom Date Range -->
        <div v-if="showCustomDateRange" class="date-range-inputs">
          <input
            v-model="customDateRange.from"
            type="date"
            placeholder="From"
            class="date-input"
          />
          <input
            v-model="customDateRange.to"
            type="date"
            placeholder="To"
            class="date-input"
          />
          <button @click="applyCustomDateRange" class="apply-date-btn">
            Apply
          </button>
        </div>
      </div>

      <!-- Applied Filters -->
      <div v-if="hasActiveFilters" class="applied-filters">
        <div class="applied-filters-header">Applied Filters:</div>
        <div class="applied-filter-chips">
          <div
            v-for="filter in appliedFiltersDisplay"
            :key="filter.key"
            class="applied-filter-chip"
          >
            {{ filter.label }}
            <button @click="removeFilter(filter.key)" class="remove-filter">×</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCategoriesStore } from '@/stores/categories'
import type { TodoStatus } from '@/types/todo'

interface FilterValues {
  status: string | null
  priority: string | null
  categoryIds: string[]
  dueDateFrom: string | null
  dueDateTo: string | null
  search: string | null
}

interface Emits {
  (e: 'filtersChanged', filters: FilterValues): void
}

const emit = defineEmits<Emits>()
const categoriesStore = useCategoriesStore()

const isCollapsed = ref(false)
const showCustomDateRange = ref(false)

const filters = reactive<FilterValues>({
  status: null,
  priority: null,
  categoryIds: [],
  dueDateFrom: null,
  dueDateTo: null,
  search: null
})

const customDateRange = reactive({
  from: '',
  to: ''
})

const statusOptions = [
  { value: '', label: 'All', icon: '📋' },
  { value: 'pending', label: 'Pending', icon: '⏳' },
  { value: 'completed', label: 'Completed', icon: '✅' }
]

const priorityOptions = [
  { value: '', label: 'All', icon: '📝' },
  { value: 'high', label: 'High', icon: '🔴' },
  { value: 'medium', label: 'Medium', icon: '🟡' },
  { value: 'low', label: 'Low', icon: '🟢' }
]

const dueDateOptions = [
  { value: '', label: 'All', icon: '📅' },
  { value: 'today', label: 'Today', icon: '🗓️' },
  { value: 'tomorrow', label: 'Tomorrow', icon: '📅' },
  { value: 'this-week', label: 'This Week', icon: '📊' },
  { value: 'overdue', label: 'Overdue', icon: '⚠️' },
  { value: 'custom', label: 'Custom Range', icon: '🎯' }
]

const selectedCategoryIds = computed(() => filters.categoryIds)
const activeDateFilter = ref('')

const activeFiltersCount = computed(() => {
  let count = 0
  if (filters.status) count++
  if (filters.priority) count++
  if (filters.categoryIds.length > 0) count++
  if (filters.dueDateFrom || filters.dueDateTo) count++
  return count
})

const hasActiveFilters = computed(() => activeFiltersCount.value > 0)

const appliedFiltersDisplay = computed(() => {
  const applied = []
  
  if (filters.status) {
    const status = statusOptions.find(s => s.value === filters.status)
    applied.push({ key: 'status', label: `Status: ${status?.label}` })
  }
  
  if (filters.priority) {
    const priority = priorityOptions.find(p => p.value === filters.priority)
    applied.push({ key: 'priority', label: `Priority: ${priority?.label}` })
  }
  
  if (filters.categoryIds.length > 0) {
    const count = filters.categoryIds.length
    applied.push({ key: 'categories', label: `Categories: ${count} selected` })
  }
  
  if (filters.dueDateFrom || filters.dueDateTo) {
    applied.push({ key: 'dateRange', label: 'Custom date range' })
  }
  
  return applied
})

const toggleFilter = (type: string, value: string) => {
  if (type === 'status') {
    filters.status = filters.status === value ? null : (value || null)
  } else if (type === 'priority') {
    filters.priority = filters.priority === value ? null : (value || null)
  }
  emitFilters()
}

const toggleCategoryFilter = (categoryId: string) => {
  const index = filters.categoryIds.indexOf(categoryId)
  if (index === -1) {
    filters.categoryIds.push(categoryId)
  } else {
    filters.categoryIds.splice(index, 1)
  }
  emitFilters()
}

const setDateFilter = (value: string) => {
  activeDateFilter.value = activeDateFilter.value === value ? '' : value
  showCustomDateRange.value = value === 'custom'
  
  if (value === 'custom') {
    return
  }
  
  // Clear previous date filters
  filters.dueDateFrom = null
  filters.dueDateTo = null
  
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  switch (value) {
    case 'today':
      filters.dueDateFrom = today.toISOString()
      filters.dueDateTo = new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1).toISOString()
      break
    case 'tomorrow':
      const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000)
      filters.dueDateFrom = tomorrow.toISOString()
      filters.dueDateTo = new Date(tomorrow.getTime() + 24 * 60 * 60 * 1000 - 1).toISOString()
      break
    case 'this-week':
      const startOfWeek = new Date(today)
      startOfWeek.setDate(today.getDate() - today.getDay())
      const endOfWeek = new Date(startOfWeek.getTime() + 7 * 24 * 60 * 60 * 1000 - 1)
      filters.dueDateFrom = startOfWeek.toISOString()
      filters.dueDateTo = endOfWeek.toISOString()
      break
    case 'overdue':
      filters.dueDateTo = today.toISOString()
      break
    default:
      activeDateFilter.value = ''
  }
  
  emitFilters()
}

const applyCustomDateRange = () => {
  if (customDateRange.from) {
    filters.dueDateFrom = new Date(customDateRange.from).toISOString()
  }
  if (customDateRange.to) {
    const toDate = new Date(customDateRange.to)
    toDate.setHours(23, 59, 59, 999)
    filters.dueDateTo = toDate.toISOString()
  }
  showCustomDateRange.value = false
  emitFilters()
}

const removeFilter = (key: string) => {
  switch (key) {
    case 'status':
      filters.status = null
      break
    case 'priority':
      filters.priority = null
      break
    case 'categories':
      filters.categoryIds = []
      break
    case 'dateRange':
      filters.dueDateFrom = null
      filters.dueDateTo = null
      activeDateFilter.value = ''
      break
  }
  emitFilters()
}

const clearAllFilters = () => {
  filters.status = null
  filters.priority = null
  filters.categoryIds = []
  filters.dueDateFrom = null
  filters.dueDateTo = null
  activeDateFilter.value = ''
  customDateRange.from = ''
  customDateRange.to = ''
  showCustomDateRange.value = false
  emitFilters()
}

const emitFilters = () => {
  emit('filtersChanged', { ...filters })
}

// Watch for external filter changes
watch(() => filters, () => {
  emitFilters()
}, { deep: true })

onMounted(() => {
  categoriesStore.fetchCategories()
})
</script>

<style scoped>
.filter-panel {
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e1e5e9;
  background: #f8f9fa;
}

.panel-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #343a40;
}

.panel-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-count {
  font-size: 0.8rem;
  color: #007bff;
  font-weight: 500;
}

.clear-all-btn {
  background: none;
  border: none;
  color: #dc3545;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: underline;
}

.collapse-btn {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.2s;
}

.collapse-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.panel-content {
  padding: 1rem;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-label {
  display: block;
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  background: white;
  border: 1px solid #ced4da;
  border-radius: 16px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-chip:hover {
  border-color: #007bff;
  background: #f8f9ff;
}

.filter-chip.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.chip-icon {
  font-size: 0.8rem;
}

.categories-filter {
  width: 100%;
}

.no-categories {
  color: #6c757d;
  font-style: italic;
  font-size: 0.9rem;
  padding: 0.5rem 0;
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.category-chip {
  padding: 0.375rem 0.75rem;
  border: 1px solid;
  border-radius: 16px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.category-chip:hover {
  opacity: 0.8;
}

.date-range-inputs {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.date-input {
  padding: 0.375rem 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.85rem;
  flex: 1;
  min-width: 120px;
}

.apply-date-btn {
  padding: 0.375rem 0.75rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
}

.apply-date-btn:hover {
  background: #0056b3;
}

.applied-filters {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e1e5e9;
}

.applied-filters-header {
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.applied-filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.applied-filter-chip {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: #e9ecef;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #495057;
}

.remove-filter {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 12px;
  transition: all 0.2s;
}

.remove-filter:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #495057;
}

.collapsed .panel-content {
  display: none;
}

@media (max-width: 768px) {
  .panel-header {
    padding: 0.75rem;
  }
  
  .panel-content {
    padding: 0.75rem;
  }
  
  .filter-group {
    margin-bottom: 1rem;
  }
  
  .date-range-inputs {
    flex-direction: column;
  }
  
  .date-input {
    min-width: unset;
  }
}
</style>
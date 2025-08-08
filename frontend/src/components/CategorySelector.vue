<template>
  <div class="category-selector">
    <label class="selector-label">Categories</label>
    
    <!-- Selected Categories -->
    <div v-if="selectedCategories.length > 0" class="selected-categories">
      <CategoryBadge
        v-for="category in selectedCategories"
        :key="category.id"
        :category="category"
        :removable="true"
        @remove="removeCategory"
      />
    </div>
    
    <!-- Category Selection Dropdown -->
    <div class="selector-dropdown" :class="{ open: isOpen }">
      <button 
        type="button"
        @click="toggleDropdown"
        class="dropdown-trigger"
      >
        <span>{{ isOpen ? 'Select categories' : 'Add category' }}</span>
        <span class="dropdown-icon">{{ isOpen ? '▲' : '▼' }}</span>
      </button>
      
      <div v-if="isOpen" class="dropdown-content">
        <div class="dropdown-search">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search categories..."
            class="search-input"
          />
        </div>
        
        <div class="categories-list">
          <div
            v-for="category in filteredAvailableCategories"
            :key="category.id"
            @click="addCategory(category)"
            class="category-option"
            :style="{ borderLeftColor: category.color }"
          >
            <div class="category-info">
              <span class="category-name">{{ category.name }}</span>
              <span v-if="category.description" class="category-description">
                {{ category.description }}
              </span>
            </div>
            <div 
              class="category-color-dot" 
              :style="{ backgroundColor: category.color }"
            ></div>
          </div>
          
          <div v-if="filteredAvailableCategories.length === 0" class="no-categories">
            No categories available
          </div>
        </div>
        
        <div class="dropdown-actions">
          <button 
            type="button"
            @click="showCreateForm = true"
            class="create-category-btn"
          >
            + New Category
          </button>
        </div>
      </div>
    </div>
    
    <!-- Create Category Modal -->
    <div v-if="showCreateForm" class="modal-overlay" @click="closeCreateForm">
      <div class="modal-content" @click.stop>
        <CategoryForm
          @submit="handleCreateCategory"
          @cancel="closeCreateForm"
          @close="closeCreateForm"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCategoriesStore } from '@/stores/categories'
import CategoryBadge from './CategoryBadge.vue'
import CategoryForm from './CategoryForm.vue'
import type { Category, CategoryCreate } from '@/types/category'

interface Props {
  selectedCategoryIds?: string[]
}

interface Emits {
  (e: 'update:selectedCategoryIds', categoryIds: string[]): void
  (e: 'change', categories: Category[]): void
}

const props = withDefaults(defineProps<Props>(), {
  selectedCategoryIds: () => []
})

const emit = defineEmits<Emits>()

const categoriesStore = useCategoriesStore()
const { categories } = storeToRefs(categoriesStore)

const isOpen = ref(false)
const searchQuery = ref('')
const showCreateForm = ref(false)

const selectedCategories = computed(() => {
  return categoriesStore.getCategoriesByIds(props.selectedCategoryIds || [])
})

const availableCategories = computed(() => {
  return categories.value.filter(cat => 
    !(props.selectedCategoryIds || []).includes(cat.id)
  )
})

const filteredAvailableCategories = computed(() => {
  if (!searchQuery.value) return availableCategories.value
  
  const query = searchQuery.value.toLowerCase()
  return availableCategories.value.filter(cat =>
    cat.name.toLowerCase().includes(query) ||
    (cat.description?.toLowerCase().includes(query))
  )
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    searchQuery.value = ''
  }
}

const addCategory = (category: Category) => {
  const newCategoryIds = [...(props.selectedCategoryIds || []), category.id]
  emit('update:selectedCategoryIds', newCategoryIds)
  emit('change', categoriesStore.getCategoriesByIds(newCategoryIds))
}

const removeCategory = (categoryId: string) => {
  const newCategoryIds = (props.selectedCategoryIds || []).filter(id => id !== categoryId)
  emit('update:selectedCategoryIds', newCategoryIds)
  emit('change', categoriesStore.getCategoriesByIds(newCategoryIds))
}

const handleCreateCategory = async (data: CategoryCreate | CategoryUpdate) => {
  // Type guard to ensure we have required fields for creation
  if (!('name' in data) || !data.name) {
    return
  }
  const result = await categoriesStore.createCategory(data)
  if (result) {
    showCreateForm.value = false
    // Automatically add the new category to selection
    addCategory(result)
  }
}

const closeCreateForm = () => {
  showCreateForm.value = false
  categoriesStore.clearError()
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as Element
  if (!target.closest('.category-selector')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  categoriesStore.fetchCategories()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.category-selector {
  position: relative;
}

.selector-label {
  display: block;
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.selected-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.selector-dropdown {
  position: relative;
}

.dropdown-trigger {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: border-color 0.2s;
}

.dropdown-trigger:hover {
  border-color: #007bff;
}

.dropdown-icon {
  font-size: 0.8rem;
  color: #6c757d;
  transition: transform 0.2s;
}

.selector-dropdown.open .dropdown-icon {
  transform: rotate(180deg);
}

.dropdown-content {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ced4da;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 300px;
  overflow: hidden;
}

.dropdown-search {
  padding: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.9rem;
}

.categories-list {
  max-height: 200px;
  overflow-y: auto;
}

.category-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.2s;
}

.category-option:hover {
  background: #f8f9fa;
}

.category-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  flex: 1;
}

.category-name {
  font-weight: 500;
  color: #343a40;
}

.category-description {
  font-size: 0.8rem;
  color: #6c757d;
}

.category-color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.no-categories {
  padding: 1rem;
  text-align: center;
  color: #6c757d;
  font-style: italic;
}

.dropdown-actions {
  padding: 0.5rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.create-category-btn {
  width: 100%;
  padding: 0.5rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.create-category-btn:hover {
  background: #0056b3;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  width: 100%;
  max-width: 500px;
}

@media (max-width: 768px) {
  .dropdown-content {
    max-height: 250px;
  }
  
  .categories-list {
    max-height: 150px;
  }
}
</style>
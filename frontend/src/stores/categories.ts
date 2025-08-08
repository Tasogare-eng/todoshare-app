import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { categoriesApi } from '@/services/categories'
import type { Category, CategoryCreate, CategoryUpdate } from '@/types/category'

export const useCategoriesStore = defineStore('categories', () => {
  // State
  const categories = ref<Category[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const categoriesMap = computed(() => {
    const map: Record<string, Category> = {}
    categories.value.forEach(category => {
      map[category.id] = category
    })
    return map
  })

  const getCategoryById = computed(() => {
    return (id: string) => categoriesMap.value[id]
  })

  const getCategoriesByIds = computed(() => {
    return (ids: string[]) => {
      return ids.map(id => categoriesMap.value[id]).filter(Boolean)
    }
  })

  // Actions
  const fetchCategories = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await categoriesApi.getCategories()
      categories.value = response.items
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch categories'
      return false
    } finally {
      loading.value = false
    }
  }

  const createCategory = async (data: CategoryCreate) => {
    try {
      loading.value = true
      error.value = null
      
      const newCategory = await categoriesApi.createCategory(data)
      categories.value.unshift(newCategory)
      
      return newCategory
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create category'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateCategory = async (id: string, data: CategoryUpdate) => {
    try {
      loading.value = true
      error.value = null
      
      const updatedCategory = await categoriesApi.updateCategory(id, data)
      
      const index = categories.value.findIndex(c => c.id === id)
      if (index !== -1) {
        categories.value[index] = updatedCategory
      }
      
      return updatedCategory
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update category'
      return null
    } finally {
      loading.value = false
    }
  }

  const deleteCategory = async (id: string) => {
    try {
      loading.value = true
      error.value = null
      
      await categoriesApi.deleteCategory(id)
      categories.value = categories.value.filter(c => c.id !== id)
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete category'
      return false
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    categories: computed(() => categories.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    
    // Getters
    categoriesMap,
    getCategoryById,
    getCategoriesByIds,
    
    // Actions
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    clearError
  }
})
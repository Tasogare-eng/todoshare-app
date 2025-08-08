import api from './api'
import type { Category, CategoryCreate, CategoryUpdate, CategoryListResponse } from '@/types/category'

export const categoriesApi = {
  async getCategories(): Promise<CategoryListResponse> {
    const response = await api.get('/categories')
    return response.data
  },

  async getCategory(id: string): Promise<Category> {
    const response = await api.get(`/categories/${id}`)
    return response.data
  },

  async createCategory(data: CategoryCreate): Promise<Category> {
    const response = await api.post('/categories', data)
    return response.data
  },

  async updateCategory(id: string, data: CategoryUpdate): Promise<Category> {
    const response = await api.put(`/categories/${id}`, data)
    return response.data
  },

  async deleteCategory(id: string): Promise<void> {
    await api.delete(`/categories/${id}`)
  }
}
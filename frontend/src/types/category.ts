export interface Category {
  id: string
  user_id: string
  name: string
  color: string
  description?: string
  created_at: string
  updated_at?: string
  todo_count: number
}

export interface CategoryCreate {
  name: string
  color?: string
  description?: string
}

export interface CategoryUpdate {
  name?: string
  color?: string
  description?: string
}

export interface CategoryListResponse {
  items: Category[]
  total: number
}

// Predefined color palette
export const categoryColors = [
  { name: 'Blue', value: '#1976d2' },
  { name: 'Green', value: '#388e3c' },
  { name: 'Orange', value: '#f57c00' },
  { name: 'Purple', value: '#7b1fa2' },
  { name: 'Red', value: '#d32f2f' },
  { name: 'Teal', value: '#00796b' },
  { name: 'Indigo', value: '#303f9f' },
  { name: 'Pink', value: '#c2185b' },
  { name: 'Brown', value: '#5d4037' },
  { name: 'Blue Grey', value: '#455a64' },
  { name: 'Deep Orange', value: '#e64a19' },
  { name: 'Lime', value: '#689f38' }
]
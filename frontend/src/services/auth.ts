import api from './api'

export interface UserRegister {
  email: string
  username: string
  password: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface User {
  id: string
  email: string
  username: string
  created_at: string
  is_active: boolean
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export const authApi = {
  async register(userData: UserRegister): Promise<User> {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  async login(credentials: UserLogin): Promise<LoginResponse> {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me')
    return response.data
  },

  async refreshToken(): Promise<LoginResponse> {
    const response = await api.post('/auth/refresh')
    return response.data
  },

  async googleLogin(idToken: string): Promise<LoginResponse> {
    const response = await api.post('/auth/google-login', { id_token: idToken })
    return response.data
  }
}
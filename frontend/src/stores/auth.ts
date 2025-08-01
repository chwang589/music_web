import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api`

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const username = ref<string | null>(localStorage.getItem('username'))
  
  const isAuthenticated = computed(() => token.value !== null)
  
  const login = async (username: string, password: string) => {
    try {
      console.log('🔐 Attempting login with:', { username, API_BASE_URL })
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        username,
        password
      })
      
      console.log('✅ Login response:', response.data)
      
      const { access_token, username: user } = response.data
      token.value = access_token
      username.value = user
      
      localStorage.setItem('token', access_token)
      localStorage.setItem('username', user)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      console.log('✅ Login successful, token stored')
      return { success: true }
    } catch (error: any) {
      console.error('❌ Login error:', error)
      console.error('❌ Error response:', error.response?.data)
      return { success: false, error: error.response?.data?.detail || 'Login failed' }
    }
  }
  
  const register = async (userData: { username: string; email: string; password: string }) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData)
      return { success: true, data: response.data }
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' }
    }
  }
  
  const logout = () => {
    token.value = null
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    delete axios.defaults.headers.common['Authorization']
  }
  
  // Initialize axios with token if exists
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }
  
  return {
    token,
    username,
    isAuthenticated,
    login,
    register,
    logout
  }
})
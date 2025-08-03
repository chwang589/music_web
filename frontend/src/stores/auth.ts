import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api`

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const currentUsername = ref<string | null>(localStorage.getItem('username'))
  
  const isAuthenticated = computed(() => token.value !== null)
  
  const login = async (inputUsername: string, password: string) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        username: inputUsername,
        password
      })
      
      const { access_token, username: responseUsername } = response.data
      token.value = access_token
      currentUsername.value = responseUsername
      
      localStorage.setItem('token', access_token)
      localStorage.setItem('username', responseUsername)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' }
    }
  }
  
  const register = async (userData: { username: string; email: string; password: string; verification_code: string }) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData)
      return { success: true, data: response.data }
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' }
    }
  }
  
  const logout = () => {
    token.value = null
    currentUsername.value = null
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
    username: currentUsername,
    isAuthenticated,
    login,
    register,
    logout
  }
})
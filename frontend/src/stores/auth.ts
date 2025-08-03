import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api`

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const currentUsername = ref<string | null>(localStorage.getItem('username'))
  
  const isAuthenticated = computed(() => {
    const hasToken = !!token.value
    const hasUsername = !!currentUsername.value
    console.log('Auth check - hasToken:', hasToken, 'hasUsername:', hasUsername)
    return hasToken && hasUsername
  })
  
  // Set up axios interceptor to add auth header to all requests
  const setAuthHeader = (authToken: string | null) => {
    if (authToken) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`
    } else {
      delete axios.defaults.headers.common['Authorization']
    }
  }
  
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
      
      setAuthHeader(access_token)
      
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
    setAuthHeader(null)
  }
  
  // Add response interceptor to handle 401 errors globally
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401 && token.value) {
        // Token is invalid, logout automatically
        logout()
      }
      return Promise.reject(error)
    }
  )
  
  // Initialize axios with token if exists
  if (token.value) {
    setAuthHeader(token.value)
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
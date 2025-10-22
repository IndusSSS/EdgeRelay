import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import EdgeRelayApiService from '../services/edgeRelayApi.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  
  const isAuthenticated = computed(() => {
    // Check both the store state and the API service token
    return !!user.value && !!EdgeRelayApiService.token
  })

  const login = (userData, token) => {
    user.value = userData
    // Store in both localStorage keys for compatibility
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('admin_user', JSON.stringify(userData))
    // Set token in API service
    if (token) {
      EdgeRelayApiService.setToken(token)
    }
  }

  const logout = () => {
    user.value = null
    // Clear all auth data
    localStorage.removeItem('user')
    localStorage.removeItem('admin_user')
    EdgeRelayApiService.clearToken()
  }

  const initializeAuth = () => {
    // Try to get user from admin_user first, then fallback to user
    const storedUser = localStorage.getItem('admin_user') || localStorage.getItem('user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
        // Ensure token is loaded
        const token = localStorage.getItem('admin_token')
        if (token) {
          EdgeRelayApiService.setToken(token)
        }
      } catch (error) {
        console.error('Error parsing stored user:', error)
        localStorage.removeItem('user')
        localStorage.removeItem('admin_user')
        EdgeRelayApiService.clearToken()
      }
    }
  }

  const hasRole = (role) => {
    return user.value?.role === role
  }

  const hasAnyRole = (roles) => {
    return roles.includes(user.value?.role)
  }

  // EdgeRelay specific login method
  const loginWithEdgeRelay = async (credentials) => {
    try {
      const response = await EdgeRelayApiService.adminLogin(credentials)
      if (response.data.token) {
        const userData = {
          id: response.data.admin_id,
          username: response.data.username,
          full_name: response.data.full_name,
          role: 'admin'
        }
        login(userData, response.data.token)
        return { success: true, data: response.data }
      }
      return { success: false, error: 'No token received' }
    } catch (error) {
      console.error('EdgeRelay login failed:', error)
      return { success: false, error: error.message }
    }
  }

  return {
    user,
    isAuthenticated,
    login,
    logout,
    initializeAuth,
    hasRole,
    hasAnyRole,
    loginWithEdgeRelay
  }
})

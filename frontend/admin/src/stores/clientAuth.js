import { defineStore } from 'pinia'
import { ref, computed, inject } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const apiService = inject('$api')
  
  const isAuthenticated = computed(() => {
    // Check both the store state and the API service token
    return !!user.value && apiService?.isAuthenticated()
  })

  const login = (userData, token) => {
    user.value = userData
    // Store in both localStorage keys for compatibility
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('admin_user', JSON.stringify(userData))
    // Set token in API service
    if (token && apiService) {
      apiService.setToken(token)
    }
  }

  const logout = () => {
    user.value = null
    // Clear all auth data
    localStorage.removeItem('user')
    localStorage.removeItem('admin_user')
    if (apiService) {
      apiService.clearToken()
    }
  }

  const initializeAuth = () => {
    // Try to get user from admin_user first, then fallback to user
    const storedUser = localStorage.getItem('admin_user') || localStorage.getItem('user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
        // Ensure token is loaded
        const token = localStorage.getItem('admin_token')
        if (token && apiService) {
          apiService.setToken(token)
        }
      } catch (error) {
        console.error('Error parsing stored user:', error)
        localStorage.removeItem('user')
        localStorage.removeItem('admin_user')
        if (apiService) {
          apiService.clearToken()
        }
      }
    }
  }

  const hasRole = (role) => {
    return user.value?.role === role
  }

  const hasAnyRole = (roles) => {
    return roles.includes(user.value?.role)
  }

  return {
    user,
    isAuthenticated,
    login,
    logout,
    initializeAuth,
    hasRole,
    hasAnyRole
  }
})

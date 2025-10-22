import { useAuthStore } from '../stores/auth'

export function requireAuth(to, from, next) {
  const authStore = useAuthStore()
  
  if (!authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
}

export function requireGuest(to, from, next) {
  const authStore = useAuthStore()
  
  if (authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
}

export function requireRole(role) {
  return (to, from, next) => {
    const authStore = useAuthStore()
    
    if (!authStore.isAuthenticated) {
      next('/login')
    } else if (!authStore.hasRole(role)) {
      next('/unauthorized')
    } else {
      next()
    }
  }
}

import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Devices from '../views/Devices.vue'
import Servers from '../views/Servers.vue'
import Client from '../views/Client.vue'
import Analytics from '../views/Analytics.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'AdminDashboard',
    component: Dashboard,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    redirect: '/'
  },
  {
    path: '/devices',
    name: 'Devices',
    component: Devices,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/servers',
    name: 'Servers',
    component: Servers,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/client',
    name: 'Client',
    component: Client,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const user = localStorage.getItem('admin_user')
  
  if (to.meta.requiresAuth) {
    if (!user) {
      // Redirect to admin login
      next('/login')
      return
    }
    
    const userData = JSON.parse(user)
    const userRole = userData.role
    const allowedRoles = to.meta.roles
    
    if (!allowedRoles.includes(userRole)) {
      next('/login')
      return
    }
  }
  
  // If user is authenticated and trying to access login, redirect to dashboard
  if (to.path === '/login' && user) {
    next('/')
    return
  }
  
  next()
})

export default router

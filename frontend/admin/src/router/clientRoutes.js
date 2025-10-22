import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Devices from "../views/Devices.vue"
import Analytics from '../views/Analytics.vue'
import Users from '../views/Users.vue'
import Client from '../views/Client.vue'
import Settings from '../views/Settings.vue'
import ClientDashboard from '../views/ClientDashboard.vue'
import Unauthorized from '../views/Unauthorized.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, roles: ['admin', 'operator', 'super_admin'] }
  },
  {
    path: '/devices',
    name: 'Devices',
    component: Devices,
    meta: { requiresAuth: true, roles: ['admin', 'operator', 'super_admin'] }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics,
    meta: { requiresAuth: true, roles: ['admin', 'operator', 'super_admin'] }
  },
  {
    path: '/client',
    name: 'Client',
    component: Client,
    meta: { requiresAuth: true, roles: ['admin', 'super_admin'] }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true, roles: ['admin', 'operator', 'super_admin'] }
  },
  {
    path: '/client-dashboard',
    name: 'ClientDashboard',
    component: ClientDashboard,
    meta: { requiresAuth: true, roles: ['client'] }
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: Unauthorized
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
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
      next('/login')
      return
    }
    
    const userData = JSON.parse(user)
    const userRole = userData.role
    const allowedRoles = to.meta.roles
    
    if (!allowedRoles.includes(userRole)) {
      next('/unauthorized')
      return
    }
  }
  
  next()
})

export default router

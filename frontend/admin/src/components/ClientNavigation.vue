<template>
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-xl font-bold text-gray-900">IoT Platform</h1>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              v-for="item in navigation"
              :key="item.name"
              :to="item.href"
              :class="[
                $route.name === item.name
                  ? 'border-primary-500 text-gray-900'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
              ]"
            >
              <component :is="item.icon" class="mr-2 h-4 w-4" />
              {{ item.label }}
            </router-link>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <button class="p-2 text-gray-400 hover:text-gray-500">
              <BellIcon class="h-5 w-5" />
            </button>
            <span v-if="unreadAlerts > 0" class="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full"></span>
          </div>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-700">{{ authStore.user?.email || 'admin@iotplatform.com' }}</span>
            <div class="relative">
              <button 
                @click="toggleUserMenu" 
                class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center hover:bg-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                title="User Menu"
              >
                <UserIcon class="h-4 w-4 text-gray-600" />
              </button>
              
              <!-- User Dropdown Menu - Made more visible -->
              <div 
                v-show="showUserMenu" 
                class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl py-2 z-50 border border-gray-200"
                style="box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);"
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ authStore.user?.email || 'admin@iotplatform.com' }}</p>
                  <p class="text-xs text-gray-500">{{ authStore.user?.role || 'Admin' }}</p>
                </div>
                <button 
                  @click="logout" 
                  class="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-red-50 hover:text-red-700 flex items-center transition-colors"
                >
                  <svg class="h-4 w-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                  </svg>
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import {
  BellIcon,
  UserIcon,
  CpuChipIcon,
  ChartBarIcon,
  UsersIcon,
  BuildingOfficeIcon,
  CogIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'AppNavigation',
  components: {
    BellIcon,
    UserIcon,
    CpuChipIcon,
    ChartBarIcon,
    UsersIcon,
    BuildingOfficeIcon,
    CogIcon
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const showUserMenu = ref(false)
    const unreadAlerts = ref(3)

    const navigation = ref([
      { name: 'Analytics', href: '/analytics', label: 'Analytics', icon: 'ChartBarIcon' },
      { name: "Devices", href: "/devices", label: "Devices", icon: "CpuChipIcon" },
      { name: 'Client', href: '/client', label: 'Clients', icon: 'BuildingOfficeIcon' },
      { name: 'Settings', href: '/settings', label: 'Settings', icon: 'CogIcon' }
    ])

    const toggleUserMenu = (event) => {
      event.stopPropagation()
      console.log('Toggle user menu clicked, current state:', showUserMenu.value)
      showUserMenu.value = !showUserMenu.value
      console.log('New state:', showUserMenu.value)
    }

    const closeUserMenu = (event) => {
      // Close menu when clicking outside
      if (!event.target.closest('.relative')) {
        showUserMenu.value = false
      }
    }

    const logout = () => {
      console.log('Logout clicked')
      showUserMenu.value = false
      authStore.logout()
      router.push('/login')
    }

    onMounted(() => {
      // Add click listener to close menu when clicking outside
      document.addEventListener('click', closeUserMenu)
      console.log('AppNavigation mounted')
    })

    onUnmounted(() => {
      // Remove click listener
      document.removeEventListener('click', closeUserMenu)
    })

    return {
      authStore,
      showUserMenu,
      unreadAlerts,
      navigation,
      toggleUserMenu,
      logout
    }
  }
}
</script>

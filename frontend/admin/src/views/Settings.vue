<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">System Settings</h1>
          <p class="text-gray-600 mt-2">Configure system settings and monitor health</p>
        </div>

        <!-- Settings Tabs -->
        <div class="mb-8">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                <component :is="tab.icon" class="h-4 w-4 mr-2 inline" />
                {{ tab.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- Tab Content -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg p-6">
          <!-- System Health Tab -->
          <div v-if="activeTab === 'health'" class="space-y-6">
            <!-- System Status -->
            <div class="card">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="(status, component) in health" :key="component" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center">
                    <div class="h-3 w-3 rounded-full mr-3" :class="getComponentStatusColor(status)"></div>
                    <span class="text-sm font-medium text-gray-900">{{ component }}</span>
                  </div>
                  <span class="text-xs text-gray-500">{{ status }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Security Tab -->
          <div v-if="activeTab === 'security'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Security Settings</h3>
            <p class="text-gray-600">Not implemented</p>
          </div>

          <!-- Users Tab -->
          <div v-if="activeTab === 'users'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">User Management</h3>
            <p class="text-gray-600">Not implemented</p>
          </div>

          <!-- Services Tab -->
          <div v-if="activeTab === 'services'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Service Configuration</h3>
            <p class="text-gray-600">Not implemented</p>
          </div>

          <!-- Database Tab -->
          <div v-if="activeTab === 'database'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Database Management</h3>
            <p class="text-gray-600">Not implemented</p>
          </div>

          <!-- Logs Tab -->
          <div v-if="activeTab === 'logs'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Logs</h3>
            <p class="text-gray-600">Not implemented</p>
          </div>

          <!-- Architecture Tab -->
          <div v-if="activeTab === 'architecture'">
            <ArchitectureView />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ArchitectureView from '../components/ArchitectureView.vue'
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import apiService from '../services/clientApi'
import Users from './Users.vue'
import {
  HeartIcon,
  ShieldCheckIcon,
  UsersIcon,
  CogIcon,
  CircleStackIcon,
  DocumentIcon,
  BuildingOfficeIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'Settings',
  components: {
    ArchitectureView,
    Users,
    HeartIcon,
    ShieldCheckIcon,
    UsersIcon,
    CogIcon,
    CircleStackIcon,
    DocumentIcon,
    BuildingOfficeIcon
  },
  setup() {
    const route = useRoute()
    const activeTab = ref('health')
    const health = ref({
      'API Gateway': 'healthy',
      'Admin Backend': 'healthy',
      'Client Backend': 'healthy',
      'Device Discovery': 'healthy',
      'Client Management': 'healthy',
      'Architecture API': 'healthy',
      'PostgreSQL': 'healthy',
      'Redis': 'healthy',
      'MQTT Broker': 'healthy'
    })
    const services = ref([])
    
    // Check for tab parameter in URL
    if (route.query.tab && ['health', 'security', 'users', 'services', 'database', 'logs', 'architecture'].includes(route.query.tab)) {
      activeTab.value = route.query.tab
    }

    const tabs = ref([
      { id: 'health', name: 'System Health', icon: 'HeartIcon' },
      { id: 'security', name: 'Security', icon: 'ShieldCheckIcon' },
      { id: 'users', name: 'Users', icon: 'UsersIcon' },
      { id: 'services', name: 'Services', icon: 'CogIcon' },
      { id: 'database', name: 'Database', icon: 'CircleStackIcon' },
      { id: 'logs', name: 'Logs', icon: 'DocumentIcon' },
      { id: 'architecture', name: 'Architecture', icon: 'BuildingOfficeIcon' }
    ])

    const categorizedServices = computed(() => {
      const categories = {}
      services.value.forEach(service => {
        const category = service.service_type || 'Uncategorized'
        if (!categories[category]) {
          categories[category] = {
            category,
            services: []
          }
        }
        categories[category].services.push(service)
      })
      return Object.values(categories)
    })

    const getComponentStatusColor = (status) => {
      switch (status) {
        case 'healthy':
          return 'bg-green-500'
        case 'unhealthy':
          return 'bg-red-500'
        case 'degraded':
          return 'bg-yellow-500'
        default:
          return 'bg-gray-400'
      }
    }

    onMounted(() => {
      // In a real scenario, you'd fetch health and services data from an API
      // For now, using mock data
      console.log('Settings page mounted. Fetching system health and services data...')
    })

    return {
      activeTab,
      health,
      services,
      tabs,
      categorizedServices,
      getComponentStatusColor
    }
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Welcome Section -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Welcome, {{ clientInfo.contact_person }}!</h1>
          <p class="text-gray-600 mt-2">{{ clientInfo.company_name }} - Client Dashboard</p>
        </div>

        <!-- Client Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <CpuChipIcon class="h-5 w-5 text-blue-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Devices</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.totalDevices }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircleIcon class="h-5 w-5 text-green-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Online Devices</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.onlineDevices }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <ExclamationTriangleIcon class="h-5 w-5 text-yellow-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Alerts</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.alerts }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <ChartBarIcon class="h-5 w-5 text-purple-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Data Points Today</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.dataPoints }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- My Devices -->
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">My Devices</h3>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div v-for="device in clientDevices" :key="device.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center">
                    <div class="w-3 h-3 rounded-full mr-3" :class="device.status === 'online' ? 'bg-green-400' : 'bg-gray-400'"></div>
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ device.name }}</div>
                      <div class="text-xs text-gray-500">{{ device.type }}</div>
                    </div>
                  </div>
                  <div class="text-xs text-gray-500">{{ device.lastSeen }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Alerts -->
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Recent Alerts</h3>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div v-for="alert in recentAlerts" :key="alert.id" class="flex items-start">
                  <div class="flex-shrink-0">
                    <div class="w-2 h-2 rounded-full mt-2" :class="alert.severity === 'high' ? 'bg-red-400' : alert.severity === 'medium' ? 'bg-yellow-400' : 'bg-blue-400'"></div>
                  </div>
                  <div class="ml-3">
                    <div class="text-sm text-gray-900">{{ alert.message }}</div>
                    <div class="text-xs text-gray-500">{{ alert.time }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Device Requirements -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Device Requirements</h3>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">Sensors</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="sensor in deviceRequirements.sensors" :key="sensor" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                    {{ sensor }}
                  </span>
                </div>
              </div>
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">Connectivity</h4>
                <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                  {{ deviceRequirements.connectivity }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import {
  BellIcon,
  UserIcon,
  CpuChipIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'ClientDashboard',
  components: {
    BellIcon,
    UserIcon,
    CpuChipIcon,
    CheckCircleIcon,
    ExclamationTriangleIcon,
    ChartBarIcon
  },
  setup() {
    const clientInfo = ref({
      company_name: 'Test Company Ltd',
      contact_person: 'John Smith',
      email: 'test@client.com'
    })

    const clientStats = ref({
      totalDevices: 3,
      onlineDevices: 2,
      alerts: 1,
      dataPoints: 1247
    })

    const clientDevices = ref([
      {
        id: 1,
        name: 'Temperature Sensor 01',
        type: 'Temperature Sensor',
        status: 'online',
        lastSeen: '2 min ago'
      },
      {
        id: 2,
        name: 'Humidity Monitor 02',
        type: 'Humidity Sensor',
        status: 'online',
        lastSeen: '5 min ago'
      },
      {
        id: 3,
        name: 'Pressure Gauge 03',
        type: 'Pressure Sensor',
        status: 'offline',
        lastSeen: '2 hours ago'
      }
    ])

    const recentAlerts = ref([
      {
        id: 1,
        message: 'Temperature sensor reading above threshold',
        severity: 'medium',
        time: '10 min ago'
      },
      {
        id: 2,
        message: 'Device connectivity restored',
        severity: 'low',
        time: '1 hour ago'
      }
    ])

    const deviceRequirements = ref({
      sensors: ['temperature', 'humidity', 'pressure'],
      connectivity: 'wifi',
      power: 'battery',
      location: 'indoor'
    })



    onMounted(() => {
      // Load client info from localStorage
      const user = localStorage.getItem('user')
      if (user) {
        const userData = JSON.parse(user)
        clientInfo.value = {
          company_name: userData.company_name || 'Your Company',
          contact_person: userData.contact_person || 'Contact Person',
          email: userData.email || 'your@email.com'
        }
      }
    })

    return {
      clientInfo,
      clientStats,
      clientDevices,
      recentAlerts,
      deviceRequirements,
      
      
    }
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Analytics & Monitoring</h1>
          <p class="text-gray-600 mt-2">Real-time data visualization and system monitoring</p>
        </div>

        <!-- Time Range Selector -->
        <div class="card mb-8">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Time Range</h2>
            <div class="flex space-x-2">
              <button 
                v-for="range in timeRanges" 
                :key="range.value"
                @click="selectedTimeRange = range.value"
                :class="[
                  'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                  selectedTimeRange === range.value
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                {{ range.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- Key Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <ChartBarIcon class="h-5 w-5 text-blue-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Data Points</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ metrics.dataPoints.toLocaleString() }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <ClockIcon class="h-5 w-5 text-green-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Avg Response Time</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ metrics.avgResponseTime }}ms</dd>
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
                  <dd class="text-lg font-medium text-gray-900">{{ metrics.alerts }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <CpuChipIcon class="h-5 w-5 text-purple-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Devices</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ metrics.activeDevices }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Device Status Chart -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Device Status Distribution</h3>
            <div class="h-64 flex items-center justify-center">
              <div class="text-center">
                <div class="w-32 h-32 mx-auto mb-4 relative">
                  <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      class="text-gray-200"
                      stroke="currentColor"
                      stroke-width="3"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      class="text-green-500"
                      stroke="currentColor"
                      stroke-width="3"
                      fill="none"
                      stroke-dasharray="85, 100"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-2xl font-bold text-gray-900">85%</span>
                  </div>
                </div>
                <p class="text-sm text-gray-600">Devices Online</p>
              </div>
            </div>
          </div>

          <!-- Data Flow Chart -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Data Flow Rate</h3>
            <div class="h-64 flex items-center justify-center">
              <div class="w-full h-48 bg-gray-100 rounded-lg flex items-end justify-center space-x-1 p-4">
                <div v-for="(bar, index) in dataFlowBars" :key="index" 
                     class="bg-primary-500 rounded-t" 
                     :style="{ height: bar + '%', width: '8px' }">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Real-time Telemetry -->
        <div class="card mb-8">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Real-time Telemetry</h3>
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-sm text-gray-600">Live</span>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capability</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="telemetry in realtimeTelemetry" :key="telemetry.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ telemetry.device_id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                      {{ telemetry.capability }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ telemetry.value }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatTime(telemetry.timestamp) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- System Performance -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- CPU Usage -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">System Performance</h3>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm text-gray-600 mb-1">
                  <span>CPU Usage</span>
                  <span>{{ systemMetrics.cpu }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" :style="{ width: systemMetrics.cpu + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Memory Usage</span>
                  <span>{{ systemMetrics.memory }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-green-500 h-2 rounded-full" :style="{ width: systemMetrics.memory + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Disk Usage</span>
                  <span>{{ systemMetrics.disk }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-yellow-500 h-2 rounded-full" :style="{ width: systemMetrics.disk + '%' }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Alerts -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h3>
            <div class="space-y-3">
              <div v-for="alert in recentAlerts" :key="alert.id" class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-2 h-2 rounded-full mt-2" :class="getAlertColor(alert.severity)"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-gray-900">{{ alert.message }}</p>
                  <p class="text-xs text-gray-500">{{ formatTime(alert.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  BellIcon,
  UserIcon,
  ChartBarIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CpuChipIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'Analytics',
  components: {
    BellIcon,
    UserIcon,
    ChartBarIcon,
    ClockIcon,
    ExclamationTriangleIcon,
    CpuChipIcon
  },
  setup() {
    const selectedTimeRange = ref('24h')


    const timeRanges = ref([
      { label: '1H', value: '1h' },
      { label: '24H', value: '24h' },
      { label: '7D', value: '7d' },
      { label: '30D', value: '30d' }
    ])

    const metrics = ref({
      dataPoints: 125847,
      avgResponseTime: 45,
      alerts: 12,
      activeDevices: 1189
    })

    const dataFlowBars = ref([65, 78, 45, 89, 67, 92, 55, 73, 81, 68, 76, 84])

    const systemMetrics = ref({
      cpu: 45,
      memory: 62,
      disk: 38
    })

    const realtimeTelemetry = ref([
    ])

    const recentAlerts = ref([
      {
        id: 1,
        severity: 'warning',
        timestamp: new Date(Date.now() - 1000 * 60 * 5)
      },
      {
        id: 2,
        message: 'Device DEV-089 went offline',
        severity: 'error',
        timestamp: new Date(Date.now() - 1000 * 60 * 15)
      },
      {
        id: 3,
        message: 'System backup completed successfully',
        severity: 'info',
        timestamp: new Date(Date.now() - 1000 * 60 * 30)
      }
    ])

    const getAlertColor = (severity) => {
      const colors = {
        info: 'bg-blue-500',
        warning: 'bg-yellow-500',
        error: 'bg-red-500'
      }
      return colors[severity] || 'bg-gray-500'
    }

    const formatTime = (timestamp) => {
      const now = new Date()
      const time = new Date(timestamp)
      const diff = now - time
      const seconds = Math.floor(diff / 1000)
      
      if (seconds < 60) return `${seconds}s ago`
      const minutes = Math.floor(seconds / 60)
      if (minutes < 60) return `${minutes}m ago`
      const hours = Math.floor(minutes / 60)
      return `${hours}h ago`
    }

    let intervalId

    onMounted(() => {
      // Simulate real-time updates
      intervalId = setInterval(() => {
        // Update data flow bars
        dataFlowBars.value = dataFlowBars.value.map(() => Math.floor(Math.random() * 100))
        
        // Update system metrics
        systemMetrics.value.cpu = Math.floor(Math.random() * 100)
        systemMetrics.value.memory = Math.floor(Math.random() * 100)
        systemMetrics.value.disk = Math.floor(Math.random() * 100)
      }, 2000)
    })

    onUnmounted(() => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    })

    return {
      
      selectedTimeRange,
      
      timeRanges,
      metrics,
      dataFlowBars,
      systemMetrics,
      realtimeTelemetry,
      recentAlerts,
      getAlertColor,
      formatTime
    }
  }
}
</script>
